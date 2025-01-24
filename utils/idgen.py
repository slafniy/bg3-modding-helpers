import uuid

def generate_guid() -> str:
    """
    Returns GUID string, examples: 1d7ccc7b-e2ad-48b6-a082-d8cf2b4d149f,
                                   fbc8d6d6-f975-4959-8a75-102cb9c7bf49
    """
    return str(uuid.uuid4())


def generate_handle() -> str:
    """
    Returns bg3 string handle - string starting with 'h' + 36 symbols, examples:
    h325f9b96g0d00g43bcgbc7fg62d56013e9b0
    he64377d7g21f7g4011gb8dag405cab32ff8b
    """
    return f'h{uuid.uuid4()}'.replace('-', 'g')

if __name__ == "__main__":
    print(generate_guid())
    print(generate_handle())