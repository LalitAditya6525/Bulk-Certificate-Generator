
def test_invalid_email_is_rejected(client, sample_payload):
    sample_payload["recipients"][0]["email"] = "not-an-email"

    response = client.post("/api/jobs", json=sample_payload)

    assert response.status_code == 422


def test_empty_recipients_are_rejected(client, sample_payload):
    sample_payload["recipients"] = []

    response = client.post("/api/jobs", json=sample_payload)

    assert response.status_code == 422


def test_missing_course_name_is_rejected(client, sample_payload):
    del sample_payload["course_name"]

    response = client.post("/api/jobs", json=sample_payload)

    assert response.status_code == 422
