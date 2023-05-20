'''
Part of the System Eternals Suite.

This script renames files in a specified directory based on certain criteria such as filename,
extension, start name, and new name.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
'''

import argparse
import os
from colorama import Fore, Style


def rename_files(target_dir, filename=None, extension=None, start_name=None, new_name=None):
    # Set the target directory to the current directory if not provided
    if target_dir is None:
        target_dir = os.getcwd()

    files_to_rename = []

    # Recursively search for files in the target directory
    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file matches the specified criteria
            if (
                (filename is not None and file == filename) or
                (extension is not None and file.endswith(extension)) or
                (start_name is not None and file.startswith(start_name))
            ):
                files_to_rename.append(file_path)

    num_files = len(files_to_rename)
    print(Fore.YELLOW +
          f"Found {num_files} file(s) to rename." + Style.RESET_ALL)

    if num_files > 0:
        print("Files to rename:")
        for file in files_to_rename:
            print(file)

        confirm = input(
            Fore.YELLOW + "Do you want to continue? (y/n): " + Style.RESET_ALL).lower()
        if confirm != "y":
            print(Fore.YELLOW + "Aborted. No files were renamed." + Style.RESET_ALL)
            return

        files_renamed = 0

        for file_path in files_to_rename:
            try:
                dir_name = os.path.dirname(file_path)
                file_ext = os.path.splitext(file_path)[1]
                new_file_name = os.path.join(dir_name, new_name + file_ext)
                os.rename(file_path, new_file_name)
                print(
                    Fore.GREEN + f"Renamed file: {file_path} to {new_file_name}" + Style.RESET_ALL)
                files_renamed += 1
            except Exception as e:
                print(
                    Fore.RED + f"Error renaming file: {file_path} - {e}" + Style.RESET_ALL)

        print(Fore.YELLOW +
              f"Total files renamed: {files_renamed}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW +
              "No files found matching the specified criteria." + Style.RESET_ALL)


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
