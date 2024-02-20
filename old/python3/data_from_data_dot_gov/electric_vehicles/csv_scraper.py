#!/usr/bin/python3

# this python script would create a new csv file from the original
# electric_vehicle data to split the data into two for easier access

def csv_spliter() -> None:
    my_file = "Electric_Vehicle_Population_Data.csv"

    file1 = "Electric_Vehicle_Population_Data_1.csv"
    file2 = "Electric_Vehicle_Population_Data_2.csv"

    with open(my_file, "r") as open_file:
        total_lines = sum(1 for line in open_file)
    middle_point_of_file = total_lines // 2
    current_line = 0

    with open(my_file, 'r') as open_my_file, open(file1, 'w') as open_file1, open(file2, 'w') as open_file2:
        for lines in open_my_file:
            if current_line < middle_point_of_file:
                open_file1.write(lines)
            else:
                open_file2.write(lines)
            current_line += 1

    print("DONE")

csv_spliter()
