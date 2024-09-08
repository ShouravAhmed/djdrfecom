
import re


def is_vaid_phone_number(phone_no):
    if len(phone_no) < 11 or len(phone_no) == 12 or len(phone_no) > 14:
        return False

    if len(phone_no) == 13 and not phone_no.startswith("88"):
        return False

    if len(phone_no) == 14 and not phone_no.startswith("+88"):
        return False

    if len(phone_no) > 11:
        phone_no = phone_no[-11:]

    valid_prefixes = ["013", "014", "015", "016", "017", "018", "019"]
    if phone_no[:3] not in valid_prefixes:
        return False

    return all((char.isdigit() for char in phone_no[3:]))


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
