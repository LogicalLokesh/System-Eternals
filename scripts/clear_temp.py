'''
Part of the System Eternals Suite.

This script tries to removes all of the contents from the Windows temporary directory.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
Date: 2023-05-19
'''

import os
import shutil
import tempfile
import platform


def remove_temp_contents():
    """
    This function removes all contents from the temporary directory on a Windows system.
    :return: There is no value being returned. The function only prints output to the console.
    """
    if platform.system() != 'Windows':
        print("This script is designed to run on Windows only.")
        return

    temp_dir = tempfile.gettempdir()

    if not os.path.isdir(temp_dir):
        print(f"Temporary directory not found: {temp_dir}")
        return

    files_deleted = 0
    files_failed = 0

    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
                files_deleted += 1
            except Exception as e:
                print(f"Error removing file: {file_path} - {e}")
                files_failed += 1

    dirs_deleted = 0
    dirs_failed = 0

    for root, dirs, _ in os.walk(temp_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                shutil.rmtree(dir_path)
                print(f"Removed directory: {dir_path}")
                dirs_deleted += 1
            except Exception as e:
                print(f"Error removing directory: {dir_path} - {e}")
                dirs_failed += 1

    print("Temporary directory cleared.")
    print(f"Files deleted: {files_deleted}")
    print(f"Files failed to delete: {files_failed}")
    print(f"Directories deleted: {dirs_deleted}")
    print(f"Directories failed to delete: {dirs_failed}")


remove_temp_contents()


if __name__ == "__main__":
    remove_temp_contents()
