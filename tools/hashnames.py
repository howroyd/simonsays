#!./.venv/bin/python3
import hashlib
import pprint

NAMES = [
    #    "drgreengiant",
]

OTHER = [
    "d08ba4bb01a6bb0f41df42a6cca6544df4031b367b27d978ed1f25afac5bdf3b",
    "6c7dae28b93893d307aa39911e2fd4aeb573be00e0eed6e52e4af46c8c1a081c",
    "c09ee3ae3857b990a784a192b4260c9e31f38dc836ccc5fa10f080ddbc375612",
]

if __name__ == "__main__":
    names = set(NAMES)

    blocked = [hashlib.sha256(name.strip().lower().encode("utf-8")).hexdigest() for name in names]

    blocked.extend(OTHER)

    pprint.pprint(blocked)

    with open("blocklist", "w") as f:
        f.write("\n".join(blocked))
