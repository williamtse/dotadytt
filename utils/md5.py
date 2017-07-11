import hashlib

def md5(str):
    m = hashlib.md5(str.encode(encoding='utf-8'))
    return m.hexdigest()