.. toctree::
  :maxdepth: 1
  :hidden:

Resource Manager
----------------

Overview
~~~~~~~~

The Cloud Resource Manager API provides methods that you can use
to programmatically manage your projects in the Google Cloud Platform.
With this API, you can do the following:

- Get a list of all projects associated with an account
- Create new projects
- Update existing projects
- Delete projects
- Undelete, or recover, projects that you don't want to delete

.. note::

    Don't forget to look at the **Authentication** section below.
    It's slightly different from the rest of this library.

Here's a quick example of the full life-cycle::

    >>> from gcloud import resource_manager

    >>> # List all projects you have access to
    >>> client = resource_manager.Client()
    >>> for project in client.list_projects():
    ...     print project

    >>> # Create a new project
    >>> new_project = client.project('your-project-id-here')
    >>> new_project.name = 'My new project'
    >>> new_project.create()

    >>> # Update an existing project
    >>> project = client.get_project('my-existing-project')
    >>> print project
    <Project: Existing Project (my-existing-project)>
    >>> project.name = 'Modified name'
    >>> project.update()
    >>> print project
    <Project: Modified name (my-existing-project)>

    >>> # Delete a project
    >>> project = client.get_project('my-existing-project')
    >>> project.delete()

    >>> # Undelete a project
    >>> project = client.get_project('my-existing-project')
    >>> project.undelete()

Authentication
~~~~~~~~~~~~~~

Unlike the other APIs, the Resource Manager API is focused on managing your
various projects inside Google Cloud Platform. What this means (currently) is
that you can't use a Service Account to work with some parts of this API
(for example, creating projects).

The reason is actually pretty simple: if your API call is trying to do
something like create a project, what project's Service Account can you use?
Currently none.

This means that for this API you should always use the credentials
provided by the Cloud SDK, which you can get by running ``gcloud auth login``
(if you're not familiar with this, take a look at http://cloud.google.com/sdk).

Once you run that command, ``gcloud`` will automatically pick up the
credentials from the Cloud SDK, and you can use the "automatic discovery"
feature of the library.

Start by authenticating::

    $ gcloud auth login

And then simply create a client::

    >>> from gcloud import resource_manager
    >>> client = resource_manager.Client()
