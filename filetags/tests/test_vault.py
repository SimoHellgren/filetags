from filetags.src.models2.vault import Vault


def test_vault(vault: Vault):
    assert vault
    assert vault._entries


def test_entries(vault: Vault):
    filenames = [a.value for a, _ in vault.entries()]
    assert "file1" in filenames
    assert "file2" in filenames


def test_find(vault: Vault):
    # get nodes for setup
    file1, file2 = sorted(vault._entries, key=lambda x: x.value)

    # transpose to get a nice list of files
    (files, _) = zip(*vault.find(["A"]))

    assert file1 in files
    assert file2 not in files

    (files, _) = zip(*vault.find(["b"]))

    assert file1 in files
    assert file2 in files

    (files, _) = zip(*vault.find(["B", "b"]))

    assert file1 not in files
    assert file2 in files

    result = list(vault.find(["XXX"]))

    assert not result

    # test(s) for excluding
    (files, _) = zip(*vault.find(include=["b"], exclude=["B", "b"]))
    assert file1 in files
    assert file2 not in files


def test_rename_tag(vault: Vault):
    # get nodes for setup
    file1, file2 = sorted(vault._entries, key=lambda x: x.value)

    vault.rename_tag("a", "x")

    match = lambda val: lambda x: x.value == val

    # file 1 should match x but not a
    assert not file1.find(match("a"))
    assert file1.find(match("x"))

    # file 2 didn't have a to begin with: should match neither
    assert not file2.find(match("a"))
    assert not file2.find(match("x"))
