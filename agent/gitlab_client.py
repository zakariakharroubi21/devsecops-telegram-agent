import requests
from config import GITLAB_URL, GITLAB_TOKEN, GITLAB_PROJECT_ID, GITLAB_REF, GITLAB_TRIGGER_TOKEN


class GitLabClient:
    def __init__(self):
        self.base_url = f"{GITLAB_URL}/api/v4/projects/{GITLAB_PROJECT_ID}"
        self.headers = {
            "PRIVATE-TOKEN": GITLAB_TOKEN
        }

    def trigger_pipeline(self, mode="full"):
        url =  f"{self.base_url}/pipeline"

        data = {
            "ref": GITLAB_REF,
            "variables[PIPELINE_MODE]": str(mode)
        }

        response = requests.post(url,headers=self.headers, data=data)
        print("STATUS:", response.status_code)
        print("TEXT:", response.text)
        response.raise_for_status()
        return response.json()

    def get_latest_pipeline(self):
        url = f"{self.base_url}/pipelines"

        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()

        pipelines = response.json()

        if not pipelines:
            return None

        return pipelines[0]

    def get_pipeline_jobs(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}/jobs"

        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()

        return response.json()

    def cancel_pipeline(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}/cancel"

        response = requests.post(url, headers=self.headers, timeout=20)
        response.raise_for_status()

        return response.json()

    def get_job_logs(self, job_id):
        url = f"{self.base_url}/jobs/{job_id}/trace"

        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()

        return response.text