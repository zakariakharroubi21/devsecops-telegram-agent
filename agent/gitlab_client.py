import requests
from config import (
    GITLAB_URL,
    GITLAB_TOKEN,
    GITLAB_PROJECT_ID,
    GITLAB_REF
)


class GitLabClient:
    def __init__(self):
        self.base_url = f"{GITLAB_URL}/api/v4/projects/{GITLAB_PROJECT_ID}"

        self.headers = {
            "PRIVATE-TOKEN": GITLAB_TOKEN
        }

    # =========================
    # TRIGGER PIPELINE (SAFE)
    # =========================
    def trigger_pipeline(self, mode="full"):
        print("=== TRIGGER PIPELINE ===")

        url = f"{self.base_url}/pipeline"

        # SAFE: only ref, no variable injection via API
        payload = {
            "ref": GITLAB_REF,
            "variables": [
                {
                    "key": "PIPELINE_MODE",
                    "value": mode
                }
            ]
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        response.raise_for_status()
        return response.json()

    # =========================
    # GET LATEST PIPELINE
    # =========================
    def get_latest_pipeline(self):
        url = f"{self.base_url}/pipelines"

        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()

        pipelines = response.json()
        return pipelines[0] if pipelines else None

    # =========================
    # GET JOBS
    # =========================
    def get_pipeline_jobs(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}/jobs"

        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()
        return response.json()

    # =========================
    # CANCEL PIPELINE
    # =========================
    def cancel_pipeline(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}/cancel"

        response = requests.post(url, headers=self.headers, timeout=20)
        response.raise_for_status()
        return response.json()

    # =========================
    # GET LOGS
    # =========================
    def get_job_logs(self, job_id):
        url = f"{self.base_url}/jobs/{job_id}/trace"

        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()
        return response.text
    
    def get_job_artifact(self, job_id, filename):
        url = (
            f"{self.base_url}/jobs/"
            f"{job_id}/artifacts/{filename}"
        )
        
        response = requests.get(
            url,
            headers=self.headers
    )   
        response.raise_for_status()
        return response.text