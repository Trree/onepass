from crypto import get_key


def login(password):
    key = get_key(password)
    if key is None:
        return False
    return key




