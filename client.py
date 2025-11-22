import requests, time, os, sys, json
from pathlib import Path

def main(pdf_path, server):
    r = requests.post(server + "/jobs", files={"file": open(pdf_path, "rb")})
    job_id = r.json()["job_id"]

    job_dir = Path("jobs") / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    while True:
        status = requests.get(server + f"/jobs/{job_id}").json()
        if status["status"] == "completed":
            break
        time.sleep(1)

    # Download job folder via server_jobs volume (manual copy on pod)
    print("Job completed on server. Retrieve outputs from pod at server_jobs/")

if __name__ == "__main__":
    pdf = sys.argv[1]
    server = sys.argv[2]
    main(pdf, server)
