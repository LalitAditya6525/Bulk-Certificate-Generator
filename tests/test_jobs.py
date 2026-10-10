
def test_create_job(client, sample_payload):
    response = client.post("/api/jobs", json=sample_payload)

    assert response.status_code == 202

    data = response.json()
    assert data["id"] > 0
    assert data["total_count"] == 2
    assert data["status"] == "queued"

    status_response = client.get(f"/api/jobs/{data['id']}")

    assert status_response.status_code == 200
    assert status_response.json()["total_count"] == 2


def test_job_not_found(client):
    response = client.get("/api/jobs/99999")

    assert response.status_code == 404
