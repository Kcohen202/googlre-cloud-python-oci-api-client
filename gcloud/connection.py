"""Module to define base Connection class used by all APIs."""

from pkg_resources import get_distribution

import httplib2


class Connection(object):
    """A generic connection to Google Cloud Platform.

    Subclasses should understand
    only the basic types
    in method arguments,
    however they should be capable
    of returning advanced types.
    """

    API_BASE_URL = 'https://www.googleapis.com'
    """The base of the API call URL."""

    _EMPTY = object()
    """A pointer to represent an empty value for default arguments."""

    # pylint: disable=maybe-no-member
    USER_AGENT = "gcloud-python/{0}".format(get_distribution('gcloud').version)
    # pylint: enable=maybe-no-member
    """The user agent for gcloud-python requests."""

    def __init__(self, credentials=None):
        """
        :type credentials: :class:`gcloud.credentials.Credentials`
        :param credentials: The OAuth2 Credentials to use for this connection.
        """

        self._credentials = credentials

    @property
    def credentials(self):
        """Get the connection's credentials."""
        return self._credentials

    @property
    def http(self):
        """A getter for the HTTP transport used in talking to the API.

        :rtype: :class:`httplib2.Http`
        :returns: A Http object used to transport data.
        """
        if not hasattr(self, '_http'):
            # pylint: disable=attribute-defined-outside-init
            self._http = httplib2.Http()
            if self._credentials:
                self._http = self._credentials.authorize(self._http)
            # pylint: enable=attribute-defined-outside-init
        return self._http
