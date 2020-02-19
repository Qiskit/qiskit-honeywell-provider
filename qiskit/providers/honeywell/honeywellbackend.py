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

"""Module for interfacing with a Honeywell Backend."""

import logging

from marshmallow import ValidationError

from qiskit.providers import BaseBackend
from qiskit.providers.models import BackendStatus

from .honeywelljob import HoneywellJob

logger = logging.getLogger(__name__)


class HoneywellBackend(BaseBackend):
    """Backend class interfacing with a Honeywell backend."""

    def __init__(self, name, provider, api):
        """Initialize remote backend for Honeywell Quantum Computer.

        Args:
            name (String): name of backend.
            provider (HoneywellProvider): provider.
        """
        super().__init__(configuration=None, provider=provider)

        self._api = api
        self._name = name

    def run(self, qobj):
        """Run a Qobj.

        Args:
            qobj (Qobj): description of job

        Returns:
            HoneywelJob: an instance derived from BaseJob
        """
        job = HoneywellJob(self, None, self._api, qobj=qobj)
        job.submit()
        return job

    def retrieve_job(self, job_id):
        """ Returns the job associated with the given job_id """
        job = HoneywellJob(self, job_id, self._api)
        return job

    def retrieve_jobs(self, job_ids):
        """ Returns a list of jobs associated with the given job_ids """
        return [HoneywellJob(self, job_id, self._api) for job_id in job_ids]

    def status(self):
        """Return the online backend status.

        Returns:
            BackendStatus: The status of the backend.

        Raises:
            LookupError: If status for the backend can't be found.
            HoneywellBackendError: If the status can't be formatted properly.
        """
        api_status = self._api.backend_status(self.name())

        try:
            return BackendStatus.from_dict(api_status)
        except ValidationError as ex:
            raise LookupError(
                "Couldn't get backend status: {0}".format(ex)
            )

    def name(self):
        return self._name
