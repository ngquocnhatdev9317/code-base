import os


def get_path(path: str):
    full_path = os.path.join(os.getcwd(), ".", path)

    if os.path.exists(full_path):
        return full_path

    return os.path.join(os.getcwd(), "..", path)
