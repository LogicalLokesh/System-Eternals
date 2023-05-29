'''
Part of the System Eternals Suite.

This script finds duplicate files or folders in a specified directory.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
'''

import os
import hashlib
import argparse
from collections import defaultdict
from colorama import Fore, Style, init
from multiprocessing import Pool


def get_file_hash(file_path):
    """
    Calculates the MD5 hash of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: MD5 hash value of the file.
    """
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5()
        while True:
            data = file.read(4096)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()


def process_file(file_path):
    """
    Processes a file by calculating its hash.

    Args:
        file_path (str): Path to the file.

    Returns:
        tuple: File path and its hash.
    """
    file_hash = get_file_hash(file_path)
    return file_path, file_hash


def find_duplicate_files_single(directory):
    """
    Finds duplicate files in a directory and its subdirectories using single-threaded approach.

    Args:
        directory (str): Path to the directory.

    Returns:
        dict: Dictionary with file hash as key and list of duplicate file paths as value.
    """
    file_hashes = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            file_hashes[file_hash].append(file_path)

    duplicate_files = {hash: paths for hash, paths in file_hashes.items() if len(paths) > 1}

    return duplicate_files


def find_duplicate_files_multi(directory):
    """
    Finds duplicate files in a directory and its subdirectories using multiprocessing.

    Args:
        directory (str): Path to the directory.

    Returns:
        dict: Dictionary with file hash as key and list of duplicate file paths as value.
    """
    file_hashes = defaultdict(list)
    file_paths = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    with Pool() as pool:
        results = pool.map(process_file, file_paths)

    for file_path, file_hash in results:
        file_hashes[file_hash].append(file_path)

    duplicate_files = {hash: paths for hash, paths in file_hashes.items() if len(paths) > 1}

    return duplicate_files


def print_colored(text, color):
    """
    Prints colored text to the console.

    Args:
        text (str): Text to print.
        color (str): Colorama color code.
    """
    print(color + text + Style.RESET_ALL)


def print_duplicate_files(duplicate_files):
    """
    Prints the duplicate files with their hash values.

    Args:
        duplicate_files (dict): Dictionary with file hash as key and list of duplicate file paths as value.
    """
    print_colored("Duplicate files:", Fore.YELLOW)
    for hash, paths in duplicate_files.items():
        print_colored(f"Hash: {hash}", Fore.CYAN)
        for path in paths:
            print_colored(f"- {path}", Fore.GREEN)
        print()


def print_no_duplicate_files():
    """
    Prints a message when no duplicate files are found.
    """
    print_colored("No duplicate files found.", Fore.GREEN)


def main(directory, use_multiprocessing=False):
    """
    Main function to find and print duplicate files.

    Args:
        directory (str): Path to the directory.
        use_multiprocessing (bool): Whether to use multiprocessing for finding duplicates.
    """

    print_colored("Starting, please wait...", Fore.GREEN)
    
    if use_multiprocessing:
        
        print_colored("Multiprocessing: ON.", Fore.CYAN)
        duplicate_files = find_duplicate_files_multi(directory)
    else:
        print_colored("Multiprocessing: OFF.", Fore.CYAN)
        duplicate_files = find_duplicate_files_single(directory)

    if duplicate_files:
        print_duplicate_files(duplicate_files)
    else:
        print_no_duplicate_files()


if __name__ == "__main__":
    
    # Initialize Colorama
    init()

    parser = argparse.ArgumentParser(description="Find duplicate files in a directory.")
    parser.add_argument("directory", nargs="?", default=".", help="Path to the directory (default: current directory)")
    parser.add_argument("-m", "--multiprocessing", action="store_true", help="Use multiprocessing")
    args = parser.parse_args()

    main(args.directory, args.multiprocessing)
