
def test_list_and_download_certificates(client, sample_payload):
    response = client.post("/api/jobs", json=sample_payload)
    job_id = response.json()["id"]

    list_response = client.get(
        f"/api/jobs/{job_id}/certificates"
    )

    assert list_response.status_code == 200

    certificates = list_response.json()
    assert len(certificates) == 2

    certificate_id = certificates[0]["id"]

    download_response = client.get(
        f"/api/certificates/{certificate_id}"
    )

    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/pdf"
    assert download_response.content.startswith(b"%PDF")


def test_missing_certificate_returns_404(client):
    response = client.get("/api/certificates/99999")

    assert response.status_code == 404
