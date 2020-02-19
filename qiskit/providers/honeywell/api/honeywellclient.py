#   Copyright 2019-2020 Honeywell, Intl. (www.honeywell.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Client for accessing Honeywell."""

import os
from requests.compat import urljoin

from .session import RetrySession
from .rest import Api

_api_url = 'https://hqsapi.honeywell.com'
_api_version = 'v1'


class HoneywellClient:
    """Client for programmatic access to the Honeywell API."""

    def __init__(self):
        """ HoneywellClient constructor """

        self.client_api = self._init_service_client()

    def _init_service_client(self):
        """Initialize the client used for communicating with the API.

        Returns:
            Api: client for the api server.
        """
        access_token = None
        if 'HQS_API_KEY' in os.environ:
            access_token = os.environ['HQS_API_KEY']

        service_url = urljoin(_api_url, _api_version)

        # Create the api server client, using the access token.
        client_api = Api(RetrySession(service_url, access_token))

        return client_api
    
    def has_token(self):
        return bool(self.client_api.session.access_token)

    def authenticate(self, token=None):
        if token:
            self.client_api.session.access_token = token
        else:
            self.client_api.session.access_token = self._request_access_token()

    def _request_access_token(self):
        access_token = os.environ.get('HQS_API_KEY')
        if access_token is None:
            try:
                input_fun = raw_input
            except NameError:
                input_fun = input
            access_token = input_fun("API Key:")
        return access_token

    # Backend-related public functions.

    def list_backends(self):
        """Return a list of backends.

        Returns:
            list[dict]: a list of backends.
        """
        return self.client_api.backends()

    def backend_status(self, backend_name):
        """Return the status of a backend.

        Args:
            backend_name (str): the name of the backend.

        Returns:
            dict: backend status.
        """
        return self.client_api.backend(backend_name).status()

    # Jobs-related public functions.

    def job_submit(self, backend_name, qobj_config, qasm):
        """Submit a Qobj to a device.

        Args:
            backend_name (str): the name of the backend.
            qobj_dict (dict): the Qobj to be executed, as a dictionary.

        Returns:
            dict: job status.
        """
        return self.client_api.submit_job(backend_name, qobj_config, qasm)

    def job_status(self, job_id):
        """Return the status of a job.

        Args:
            job_id (str): the id of the job.

        Returns:
            dict: job status.
        """
        return self.client_api.job(job_id).status()
