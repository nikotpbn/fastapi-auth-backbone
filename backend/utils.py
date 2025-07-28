import os


def get_secret(key, default):
    value = os.environ.get(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read()
    return value
