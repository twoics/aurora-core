from passlib.handlers.bcrypt import bcrypt


def generate_salt():
    """Generate a random salt for hashing"""

    return bcrypt._generate_salt()  # noqa
