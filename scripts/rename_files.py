'''
Part of the System Eternals Suite.

This script renames files in a specified directory based on certain criteria such as filename,
extension, start name, and new name.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
Date: 2023-05-19
'''


import argparse
import os


def rename_files(target_dir, filename=None, extension=None, start_name=None, new_name=None):
    """
    This function renames files in a specified directory based on certain criteria such as filename,
    extension, start name, and new name.

    :param target_dir: The directory path where the files to be renamed are located. If None is passed,
    it will use the current working directory
    :param filename: The name of the file to be renamed. If specified, only files with this exact name
    will be considered for renaming
    :param extension: The file extension to match when searching for files to rename. For example, if
    extension=".txt", the function will only consider files with a ".txt" extension for renaming
    :param start_name: The start_name parameter is a string that specifies the starting characters of
    the file name that should be considered for renaming. Only files whose names start with this string
    will be included in the list of files to be renamed
    :param new_name: The new name that will replace the original name of the file(s) being renamed
    :return: The function does not explicitly return anything, but it may print messages to the console.
    """
    if target_dir is None:
        target_dir = os.getcwd()

    files_to_rename = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if (
                (filename is not None and file == filename) or
                (extension is not None and file.endswith(extension)) or
                (start_name is not None and file.startswith(start_name))
            ):
                files_to_rename.append(file_path)

    num_files = len(files_to_rename)
    print(f"Found {num_files} file(s) to rename.")

    if num_files > 0:
        print("Files to rename:")
        for file in files_to_rename:
            print(file)

        confirm = input("Do you want to continue? (y/n): ").lower()
        if confirm != "y":
            print("Aborted. No files were renamed.")
            return

        files_renamed = 0

        for file_path in files_to_rename:
            try:
                dir_name = os.path.dirname(file_path)
                file_ext = os.path.splitext(file_path)[1]
                new_file_name = os.path.join(dir_name, new_name + file_ext)
                os.rename(file_path, new_file_name)
                print(f"Renamed file: {file_path} to {new_file_name}")
                files_renamed += 1
            except Exception as e:
                print(f"Error renaming file: {file_path} - {e}")

        print(f"Total files renamed: {files_renamed}")
    else:
        print("No files found matching the specified criteria.")


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Rename files based on criteria')

    # Add the command line arguments
    parser.add_argument('-d', '--directory', help='Target directory')
    parser.add_argument('-f', '--filename', help='Exact filename')
    parser.add_argument('-e', '--extension', help='File extension')
    parser.add_argument('-s', '--startname', help='Start of filename')
    parser.add_argument('-n', '--newname', required=True, help='New filename')

    # Parse the arguments
    args = parser.parse_args()

    # Call the rename_files function with the provided arguments
    rename_files(args.directory, args.filename,
                 args.extension, args.startname, args.newname)


if __name__ == '__main__':
    main()
