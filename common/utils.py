
import re


def is_valid_password(new_password, confirm_new_password):
    if new_password != confirm_new_password:
        return False
    if (
        len(new_password) < 8
        or not any(char.islower() for char in new_password)
        or not any(char.isupper() for char in new_password)
        or not any(char.isdigit() for char in new_password)
        or not any(char in '~!@#$%^&*-_+=|?' for char in new_password)
    ):
        return False

    return True


def get_slug(text):
    return ' '.join(
        re.sub(r'[^a-z0-9 ]+', '', text.lower()).split()
    ).replace(' ', '-')
