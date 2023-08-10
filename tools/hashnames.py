import hashlib
import pprint

NAMES = [
    "drgreengiant",
]

if __name__ == "__main__":
    pprint.pprint([hashlib.sha256(name.strip().lower().encode("utf-8")).hexdigest() for name in NAMES])
