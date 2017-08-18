# Copyright 2017, Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from concurrent import futures
import queue
import logging
import threading

import grpc

from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import helper_threads
from google.cloud.pubsub_v1.subscriber.policy import base
from google.cloud.pubsub_v1.subscriber.message import Message


logger = logging.getLogger(__name__)


class Policy(base.BasePolicy):
    """A consumer class based on :class:``threading.Thread``.

    This consumer handles the connection to the Pub/Sub service and all of
    the concurrency needs.
    """
    def __init__(self, client, subscription, flow_control=types.FlowControl()):
        """Instantiate the policy.

        Args:
            client (~.pubsub_v1.subscriber.client): The subscriber client used
                to create this instance.
            subscription (str): The name of the subscription. The canonical
                format for this is
                ``projects/{project}/subscriptions/{subscription}``.
            flow_control (~.pubsub_v1.types.FlowControl): The flow control
                settings.
        """
        # Default the callback to a no-op; it is provided by `.open`.
        self._callback = lambda message: None

        # Create a queue for keeping track of shared state.
        self._request_queue = queue.Queue()

        # Call the superclass constructor.
        super(Policy, self).__init__(
            client=client,
            flow_control=flow_control,
            subscription=subscription,
        )

        # Also maintain a request queue and an executor.
        logger.debug('Creating callback requests thread (not starting).')
        self._executor = futures.ThreadPoolExecutor()
        self._callback_requests = helper_threads.QueueCallbackThread(
            self._request_queue,
            self.on_callback_request,
        )

    def close(self):
        """Close the existing connection."""
        # Close the main subscription connection.
        self._consumer.helper_threads.stop('callback requests worker')
        self._consumer.stop_consuming()

    def open(self, callback):
        """Open a streaming pull connection and begin receiving messages.

        For each message received, the ``callback`` function is fired with
        a :class:`~.pubsub_v1.subscriber.message.Message` as its only
        argument.

        Args:
            callback (Callable): The callback function.
        """
        # Start the thread to pass the requests.
        logger.debug('Starting callback requests worker.')
        self._callback = callback
        self._consumer.helper_threads.start('callback requests worker',
            self._request_queue,
            self._callback_requests,
        )

        # Actually start consuming messages.
        self._consumer.start_consuming()

        # Spawn a helper thread that maintains all of the leases for
        # this policy.
        logger.debug('Spawning lease maintenance worker.')
        self._leaser = threading.Thread(target=self.maintain_leases)
        self._leaser.daemon = True
        self._leaser.start()

    def on_callback_request(self, callback_request):
        """Map the callback request to the appropriate GRPC request."""
        action, kwargs = callback_request[0], callback_request[1]
        getattr(self, action)(**kwargs)

    def on_exception(self, exception):
        """Bubble the exception.

        This will cause the stream to exit loudly.
        """
        # If this is DEADLINE_EXCEEDED, then we want to retry.
        # That entails just returning None.
        deadline_exceeded = grpc.StatusCode.DEADLINE_EXCEEDED
        if getattr(exception, 'code', lambda: None)() == deadline_exceeded:
            return

        # Raise any other exception.
        raise exception

    def on_response(self, response):
        """Process all received Pub/Sub messages.

        For each message, schedule a callback with the executor.
        """
        for msg in response.received_messages:
            logger.debug('New message received from Pub/Sub: %r', msg)
            logger.debug(self._callback)
            message = Message(msg.message, msg.ack_id, self._request_queue)
            future = self._executor.submit(self._callback, message)
            logger.debug('Result: %s' % future.result())
