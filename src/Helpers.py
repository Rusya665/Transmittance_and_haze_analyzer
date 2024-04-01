import os
from typing import Optional, List


def pick_the_last_one(path: str, name: str, extension: Optional[str] = '.txt') -> Optional[str]:
    """
    Find the most recently created file with a given name and extension in a specified path and return its full path.

    :param path: The directory path to search in.
    :param name: Base name to search for in the files.
    :param extension: File extension (default is '.txt').
    :return: The full path of the most recently created matching file, or None if no match is found.
    """
    latest_time = 0
    latest_file = None

    # Check if the provided path is a directory
    if not os.path.isdir(path):
        return None

    # Loop through all files in the specified directory
    for file in os.listdir(path):
        full_file_path = os.path.join(path, file)
        # Check if the file name contains the specified name and has the correct extension
        if name.lower() in file.lower() and file.endswith(extension):
            # Get the creation time of the file
            creation_time = os.path.getctime(full_file_path)
            # Update latest_file if this file is newer
            if creation_time > latest_time:
                latest_time = creation_time
                latest_file = full_file_path

    return latest_file


def find_any_match(path: str, name: str, extension: Optional[str] = '.txt') -> Optional[str]:
    """
    Find any file with a given name and extension in a specified path and return its full path.

    :param path: The directory path to search in.
    :param name: Base name to search for in the files.
    :param extension: File extension (default is '.txt').
    :return: The full path of a matching file, or None if no match is found.
    """
    # Check if the provided path is a directory
    if not os.path.isdir(path):
        return None

    # Loop through all files in the specified directory
    for file in os.listdir(path):
        full_file_path = os.path.join(path, file)
        # Check if the file name contains the specified name and has the correct extension
        if name.lower() in file.lower() and file.endswith(extension):
            # Return the first match
            return full_file_path

    # Return None if no match is found
    return None


def find_all_matches(path: str, name: str, extension: Optional[str] = '.txt') -> List[str]:
    """
    Find all files with a given name and extension in a specified path and return their full paths.

    :param path: The directory path to search in.
    :param name: Base name to search for in the files.
    :param extension: File extension (default is '.txt').
    :return: A list of full paths of matching files, or an empty list if no match is found.
    """
    matches = []

    # Check if the provided path is a directory
    if not os.path.isdir(path):
        return matches

    # Loop through all files in the specified directory
    for file in os.listdir(path):
        full_file_path = os.path.join(path, file)
        # Check if the file name contains the specified name and has the correct extension
        if name.lower() in file.lower() and file.endswith(extension):
            matches.append(full_file_path)

    return matches
