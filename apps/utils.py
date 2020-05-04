from os import getenv


def get_secret(secret, default=None):
    try:
        with open(f'/run/secrets/{secret}', 'r') as f:
            return f.read()
    except:
        return default if default else getenv(secret)