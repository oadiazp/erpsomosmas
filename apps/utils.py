from os import getenv


def get_secret(secret):
    try:
        with open(f'/run/secrets/{secret}', 'r') as f:
            return f.read()
    except:
        return getenv(secret)