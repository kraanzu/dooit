from random import choice
from string import ascii_letters, digits

letters = ascii_letters + digits


def generate_uuid(name: str = ""):
    return name + "".join([choice(letters) for _ in range(20)])
