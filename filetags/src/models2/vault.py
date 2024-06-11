from typing import Generator
import json
from filetags.src.models2.node import Node


class Vault:
    def __init__(self, entries: Node):
        self._entries = entries

    def entries(self) -> Generator[tuple[str, list[Node]], None, None]:
        for file in self._entries:
            yield file, file.children


def parse(tag: dict):
    name = tag["name"]
    children = tag["children"]
    child_tags = [parse(t) for t in children]
    return Node(name, child_tags)


if __name__ == "__main__":
    with open("vault2.json") as f:
        data = json.load(f)

    vault = Vault([parse(e) for e in data])

    for file, tags in vault.entries():
        print(file.value, list(map(str, tags)))
