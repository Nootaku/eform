import hashlib


def encryptPsw(password):
    """Takes a password as string and returns it as a hashed string.

    Arguments:
            - password: string containing a user password

    Output:
            - hash: string containing the hashed password
    """
    # Transform the password into a byte object
    byte = str.encode(password)

    # SHA256 the byte object --> HASH object
    middle = hashlib.sha256(byte)

    # Convert the HASH object into string
    hash = middle.hexdigest()

    return hash


def dectyptPsw(hash):
    """Takes a hashed string and decodes it to a readable password.

    Arguments:
            - hash: a string containing a hashed password

    Output:
            - password: a sting containing a readable password
    """
    # Not needed at the moment of writing
    pass
