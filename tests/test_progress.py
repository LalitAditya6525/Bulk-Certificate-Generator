
def test_job_progress(client, sample_payload):
    response = client.post("/api/jobs", json=sample_payload)
    job_id = response.json()["id"]

    status_response = client.get(f"/api/jobs/{job_id}")

    assert status_response.status_code == 200

    status = status_response.json()

    assert status["progress_percent"] == 100.0
    assert (
        status["success_count"] + status["failed_count"]
        == status["total_count"]
    )
