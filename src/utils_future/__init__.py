from functools import cached_property
from utils import hashx

def file_hash(file_path) -> str:
    with open(file_path, 'rb') as f:
        file_content = f.read().decode('utf-8', errors='ignore')
        h32 = hashx.md5(file_content)
        return h32