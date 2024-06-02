from filetags.src.models import Tag


def test_tag_creation():
    t = Tag("test")

    assert t.name == "test"
    assert t.tag_along == []

    assert t.to_dict() == {"name": "test", "tag_along": []}
