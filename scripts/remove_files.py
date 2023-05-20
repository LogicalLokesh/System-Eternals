'''
Part of the System Eternals Suite.

This script tries to remove files from a specified directory based on certain criteria 
such as filename, extension, or starting name.

Author: LogicalLokesh
'''

import argparse
import os
from colorama import init, Fore, Style


def remove_files(target_dir, filename=None, extension=None, start_name=None):
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
    print(Fore.YELLOW +
          f"Found {num_files} file(s) to delete." + Style.RESET_ALL)

    if num_files > 0:
        print(Fore.RED + "Files to delete:")
        for file in files_to_delete:
            print(file)
        print(Style.RESET_ALL)

        # ask the user if they want to delete the files
        confirm = input(
            Fore.YELLOW + "Do you want to continue? (y/n): " + Style.RESET_ALL).lower()
        if confirm != "y":
            print(Fore.GREEN + "Aborted. No files were deleted." + Style.RESET_ALL)
            return

        files_deleted = 0

        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(Fore.GREEN +
                      f"Deleted file: {file_path}" + Style.RESET_ALL)
                files_deleted += 1
            except Exception as e:
                print(
                    Fore.RED + f"Error deleting file: {file_path} - {e}" + Style.RESET_ALL)

        print(Fore.YELLOW +
              f"Total files deleted: {files_deleted}" + Style.RESET_ALL)
    else:
        print(
            Fore.GREEN + "No files found matching the specified criteria." + Style.RESET_ALL)


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
    init()  # Initialize colorama
    main()
