def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")

    assert response.status_code == 200
    json_data = response.json()
    assert "Chess Club" in json_data
    assert "Programming Class" in json_data
    assert "Gym Class" in json_data
    assert json_data["Gym Class"]["max_participants"] == 30


def test_signup_for_activity_adds_participant(client):
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()["Programming Class"]["participants"]

    response = client.post(
        "/activities/Programming Class/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Programming Class"
    }

    updated_response = client.get("/activities")
    updated_participants = updated_response.json()["Programming Class"]["participants"]

    assert "newstudent@mergington.edu" in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_for_nonexistent_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "fail@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
