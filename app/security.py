import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password using the bcrypt hashing algorithm.

    Encodes the password into UTF-8 bytes, generates a random salt,
    and creates a secure password hash using bcrypt.

    Args:
        plain_password (str): The original plain-text password to hash.

    Returns:
        str: The bcrypt password hash decoded as a UTF-8 string.

    Example:
        hashed = hash_password("admin123")
        print(hashed)
    """
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verify a plain-text password against an existing bcrypt password hash.

    Encodes the provided password and stored hash into UTF-8 bytes,
    then uses bcrypt to check whether the password matches the hash.

    Args:
        plain_password (str): The plain-text password entered by the user.
        password_hash (str): The previously stored bcrypt password hash.

    Returns:
        bool: True if the password matches the stored hash;
              otherwise, False.

    Example:
        hashed = hash_password("admin123")
        is_valid = verify_password("admin123", hashed)
        print(is_valid)  # True
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))