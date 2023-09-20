import secrets
import string


def generate_random_token(length=32):
    # Define the characters that can be used in the token
    characters = string.ascii_letters + string.digits

    # Generate a random token with the specified length
    random_token = "".join(secrets.choice(characters) for _ in range(length))

    return random_token
