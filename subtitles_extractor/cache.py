import hashlib
import pickle
from pathlib import Path


class File:
    __slots__ = ("name", "mtime")

    def __init__(self, path: Path):
        self.name = str(path)
        self.mtime = path.stat().st_mtime_ns

    def __hash__(self):
        return hash((self.name, self.mtime))

    def __eq__(self, other):
        return (self.name, self.mtime) == (other.name, other.mtime)

    def __repr__(self):
        return repr(self.name)


def get_hash(arg, *args) -> str:
    h = hashlib.sha512()
    for a in (arg, *args):
        h.update(str(a).encode())
    return h.hexdigest()


def read_cache(cache_file: Path, p_hash: str):
    try:
        c_hash, cache = pickle.loads(cache_file.read_bytes())
        if p_hash != c_hash:
            raise ValueError
    except (OSError, EOFError, ValueError, pickle.UnpicklingError):
        print("Cache (re)initialized")
        cache = set()
    else:
        print(f"Cache size: {len(cache)}")

    return cache


def write_cache(cache_file: Path, p_hash: str, cache: set[File]):
    print(f"Cache updated: {len(cache)}")
    cache_file.write_bytes(pickle.dumps((p_hash, cache)))
