#!/usr/bin/python3

import re


sub_file = input("Enter sub file path: ")
time_d = input("\nEnter time difference\nin this format H:M:S\n(e.g 00:00:35) the difference is 35 seconds,\nit'll adjust the subtitle file by 35 seconds\nbut keep the text time interval >>> ")


def time_to_seconds(time_str):
    """Function to convert a time string (hh:mm:ss,ms) to seconds
    Takes in string format the time like {00:02:59,000}
    Return the current time in seconds
        format >>> (float) 179.059 
    """
    time_str = time_str.replace(',', '.')  # replace , with .
    parts = time_str.split(':')  # split according to the double coulmn
    h, m, s = map(float, parts[0:3])
    ms = float(parts[2]) / 1000
    test = h * 3600 + m * 60 + s + ms
    return h * 3600 + m * 60 + s + ms


def seconds_to_time(seconds):
    """Function to convert seconds to a time string (hh:mm:ss,ms)
    Converts the seconds from time_to_seconds to time format
    Return time format
        format >>> 00:02:59.059
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:06.3f}".format(int(h), int(m), s)


# Open the subtitle file and read the first line to get time difference
with open(sub_file, "r") as op_file:
    line = op_file.readlines()
    if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line[1]):
        sub_time_d = line[1].split('-->')[0]

# Define the time difference (in seconds) between the subtitle and the movie
time_difference = time_to_seconds(f"{sub_time_d}") - time_to_seconds(f"{time_d},000")

# Open the .srt file for reading and create a new .srt file for writing
with open(sub_file, "r") as input_file, open("output_subtitle.srt", "w") as output_file:
    lines = input_file.readlines()
    subtitle_entry = []

    for line in lines:
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            # Extract start and end times and adjust them
            start_time, end_time = map(time_to_seconds,
                            re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', line))
            start_time -= time_difference
            end_time -= time_difference

            # Write the adjusted time range to the output file
            output_file.write("{} --> {}\n".format(seconds_to_time(start_time), seconds_to_time(end_time)))

        elif line.strip() == "":
            # Blank line, indicating the end of a subtitle entry
            output_file.write("\n")
        else:
            # Subtitle text, simply copy to the output file
            output_file.write(line)

print("Subtitle adjustment completed.\n\tHAVE A GREAT DAY!!!")