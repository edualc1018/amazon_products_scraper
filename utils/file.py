import os


def check_filename(base_filename) -> str:
    if not os.path.exists(base_filename):
        return base_filename

    filename, extension = os.path.splitext(base_filename)
    counter = 1
    while os.path.exists(f"{filename}_{counter}{extension}"):
        counter += 1
    return f"{filename}_{counter}{extension}"


def get_base_directory():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def insert_before(file_path, new_folder):
    directory, filename = os.path.split(file_path)
    return os.path.join(directory, new_folder, filename)


def create_dir(*args):
    new_dir = os.path.join(*args)
    directory_path = os.path.join(get_base_directory(), new_dir)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def path_join(*args):
    return os.path.join(*args)
