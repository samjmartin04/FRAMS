import csv
import time
import os
import math

from GlobalConstants import *

def order_list(list, descending=False):
    if descending:
        m = 0
        while m < len(list)-1:
            n = 0
            while n < len(list)-1-m:
                if list[n] < list[n+1]:
                    temp = list[n+1]
                    list[n+1] = list[n]
                    list[n] = temp
                n += 1
            m += 1
    else:
        m = 0
        while m < len(list)-1:
            n = 0
            while n < len(list)-1-m:
                if list[n] > list[n+1]:
                    temp = list[n+1]
                    list[n+1] = list[n]
                    list[n] = temp
                n += 1
            m += 1
    return list

def order_list_insert(list):
    if len(list) == 2:
        if list[1] < list[0]:
            return [list[1], list[0]]
        else:
            return list
    else:
        n = 1
        while n < len(list):
            m = 0
            while m < n:
                if list[n-m] < list[n-m-1]:
                    temp = list[n-m]
                    list[n-m] = list[n-m-1]
                    list[n-m-1] = temp
                else:
                    break
                m += 1
            n += 1
        return list

def order_array_list(array_list, index, descending=False):
    if descending:
        m = 0
        while m < len(array_list)-1:
            n = 0
            while n < len(array_list)-1-m:
                if array_list[n][index] < array_list[n+1][index]:
                    temp = array_list[n+1]
                    array_list[n+1] = array_list[n]
                    array_list[n] = temp
                n += 1
            m += 1
    else:
        m = 0
        while m < len(array_list)-1:
            n = 0
            while n < len(array_list)-1-m:
                if array_list[n][index] > array_list[n+1][index]:
                    temp = array_list[n+1]
                    array_list[n+1] = array_list[n]
                    array_list[n] = temp
                n += 1
            m += 1
    return array_list

def remove_league_blocks_from_schedule(match_schedule):
    new_schedule = []
    for league_block in match_schedule:
        for match in league_block:
            new_schedule.append(match)
    return new_schedule

def check_location(location):
    count = 1
    while count < 5:
        if location[-count] == ".":
            break
        else:
            count += 1
    if count == 5:
        return location
    else:
        pos = len(location) - count
        file_type = location[pos+1:]
        name = location[:pos]
        if os.path.isfile(location):
            n = 2
            while n < 99:
                new_location = f"{name}_{n}.{file_type}"
                if os.path.isfile(new_location):
                    n += 1
                else:
                    return new_location
        return location

def get_current_time(seconds=True):
    ct = time.localtime()
    if seconds:
        return f"{ct.tm_hour:02d}:{ct.tm_min:02d}:{ct.tm_sec:02d}"
    else:
        return f"{ct.tm_hour:02d}:{ct.tm_min:02d}"

def import_schedule(file_location, league_block_size=0):
    file_schedule = csv.reader(open(file_location, 'r'))
    output = []
    match_schedule = []
    for row in file_schedule:
        match = row[0].split("|")
        new_row = []
        for team_num in match:
            new_row.append(int(team_num))
        match_schedule.append(new_row)
    if league_block_size == 0:
        output = match_schedule
    else:
        league_block = []
        n = 0
        while n < len(match_schedule):
            if n > 0 and n%league_block_size == 0:
                output.append(league_block)
                league_block = []
            league_block.append(match_schedule[n])
            n += 1
        output.append(league_block)
    return output

def export_schedule_to_txt(match_schedule, file_location, in_blocks=False):
    if in_blocks:
        export_text = ""
        for league_block in match_schedule:
            for match in league_block:
                export_text += f"{match[0]}|{match[1]}|{match[2]}|{match[3]}\n"
        export_text = export_text[:-1]
        f = open(file_location, "w")
        f.write(export_text)
        f.close()
    else:
        export_text = ""
        for match in match_schedule:
            export_text += f"{match[0]}|{match[1]}|{match[2]}|{match[3]}\n"
        export_text = export_text[:-1]
        f = open(file_location, "w")
        f.write(export_text)
        f.close()


def get_list_of_team_numbers(number_of_teams):
    list_of_team_numbers = []
    for n in range(number_of_teams):
        list_of_team_numbers.append(n+1)
    return list_of_team_numbers

def get_number_of_teams_from_schedule(match_schedule, in_blocks=False):
    test_number = 1
    searching = True
    if in_blocks:
        while searching == True:
            found = False
            for league_block in match_schedule:
                for match in league_block:
                    if test_number in match:
                        found = True
                        break
            if found:
                test_number += 1
            else:
                searching = False
                test_number -= 1
    else:
        while searching == True:
            found = False
            for match in match_schedule:
                if test_number in match:
                    found = True
                    break
            if found:
                test_number += 1
            else:
                searching = False
                test_number -= 1
    return test_number

def get_list_of_team_numbers_from_schedule(match_schedule, in_blocks=False):
    return get_list_of_team_numbers(get_number_of_teams_from_schedule(match_schedule, in_blocks))

def get_appearances_from_schedule(match_schedule, in_blocks=False):
    number_of_teams = get_number_of_teams_from_schedule(match_schedule, in_blocks)
    list_of_team_numbers = get_list_of_team_numbers(number_of_teams)
    appearances_list = []
    for n in list_of_team_numbers:
        appearances_list.append(0)
    
    if in_blocks:
        for team_number in list_of_team_numbers:
            for league_block in match_schedule:
                for match in league_block:
                    if team_number in match:
                        appearances_list[team_number-1] += 1
    else:
        for team_number in list_of_team_numbers:
            for match in match_schedule:
                if team_number in match:
                    appearances_list[team_number-1] += 1
    
    appearances_dict = {}

    for appearances_for_team in appearances_list:
        if appearances_for_team in appearances_dict.keys():
            appearances_dict[appearances_for_team] += 1
        else:
            appearances_dict[appearances_for_team] = 1

    for key in appearances_dict.keys():
        if appearances_dict[key] > int(math.ceil(number_of_teams/2)):
            return key
    # Less than half the teams have the same number of appearances, uses mean instead:
    sum = 0
    for count in appearances_list:
        sum += count

    average = sum/number_of_teams
    return int(round(average,0))

def get_number_of_teams_per_match_from_schedule(match_schedule, in_blocks=False):
    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                return len(match)
    else:
        for match in match_schedule:
            return len(match)

def colour_text(text, colour):
    if colour is None:
        return text
    colour = colour.casefold()
    if not COLOURED_TEXT:
        return text
    if colour == "nothing":
        return text
    elif colour == "black":
        colour_info = "\033[38;5;0m\033[48;5;15m"
    elif colour == "blue":
        colour_info = "\033[38;5;25m"
    elif colour == "red":
        colour_info = "\033[38;5;196m"
    elif colour == "green":
        colour_info = "\033[38;5;46m"
    elif colour == "dark green":
        colour_info = "\033[38;5;35m"
    elif colour == "brown":
        colour_info = "\033[38;5;94m"
    elif colour == "turquoise":
        colour_info = "\033[38;5;51m"
    elif colour == "pink":
        colour_info = "\033[38;5;200m"
    elif colour == "purple":
        colour_info = "\033[38;5;214m"
    elif colour == "orange":
        colour_info = "\033[38;5;214m"
    elif colour == "lilac":
        colour_info = "\033[38;5;177m"
    elif colour == "aqua":
        colour_info = "\033[38;5;120m"
    elif colour == "grey":
        colour_info = "\033[38;5;244m"
    elif colour == "yellow":
        colour_info = "\033[38;5;226m"
    elif colour == "italics":
        colour_info = "\033[48;5;240m"
    elif colour == "white":
        colour_info = "\033[48;5;0m\033[38;5;15m"
    elif colour == "bold":
        colour_info = "\033[01m"
    else:
        colour_info = colour
    # else:
    #     colour_info = "\033[48;5;196m"
    return f"{colour_info}{text}\u001b[0m"

def get_team_list_text_when_number_matches(info_array, number_to_match_with):
    """
    Takes an array with info in it (ordered such that index 0 is team 1) and returns a list with every team number that matches the number_to_match_with value
    """
    team_list_text = " ("
    for m, spacing in enumerate(info_array):
        if spacing == number_to_match_with:
            team_list_text += f"{m+1}, "
    
    team_list_text = team_list_text[:-2]
    team_list_text += ")"
    return team_list_text

def get_team_list_text_when_number_matches_dict(info_dict, number_to_match_with):
    """
    Takes an array with info in it (ordered such that index 0 is team 1) and returns a list with every team number that matches the number_to_match_with value
    """
    team_list_text = " ("
    for m, spacing in info_dict.items():
        if spacing == number_to_match_with:
            team_list_text += f"{m}, "
    
    team_list_text = team_list_text[:-2]
    team_list_text += ")"
    return team_list_text

def tidy_list_of_team_numbers(info_array):
    """
    Takes an array in [] form and convert it into () form.
    """
    team_list_text = " ("
    for team_number in info_array:
        team_list_text += f"{team_number}, "
    
    team_list_text = team_list_text[:-2]
    team_list_text += ")"
    return team_list_text

def get_team_numbers_not_in_list(list_of_team_numbers, list_to_exclude):
    output_array = []
    for team_number in list_of_team_numbers:
        if not team_number in list_to_exclude:
            output_array.append(team_number)
    return output_array

def number_array_from_list(list):
    try:
        list = list.replace(" ", "")
        pos1 = list.find(",")
        array = []
        if pos1 == -1:
            if not len(list) == 0:
                try:
                    num = list
                    array.append(num)
                except:
                    pass
        else:
            try:
                array.append(list[:pos1])
            except:
                pass
        while not pos1 == -1:
            pos2 = list[pos1+1:].find(",")
            if pos2 == -1:
                pos2 = len(list)
            else:
                pos2 += pos1+1
            try:
                num = list[pos1+1:pos2]
                array.append(num)
            except:
                pass
            list = list[pos1+1:]
            pos1 = list.find(",")

        new_array = []
        for item in array:
            pos = str(item).find("-")
            if pos == -1:
                new_array.append(int(item))
            else:
                first_num = int(str(item)[:pos])
                second_num = int(str(item)[pos+1:])
                n = first_num
                while n <= second_num:
                    new_array.append(n)
                    n += 1
        return new_array
    except Exception as e:
        print(f"\nERROR PROCESSING LIST ENTERED: {e}")
        return []