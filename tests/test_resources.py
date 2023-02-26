import pytest

from app import models


def test_GetList(authorized_client, resources):
    res = authorized_client.get("/GetList")
    assert res.status_code == 200
    for index in range(len(resources)):
        assert res.json()[index]["title"] == resources[index]["title"]
        assert res.json()[index]["content"] == resources[index]["content"]


@pytest.mark.parametrize(
    "id, expected_statuscode",
    [
        (1, 200),
        (2, 200),
        (100, 404),
    ],
)
def test_GetOne(authorized_client, resources, id, expected_statuscode):
    res = authorized_client.get(f"/GetOne/id={id}")

    assert res.status_code == expected_statuscode

    if expected_statuscode == 200:
        assert res.json()["title"] == resources[id - 1]["title"]
        assert res.json()["content"] == resources[id - 1]["content"]
        assert res.json()["id"] == id


@pytest.mark.parametrize(
    "id, expected_statuscode",
    [
        (2, 204),
        (3, 204),
        (100, 404),
    ],
)
def test_DeleteOne(authorized_client, resources, session, id, expected_statuscode):
    res = authorized_client.delete(f"/DeleteOne/id={id}")

    assert res.status_code == expected_statuscode
    if expected_statuscode == 204:
        assert (
            not session.query(models.Resource).filter(models.Resource.id == id).first()
        )


@pytest.mark.parametrize(
    "id,body, expected_statuscode",
    [
        (1, {"title": "updated", "content": "updated"}, 200),
        (1, {"wrong": "updated", "content": "updated"}, 422),
        (1, {"title": "updated", "wrong": "updated"}, 422),
        (1, "", 422),
        (100, {"title": "updated", "content": "updated"}, 404),
    ],
)
def test_UpdateOne(
    authorized_client, resources, session, id, body, expected_statuscode
):
    res = authorized_client.put(f"/UpdateOne/id={id}", json=body)

    assert res.status_code == expected_statuscode
    if expected_statuscode == 200:
        updated_resource = (
            session.query(models.Resource).filter(models.Resource.id == id).first()
        )
        assert updated_resource.title == body["title"]
        assert updated_resource.content == body["content"]


@pytest.mark.parametrize(
    "payload, expected_statuscode, n_expected_resources",
    [
        (
            {
                "created_at__gte": "2023-01-04T12:00:01.000",
                "created_at__lte": "2023-01-01T12:00:00.000",
            },
            200,
            3,
        ),
        (
            {
                "created_at__gte": "2023-01-04T12:00:00.000",
                "created_at__lte": "2023-01-01T12:00:00.000",
            },
            200,
            2,
        ),
        (
            {
                "created_at__gte": "2023-01-03T12:00:00.000",
                "created_at__lte": "2023-01-01T12:00:00.000",
            },
            200,
            1,
        ),
        (
            {
                "created_at__gte": "2023-01-02T12:00:00.000",
                "created_at__lte": "2023-01-01T12:00:00.000",
            },
            200,
            0,
        ),
        (
            {
                "wrong": "2023-01-02T12:00:00.000",
                "created_at__lte": "2023-01-01T12:00:00.000",
            },
            422,
            None,
        ),
        (
            {
                "created_at__gte": "2023-01-02T12:00:00.000",
                "wrong": "2023-01-01T12:00:00.000",
            },
            422,
            None,
        ),
        (
            {"created_at__gte": "wrong", "created_at__lte": "2023-01-01T12:00:00.000"},
            422,
            None,
        ),
        (
            {"created_at__gte": "2023-01-02T12:00:00.000", "created_at__lte": "wrong"},
            422,
            None,
        ),
        (
            {
                "created_at__gte": "2023-01-02T12:00:00.000",
                "created_at__lte": "2023-01-03T12:00:00.000",
            },
            422,
            None,
        ),
    ],
)
def test_get_items_by_creation_date(
    authorized_client, resources, payload, expected_statuscode, n_expected_resources
):
    res = authorized_client.get(f"/items", params=payload)

    assert res.status_code == expected_statuscode
    if res.status_code == 200:
        assert len(res.json()) == n_expected_resources
        for resource in res.json():
            assert (
                payload["created_at__gte"]
                > resource["created_at"]
                > payload["created_at__lte"]
            )
