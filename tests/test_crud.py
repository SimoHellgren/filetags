import pytest

from filetags import crud


class TestTagCRUD:
    def test_create(self, conn):
        row = crud.tag.create(conn, "rock", "genre")

        assert row["name"] == "rock"
        assert row["category"] == "genre"
        assert row["id"] is not None

    def test_create_without_category(self, conn):
        row = crud.tag.create(conn, "rock")

        assert row["name"] == "rock"
        assert row["category"] is None
        assert row["id"] is not None

    def test_get_by_name(self, conn):
        crud.tag.create(conn, "rock")

        row = crud.tag.get_by_name(conn, "rock")

        assert row["name"] == "rock"

    def test_get_by_name_not_found(self, conn):
        row = crud.tag.get_by_name(conn, "this doesn't exist!")

        assert row is None

    def test_get_many_by_name(self, conn):
        crud.tag.create(conn, "rock")
        crud.tag.create(conn, "opera")
        crud.tag.create(conn, "jazz")

        rows = crud.tag.get_many_by_name(conn, ["rock", "opera"])

        assert len(rows) == 2
        assert {"rock", "opera"} == {r["name"] for r in rows}

    def test_get_many_by_name_empty(self, conn):
        rows = crud.tag.get_many_by_name(conn, [])

        assert rows == []

    def test_get_many_by_name_missing(self, conn):
        crud.tag.create(conn, "rock")
        crud.tag.create(conn, "opera")

        rows = crud.tag.get_many_by_name(conn, ["rock", "jazz"])

        names = {r["name"] for r in rows}

        assert len(rows) == 1
        assert "rock" in names
        assert "opera" not in names
        assert "jazz" not in names

    def test_get_or_create_creates(self, conn):
        row = crud.tag.get_or_create(conn, "rock")

        assert row["name"] == "rock"

    def test_get_or_create_idempotent(self, conn):
        row1 = crud.tag.get_or_create(conn, "rock")
        row2 = crud.tag.get_or_create(conn, "rock")

        assert row1["id"] == row2["id"]

    def test_get_or_create_many(self, conn):
        rows = crud.tag.get_or_create_many(conn, ["rock", "jazz"])

        assert len(rows) == 2

    def test_get_or_create_many_idempotent(self, conn):
        rows1 = crud.tag.get_or_create_many(conn, ["rock", "jazz"])
        rows2 = crud.tag.get_or_create_many(conn, ["rock", "jazz"])

        ids1 = {r["id"] for r in rows1}
        ids2 = {r["id"] for r in rows2}
        assert ids1 == ids2

    def test_get_all(self, conn):
        crud.tag.create(conn, "rock")
        crud.tag.create(conn, "jazz")

        rows = crud.tag.get_all(conn)

        assert len(rows) == 2

    def test_get_all_empty(self, conn):
        rows = crud.tag.get_all(conn)

        assert rows == []

    def test_update_single(self, conn):
        crud.tag.create(conn, "rock")

        crud.tag.update(conn, ["rock"], {"category": "genre"})

        row = crud.tag.get_by_name(conn, "rock")
        assert row["category"] == "genre"

    def test_update_multiple(self, conn):
        crud.tag.create(conn, "rock")
        crud.tag.create(conn, "jazz")

        crud.tag.update(conn, ["rock", "jazz"], {"category": "genre"})

        for name in ["rock", "jazz"]:
            row = crud.tag.get_by_name(conn, name)
            assert row["category"] == "genre"

    def test_update_forbidden_column(self, conn):
        crud.tag.create(conn, "rock")

        with pytest.raises(ValueError, match="Forbidden column"):
            crud.tag.update(conn, ["rock"], {"id": 999})

    def test_delete(self, conn):
        row = crud.tag.create(conn, "rock")

        crud.tag.delete(conn, row["id"])

        assert crud.tag.get_by_name(conn, "rock") is None
