import json
from filetags.src.models2.node import Node
from filetags.src.models2.vault import Vault, VaultJSONEncoder


def test_node(nodes: list[Node]):
    [n1, n2, n3, n4, n5, n6, n7, n8] = nodes

    assert n8.__json__() == {"name": 8, "children": []}
    assert n7.__json__() == {"name": 7, "children": [n8]}
    assert n6.__json__() == {"name": 6, "children": [n7]}

    assert n2.__json__() == {"name": 2, "children": [n3, n4]}


def test_vault(vault: Vault):
    result = vault.__json__()
    assert result
    assert isinstance(result, list)
    assert len(result) == 2


def test_encoder(vault: Vault, nodes: list[Node]):
    [n1, n2, n3, n4, n5, n6, n7, n8] = nodes

    value = json.dumps(n2, cls=VaultJSONEncoder)
    assert (
        value
        == '{"name": 2, "children": [{"name": 3, "children": []}, {"name": 4, "children": []}]}'
    )

    # for now, just test that the conversion works
    value = json.dumps(vault, cls=VaultJSONEncoder)
    assert value

    # also check that you can convert back to vault
    new_vault = Vault.from_json(json.loads(value))
    assert new_vault
