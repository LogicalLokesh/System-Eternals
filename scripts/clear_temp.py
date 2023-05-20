'''
Part of the System Eternals Suite.

This script tries to remove all of the contents from the Windows temporary directory.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
'''


import os
import shutil
import tempfile
import platform
from colorama import init, Fore, Style

# Initialize colorama
init()


def get_folder_size(folder_path):
    # Calculate the total size of a folder and its subfolders
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def remove_temp_contents():
    # Check if the script is running on Windows
    if platform.system() != 'Windows':
        print(
            Fore.RED + "This script is designed to run on Windows only." + Style.RESET_ALL)
        return

    # Get the path to the Windows temporary directory
    temp_dir = tempfile.gettempdir()

    # Check if the temporary directory exists
    if not os.path.isdir(temp_dir):
        print(
            Fore.RED + f"Temporary directory not found: {temp_dir}" + Style.RESET_ALL)
        return

    # Get the initial size of the temporary directory
    initial_size = get_folder_size(temp_dir)

    # Initialize counters for deleted and failed files
    files_deleted = 0
    files_failed = 0

    # Walk through the temporary directory and remove files
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Attempt to remove the file
                os.remove(file_path)
                print(Fore.GREEN +
                      f"Removed file: {file_path}" + Style.RESET_ALL)
                files_deleted += 1
            except Exception as e:
                # If there is an error, print the error message in red
                print(
                    Fore.RED + f"Error removing file: {file_path} - {e}" + Style.RESET_ALL)
                files_failed += 1

    # Initialize counters for deleted and failed directories
    dirs_deleted = 0
    dirs_failed = 0

    # Walk through the temporary directory (in reverse) and remove directories
    for root, dirs, _ in os.walk(temp_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                # Attempt to remove the directory and its contents
                shutil.rmtree(dir_path)
                print(Fore.GREEN +
                      f"Removed directory: {dir_path}" + Style.RESET_ALL)
                dirs_deleted += 1
            except Exception as e:
                # If there is an error, print the error message in red
                print(
                    Fore.RED + f"Error removing directory: {dir_path} - {e}" + Style.RESET_ALL)
                dirs_failed += 1

    # Get the final size of the temporary directory
    final_size = get_folder_size(temp_dir)
    space_freed = initial_size - final_size

    # Print summary information
    print("Temporary directory cleared.")
    print(Fore.GREEN + f"Files deleted: {files_deleted}" + Style.RESET_ALL)
    print(
        Fore.RED + f"Files failed to delete: {files_failed}" + Style.RESET_ALL)
    print(Fore.GREEN +
          f"Directories deleted: {dirs_deleted}" + Style.RESET_ALL)
    print(
        Fore.RED + f"Directories failed to delete: {dirs_failed}" + Style.RESET_ALL)
    print(Fore.YELLOW +
          f"Space freed: {space_freed / (1024 * 1024):.2f} MB" + Style.RESET_ALL)


if __name__ == "__main__":
    # Call the function to remove the contents of the Windows temporary directory
    remove_temp_contents()
