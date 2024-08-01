import uuid


def generate_8_digit_uuid():
    # Generate a UUID version 4 (random) and convert it to a string
    uuid_value = str(uuid.uuid4())
    # Remove hyphens from the UUID string
    uuid_value = uuid_value.replace("-", "")
    # Extract the first 8 characters from the UUID string
    uuid_value = uuid_value[:8]
    return uuid_value