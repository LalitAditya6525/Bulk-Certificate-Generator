
from pathlib import Path


def test_certificates_are_generated(client, sample_payload):
    response = client.post("/api/jobs", json=sample_payload)

    assert response.status_code == 202
    job_id = response.json()["id"]

    status = client.get(f"/api/jobs/{job_id}").json()

    assert status["success_count"] == 2
    assert status["failed_count"] == 0
    assert status["status"] == "completed"

    certificates = client.get(
        f"/api/jobs/{job_id}/certificates"
    ).json()

    assert len(certificates) == 2

    for certificate in certificates:
        assert Path(certificate["file_path"]).is_file()
