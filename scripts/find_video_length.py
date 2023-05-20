'''
Part of the System Eternals Suite.

This script calculates the total runtime of all video files in a specified directory
and its subdirectories. It can also display file names, runtime, and size if requested.

Copyright (c) LogicalLokesh. All rights reserved.
Author: LogicalLokesh
'''

import os
import sys
import concurrent.futures
from colorama import init, Fore, Style
from moviepy.editor import VideoFileClip


# Initialize colorama
init()


def get_video_duration(filepath):
    '''
    Retrieves the duration of a video file using moviepy.

    Args:
        filepath (str): Path to the video file.

    Returns:
        float: Duration of the video in seconds.
    '''
    try:
        clip = VideoFileClip(filepath)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0.0


def get_video_size(filepath):
    '''
    Retrieves the size of a video file.

    Args:
        filepath (str): Path to the video file.

    Returns:
        int: Size of the video in bytes.
    '''
    return os.path.getsize(filepath)


def format_time(seconds):
    '''
    Formats the time duration in hours, minutes, and seconds.

    Args:
        seconds (float): Time duration in seconds.

    Returns:
        str: Formatted time string.
    '''
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"


def format_size(bytes):
    '''
    Formats the size in megabytes.

    Args:
        bytes (int): Size in bytes.

    Returns:
        str: Formatted size string.
    '''
    megabytes = bytes / (1024 * 1024)
    return f"{megabytes:.2f} MB"


def process_video_file(filepath):
    '''
    Processes a video file and returns its duration and size.

    Args:
        filepath (str): Path to the video file.

    Returns:
        tuple: Duration and size of the video file.
    '''
    duration = get_video_duration(filepath)
    size = get_video_size(filepath)
    return duration, size


def get_total_runtime(directory, display_files=False):
    '''
    Calculates the total runtime of all video files in the specified directory and its subdirectories.
    Optionally, displays file names, runtime, and size.

    Args:
        directory (str): Path to the video directory.
        display_files (bool): Whether to display file names, runtime, and size.

    Returns:
        tuple: Total runtime of all videos in (seconds, minutes, hours, days).
    '''
    total_runtime = 0
    total_videos = 0

    if display_files:
        print("File Name".ljust(60), "Runtime".ljust(15), "Size".ljust(15))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(process_video_file, os.path.join(root, file)): os.path.join(root, file)
            for root, _, files in os.walk(directory)
            for file in files
            if file.endswith(('.mp4', '.avi', '.mkv'))
        }

        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                duration, size = future.result()
                total_runtime += duration
                if display_files:
                    print(file.ljust(60), format_time(duration).ljust(
                        15), format_size(size).ljust(15))
                total_videos += 1
            except Exception as e:
                print(f"Error processing video file '{file}': {e}")

    seconds = total_runtime
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    return seconds, minutes % 60, hours % 24, days, total_videos


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            Fore.RED + "Usage: python script.py <directory> [--files]" + Style.RESET_ALL)
        sys.exit(1)

    directory_path = sys.argv[1]
    display_files = False

    if len(sys.argv) >= 3 and sys.argv[2] == "--files":
        display_files = True

    total_seconds, remaining_minutes, remaining_hours, remaining_days, total_videos = get_total_runtime(
        directory_path, display_files)

    if display_files:
        print("\n")

    print(Fore.GREEN + "Total number of videos:" + Style.RESET_ALL, total_videos)
    print(Fore.GREEN + "Total runtime of all videos:" + Style.RESET_ALL,
          f"{total_seconds:.2f} seconds OR" + Fore.BLUE +
          f"  {remaining_days} days, {remaining_hours} hours, {remaining_minutes} minutes.")
