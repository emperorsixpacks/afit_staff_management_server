import secrets

def generate_random_password():
    """
    Generate a random password.

    Returns:
        str: The generated random password.
    """
    return secrets.token_hex(16)