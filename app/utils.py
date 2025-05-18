import uuid


def generate_uuid_32():
    return str(uuid.uuid4()).replace("-", "")
