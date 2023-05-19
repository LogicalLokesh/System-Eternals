'''
Part of the System Eternals Suite.

This script tries to removes files from a specified directory based on certain criteria 
such as filename, extension, or starting name.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
Date: 2023-05-19
'''


import argparse
import os


def remove_files(target_dir, filename=None, extension=None, start_name=None):
    """
    This function removes files from a specified directory based on certain criteria such as filename,
    extension, or starting name.

    :param target_dir: The directory where the function will search for files to delete
    :param filename: The name of the file to be deleted. If specified, only files with this exact name
    will be deleted
    :param extension: The file extension to match when searching for files to delete. For example, if
    extension=".txt", the function will search for all files with a ".txt" extension in the target
    directory and its subdirectories
    :param start_name: A string that specifies the starting characters of the file name. If a file's
    name starts with the specified string, it will be added to the list of files to be deleted
    :return: The function does not explicitly return anything, but it may return `None` implicitly if
    the `confirm` variable is not equal to "y".
    """
    if target_dir is None:
        target_dir = os.getcwd()

    files_to_delete = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if (
                (filename is not None and file == filename) or
                (extension is not None and file.endswith(extension)) or
                (start_name is not None and file.startswith(start_name))
            ):
                files_to_delete.append(file_path)

    num_files = len(files_to_delete)
    print(f"Found {num_files} file(s) to delete.")

    if num_files > 0:
        print("Files to delete:")
        for file in files_to_delete:
            print(file)

        # ask the user if they want to delete the files
        confirm = input("Do you want to continue? (y/n): ").lower()
        if confirm != "y":
            print("Aborted. No files were deleted.")
            return

        files_deleted = 0

        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
                files_deleted += 1
            except Exception as e:
                print(f"Error deleting file: {file_path} - {e}")

        print(f"Total files deleted: {files_deleted}")
    else:
        print("No files found matching the specified criteria.")


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Delete files based on criteria')

    # Add the command line arguments
    parser.add_argument('-d', '--directory', help='Target directory')
    parser.add_argument('-f', '--filename', help='Exact filename')
    parser.add_argument('-e', '--extension', help='File extension')
    parser.add_argument('-s', '--startname', help='Start of filename')

    # Parse the arguments
    args = parser.parse_args()

    # Call the remove_files function with the provided arguments
    remove_files(args.directory, args.filename, args.extension, args.startname)


if __name__ == "__main__":
    main()
