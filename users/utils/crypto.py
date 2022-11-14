from passlib.hash import pbkdf2_sha256


def get_hashed_password(password: str):
    return pbkdf2_sha256.hash(password)


def verify_hashed(password: str, hashed_password: str):
    return pbkdf2_sha256.verify(secret=password, hash=hashed_password)
