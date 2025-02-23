import copy
import time
import math
import argparse
import statistics
from collections import Counter

from GlobalConstants import *
from GeneralFunctions import *

def get_spacing_data(match_schedule, specific_team_number, in_blocks=False):
    number_of_teams = get_number_of_teams_from_schedule(match_schedule, in_blocks)

    #get_match_spacing()
    present_match_numbers = []
    counter = 0
    half_counter = 0
    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                if specific_team_number in match:
                    present_match_numbers.append(counter)
                half_counter += 1
                if half_counter == NUMBER_OF_ARENAS:
                    counter += 1
                    half_counter = 0
    else:
        for match in match_schedule:
            if specific_team_number in match:
                present_match_numbers.append(counter)
            half_counter += 1
            if half_counter == NUMBER_OF_ARENAS:
                counter += 1
                half_counter = 0

    #analyse_match_spacing()
    spacings_data = []
    n = 0
    while n < len(present_match_numbers)-1:
        spacings_data.append(present_match_numbers[n+1]-present_match_numbers[n]-1)
        n += 1
    
    return spacings_data

def min_value_from_list(list):
    min_value = list[0]
    for value in list:
        if value < min_value:
            min_value = value
    return min_value

def min_value_from_dict(dict):
    min_value = dict[next(iter(dict))]
    for value in dict.values():
        if value < min_value:
            min_value = value
    return min_value

def max_value_from_list(list):
    max_value = list[0]
    for value in list:
        if value > max_value:
            max_value = value
    return max_value

def max_value_from_dict(dict):
    max_value = dict[next(iter(dict))]
    for value in dict.values():
        if value > max_value:
            max_value = value
    return max_value

def av_value_from_list(list):
    sum = 0
    for value in list:
        sum += value
    return sum/len(list)

def av_value_from_dict(dict):
    sum = 0
    for value in dict.values():
        sum += value
    return sum/len(dict.keys())

def spacing_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    number_of_teams = get_number_of_teams_from_schedule(match_schedule)-len(exclude_teams_list)
    output_text = "\n## Spacings\n"
    output_text += "\n#### This looks at the spacing between matches for each team."
    if INCREMENT_SPACING_CHECK:
        output_text += "\n#### Spacing is given as the difference between the two match numbers. E.g. a spacing of 4 is (on, off, off, off, on).\n"
    else:
        output_text += "\n#### Spacing is given as the gap between two matches. E.g. a spacing of 3 is (on, off, off, off, on).\n"
    min_spacings_list = {}
    av_spacings_list = {}
    max_spacings_list = {}
    spacings_data_all = {}
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)
    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    for team_number in list_of_team_numbers:
        if not team_number in exclude_teams_list:
            spacings_data = get_spacing_data(match_schedule, team_number)
            if INCREMENT_SPACING_CHECK:
                n = 0
                while n < len(spacings_data):
                    spacings_data[n] += 1
                    n += 1
            spacings_data_all[team_number] = spacings_data
            min_spacings_list[team_number] = min_value_from_list(spacings_data)
            max_spacings_list[team_number] = max_value_from_list(spacings_data)
            av_spacings_list[team_number] = round(av_value_from_list(spacings_data), 2)
            # min_spacings_list.append(min_value_from_list(spacings_data))
            # max_spacings_list.append(max_value_from_list(spacings_data))
            # av_spacings_list.append(round(av_value_from_list(spacings_data), 2))
    
    strong_alert_level_low = 0
    medium_alert_level_low = 1
    weak_alert_level_low = 2
    target_spacing = number_of_teams/number_of_teams_per_match - 1
    weak_alert_level_high = target_spacing*2+1
    medium_alert_level_high = target_spacing*3
    weak_alert_level_high_count = 0
    medium_alert_level_high_count = 0
    strong_alert_low_text, medium_alert_low_text, weak_alert_low_text = "", "", ""
    if INCREMENT_SPACING_CHECK:
        strong_alert_level += 1
        medium_alert_level += 1
        weak_alert_level += 1
        weak_alert_level_high += 1
        medium_alert_level_high += 1

    min_spacing_summary_list = []
    max_spacing_summary_list = []
    av_spacing_summary_list = []

    min_spacing_summary_list.append(min_value_from_dict(min_spacings_list))
    min_spacing_summary_list.append(av_value_from_dict(min_spacings_list))
    min_spacing_summary_list.append(max_value_from_dict(min_spacings_list))
    max_spacing_summary_list.append(min_value_from_dict(max_spacings_list))
    max_spacing_summary_list.append(av_value_from_dict(max_spacings_list))
    max_spacing_summary_list.append(max_value_from_dict(max_spacings_list))
    av_spacing_summary_list.append(min_value_from_dict(av_spacings_list))
    av_spacing_summary_list.append(av_value_from_dict(av_spacings_list))
    av_spacing_summary_list.append(max_value_from_dict(av_spacings_list))

    top_line_text = "                       min    av     max"
    min_spacing_output_text = f"  Minimum Spacings:   {min_spacing_summary_list[0]:4.1f}   {min_spacing_summary_list[1]:4.1f}   {min_spacing_summary_list[2]:4.1f}"
    av_spacing_output_text =  f"  Average Spacings:   {av_spacing_summary_list[0]:4.1f}   {av_spacing_summary_list[1]:4.1f}   {av_spacing_summary_list[2]:4.1f}"
    max_spacing_output_text = f"  Maximum Spacings:   {max_spacing_summary_list[0]:4.1f}   {max_spacing_summary_list[1]:4.1f}   {max_spacing_summary_list[2]:4.1f}"

    output_text += f"\n{top_line_text}\n{min_spacing_output_text}\n{av_spacing_output_text}\n{max_spacing_output_text}\n"

    min_spacings_count_list = []
    min_spacing_list_totals = Counter(min_spacings_list.values())
    total = 0
    n = 0
    while n < 99:
        number_of_n = min_spacing_list_totals[n]
        min_spacings_count_list.append(number_of_n)
        total += number_of_n
        if total == number_of_teams:
            break
        n += 1
    
    max_spacings_count_list = []
    ax_spacing_list_totals = Counter(max_spacings_list.values())
    total = 0
    n = 0
    while n < 99:
        number_of_n = ax_spacing_list_totals[n]
        max_spacings_count_list.append(number_of_n)
        total += number_of_n
        if total == number_of_teams:
            break
        n += 1
    
    min_spacings_count_text = "Number of teams with each minimum spacing:\n"

    n = 0
    while n < len(min_spacings_count_list):
        if min_spacings_count_list[n] > 0:
            text_to_add = f"  Min spacing of {n:>2}: {min_spacings_count_list[n]:>3} teams"
            if n == strong_alert_level_low:
                colour_for_text = "red"
                text = f"{min_spacings_count_list[n]:>3} teams have a minimum spacing of {strong_alert_level_low}."
                strong_alert_low_text = f"{colour_text(text, 'red')} This spacing is impossible for a physical competition as it would result in consecutive matches (on, on)."
                add_team_numbers = True
                summary_of_checks[0].append(["minimum spacing", strong_alert_low_text])
            elif n == medium_alert_level_low:
                colour_for_text = "orange"
                text = f"{min_spacings_count_list[n]:>3} teams have a minimum spacing of {medium_alert_level_low}."
                medium_alert_low_text = f"{colour_text(text, 'orange')} This spacing is very tight for a physical competition as it would result in almost consecutive matches (on, off, on)."
                add_team_numbers = True
                summary_of_checks[1].append(["minimum spacing", medium_alert_low_text])
            elif n == weak_alert_level_low:
                colour_for_text = "yellow"
                text = f"{min_spacings_count_list[n]:>3} teams have a minimum spacing of {weak_alert_level_low}."
                weak_alert_low_text = f"{colour_text(text, 'yellow')} This spacing is a bit close for a physical competition, but still very usable (on, off, off, on)."
                add_team_numbers = True
                summary_of_checks[2].append(["minimum spacing", weak_alert_low_text])
            else:
                colour_for_text = None
                add_team_numbers = False
            
            if add_team_numbers:
                team_list = get_team_list_when_number_matches_dict(min_spacings_list, n)
                team_list_text = tidy_list_of_team_numbers_text(team_list, number_of_teams, exclude_teams_list)
            else:
                team_list_text = ""
            min_spacings_count_text += f"{colour_text(text_to_add, colour_for_text)}{team_list_text}\n"
        n += 1
    
    min_spacings_count_text = min_spacings_count_text[:-1]

    output_text = f"{output_text}\n{min_spacings_count_text}\n"

    max_spacings_count_text = "Number of teams with each maximum spacing:\n"

    n = 0
    while n < len(max_spacings_count_list):
        if max_spacings_count_list[n] > 0:
            text_to_add = f"  Max spacing of {n:>2}: {max_spacings_count_list[n]:>3} teams"
            if n > medium_alert_level_high:
                colour_for_text = "orange"
                medium_alert_level_high_count += max_spacings_count_list[n]
                add_team_numbers = True
            elif n > weak_alert_level_high:
                colour_for_text = "yellow"
                weak_alert_level_high_count += max_spacings_count_list[n]
                add_team_numbers = True
            else:
                colour_for_text = None
                add_team_numbers = False

            if add_team_numbers:
                team_list = get_team_list_when_number_matches_dict(max_spacings_list, n)
                team_list_text = tidy_list_of_team_numbers_text(team_list, number_of_teams, exclude_teams_list)
            else:
                team_list_text = ""
            max_spacings_count_text += f"{colour_text(text_to_add, colour_for_text)}{team_list_text}\n"
        n += 1

    max_spacings_count_text = max_spacings_count_text[:-1]

    output_text = f"{output_text}\n{max_spacings_count_text}\n"

    if strong_alert_low_text != "":
        output_text += f"\n{strong_alert_low_text}"
        output_text += "\n"
    if medium_alert_low_text != "":
        output_text += f"\n{medium_alert_low_text}"
        output_text += "\n"
    if weak_alert_low_text != "":
        output_text += f"\n{weak_alert_low_text}"
        output_text += "\n"

    if medium_alert_level_high_count > 0:
        text = f"{medium_alert_level_high_count:>3} teams have a maximum spacing larger than {math.floor(medium_alert_level_high):>2}."
        medium_alert_level_high_text = f"{colour_text(text, 'orange')} This spacing is very large for a competition."
        summary_of_checks[1].append(["maximum spacing", medium_alert_level_high_text])
        output_text += f"\n{medium_alert_level_high_text}"
        output_text += "\n"

    if weak_alert_level_high_count > 0:
        text = f"{weak_alert_level_high_count+medium_alert_level_high_count:>3} teams have a maximum spacing larger than {math.floor(weak_alert_level_high):>2}."
        weak_alert_level_high_text = f"{colour_text(text, 'yellow')} This spacing is quite large for a competition, but still very usable."
        summary_of_checks[2].append(["maximum spacing", weak_alert_level_high_text])
        output_text += f"\n{weak_alert_level_high_text}"
        output_text += "\n"

    output_text += "\n"
    
    if detailed:
        separated = False
        if separated:
            #Minimum stuff:     [team_num, min_spacing, count]
            output_text += "\n  Team    Min   Count"
            min_spacing_detailed_list = []
            for n, spacings_data in spacings_data_all.items():
                min_spacing = min_spacings_list[n]
                spacing_count = spacings_data.count(min_spacing)
                add_array = [n+1, min_spacing, spacing_count, 100*min_spacing-spacing_count]
                min_spacing_detailed_list.append(add_array)
            min_spacing_detailed_list = order_array_list(min_spacing_detailed_list, 3)
            for row in min_spacing_detailed_list:
                text_to_add = f"\n  {row[0]:>3}     {row[1]:>2}     {row[2]:>2}"
                if row[1] == strong_alert_level_low:
                    colour = "red"
                elif row[1] == medium_alert_level_low:
                    colour = "orange"
                elif row[1] == weak_alert_level_low:
                    colour = "yellow"
                else:
                    colour = None
                output_text += colour_text(text_to_add, colour)
            output_text += "\n"
            
            #Average stuff:     [team_num, average_spacing]
            output_text += "\n  Team     Av"
            closest_to_target = 999999
            n = 0
            while n < len(av_spacings_list):
                if abs(target_spacing-av_spacings_list[n]) < closest_to_target:
                    closest_to_target = abs(target_spacing-av_spacings_list[n])
                n += 1
            closest_to_target = round(closest_to_target, 2)
            av_spacing_detailed_list = []
            for n, spacings_data in spacings_data_all.items():
                av_spacing = av_value_from_list(spacings_data)
                add_array = [n+1, round(av_spacing,5)]
                av_spacing_detailed_list.append(add_array)
            av_spacing_detailed_list = order_array_list(av_spacing_detailed_list, 1, False)
            for row in av_spacing_detailed_list:
                text_to_add = f"\n  {row[0]:>3}     {row[1]:3.1f}"
                if round(abs(target_spacing-round(row[1],2)),2) == closest_to_target:
                    colour = "dark green"
                else:
                    colour = None
                output_text += colour_text(text_to_add, colour)
            output_text += "\n"

            #Maximum stuff:     [team_num, max_spacing, count]
            output_text += "\n  Team    Max   Count"
            max_spacing_detailed_list = []
            for n, spacings_data in spacings_data_all.items():
                max_spacing = max_spacings_list[n]
                spacing_count = spacings_data.count(max_spacing)
                add_array = [n+1, max_spacing, spacing_count, 100*max_spacing+spacing_count]
                max_spacing_detailed_list.append(add_array)
            max_spacing_detailed_list = order_array_list(max_spacing_detailed_list, 3, True)
            for row in max_spacing_detailed_list:
                text_to_add = f"\n  {row[0]:>3}     {row[1]:>2}     {row[2]:>2}"
                if row[1] > medium_alert_level_high:
                    colour = "orange"
                elif row[1] > weak_alert_level_high:
                    colour = "yellow"
                else:
                    colour = None
                output_text += colour_text(text_to_add, colour)
            output_text += "\n"

            #Spacing stuff:     [team_num, list_of_spacings]
            output_text += "\n  Team   Spacings"
            for n, spacings_data in enumerate(spacings_data_all):
                text_to_add = f"\n  {n+1:>3}    "
                for spacing in spacings_data:
                    text_to_add += f"{spacing:>2}, "
                text_to_add = text_to_add[:-2]
                output_text += text_to_add
        else:
            #Minimum stuff:     [team_num, min_spacing, count]
            min_spacing_detailed_list = []
            for n, spacings_data in spacings_data_all.items():
                min_spacing = min_spacings_list[n]
                spacing_count = spacings_data.count(min_spacing)
                add_array = [n, min_spacing, spacing_count, 100*min_spacing-spacing_count]
                min_spacing_detailed_list.append(add_array)
            min_spacing_detailed_list_sorted_by_team = min_spacing_detailed_list.copy()
            min_spacing_detailed_list = order_array_list(min_spacing_detailed_list.copy(), 3)

            #Average stuff:     [team_num, average_spacing]
            closest_to_target = 999999
            for value in av_spacings_list.values():
                if abs(target_spacing-value) < closest_to_target:
                    closest_to_target = abs(target_spacing-value)
            closest_to_target = round(closest_to_target, 2)
            av_spacing_detailed_list = []
            for n, spacings_data in spacings_data_all.items():
                av_spacing = av_value_from_list(spacings_data)
                add_array = [n, round(av_spacing,5)]
                av_spacing_detailed_list.append(add_array)
            av_spacing_detailed_list_sorted_by_team = av_spacing_detailed_list.copy()
            av_spacing_detailed_list = order_array_list(av_spacing_detailed_list.copy(), 1, False)

            #Maximum stuff:     [team_num, max_spacing, count]
            max_spacing_detailed_list = []
            for n, spacings_data in spacings_data_all.items():
                max_spacing = max_spacings_list[n]
                spacing_count = spacings_data.count(max_spacing)
                add_array = [n, max_spacing, spacing_count, 100*max_spacing+spacing_count]
                max_spacing_detailed_list.append(add_array)
            max_spacing_detailed_list_sorted_by_team = max_spacing_detailed_list.copy()
            max_spacing_detailed_list = order_array_list(max_spacing_detailed_list.copy(), 3, True)


            gap_between_sections =       "            "

            min_spacing_text_top_row = f"{colour_text('Team','blue')}    Min   Count"
            av_spacing_text_top_row = f"{colour_text('Team','blue')}     Av"
            max_spacing_text_top_row = f"{colour_text('Team','blue')}    Max   Count"
            output_text += f"\n  {min_spacing_text_top_row}          {av_spacing_text_top_row}            {max_spacing_text_top_row}"

            for n, row in enumerate(min_spacing_detailed_list):
                min_spacing_team_num = min_spacing_detailed_list[n][0]
                min_spacing = min_spacing_detailed_list[n][1]
                min_spacing_count = min_spacing_detailed_list[n][2]
                if min_spacing == strong_alert_level_low:
                    colour = "red"
                elif min_spacing == medium_alert_level_low:
                    colour = "orange"
                elif min_spacing == weak_alert_level_low:
                    colour = "yellow"
                else:
                    colour = None
                min_spacing_team_num = colour_text(f"{min_spacing_team_num:>3}",'blue')
                min_spacing = colour_text(f"{min_spacing:>2}",colour)
                min_spacing_count = f"{min_spacing_count:>2}"
                min_spacing_text = f"{min_spacing_team_num}     {min_spacing}     {min_spacing_count}"

                av_spacing_team_num = av_spacing_detailed_list[n][0]
                av_spacing = av_spacing_detailed_list[n][1]
                if round(abs(target_spacing-round(av_spacing,2)),2) == closest_to_target:
                    colour = "dark green"
                else:
                    colour = None
                av_spacing_team_num = colour_text(f"{av_spacing_team_num:>3}",'blue')
                av_spacing = colour_text(f"{av_spacing:3.1f}",colour)
                av_spacing_text = f"{av_spacing_team_num}     {av_spacing}"

                max_spacing_team_num = max_spacing_detailed_list[n][0]
                max_spacing = max_spacing_detailed_list[n][1]
                max_spacing_count = max_spacing_detailed_list[n][2]

                if max_spacing > medium_alert_level_high:
                    colour = "orange"
                elif max_spacing > weak_alert_level_high:
                    colour = "yellow"
                else:
                    colour = None
                max_spacing_team_num = colour_text(f"{max_spacing_team_num:>3}",'blue')
                max_spacing = colour_text(f"{max_spacing:>2}",colour)
                max_spacing_count = f"{max_spacing_count:>2}"
                max_spacing_text = f"{max_spacing_team_num}     {max_spacing}     {max_spacing_count}"

                text_to_add = f"\n  {min_spacing_text}{gap_between_sections}{av_spacing_text}{gap_between_sections}{max_spacing_text}"
                output_text += text_to_add
            
            output_text += "\n"
            
            gap_between_sections =       "        "

            # output_text += f"\n  {colour_text('Team','blue')}        Min   Count         Av          Max   Count"
            output_text += f"\n  {colour_text('Team','blue')}       Min            Av         Max           Spacings"   #For when count is in brackets.

            for n, row in enumerate(min_spacing_detailed_list_sorted_by_team):
                team_number = min_spacing_detailed_list_sorted_by_team[n][0]
                min_spacing = min_spacing_detailed_list_sorted_by_team[n][1]
                min_spacing_count = min_spacing_detailed_list_sorted_by_team[n][2]
                if min_spacing == strong_alert_level_low:
                    colour = "red"
                elif min_spacing == medium_alert_level_low:
                    colour = "orange"
                elif min_spacing == weak_alert_level_low:
                    colour = "yellow"
                else:
                    colour = None
                min_spacing = colour_text(f"{min_spacing:>2}",colour)
                min_spacing_count = f"({min_spacing_count})"
                min_spacing_text = f"{min_spacing}     {min_spacing_count}"
                min_spacing_text = f"{min_spacing} {min_spacing_count:>4}"         #For when count is in brackets

                av_spacing = av_spacing_detailed_list_sorted_by_team[n][1]
                if round(abs(target_spacing-round(av_spacing,2)),2) == closest_to_target:
                    colour = "dark green"
                else:
                    colour = None
                av_spacing = colour_text(f"{av_spacing:3.1f}",colour)
                av_spacing_text = f"{av_spacing}"

                max_spacing = max_spacing_detailed_list_sorted_by_team[n][1]
                max_spacing_count = max_spacing_detailed_list_sorted_by_team[n][2]

                if max_spacing > medium_alert_level_high:
                    colour = "orange"
                elif max_spacing > weak_alert_level_high:
                    colour = "yellow"
                else:
                    colour = None
                max_spacing = colour_text(f"{max_spacing:>2}",colour)
                max_spacing_count = f"({max_spacing_count})"
                max_spacing_text = f"{max_spacing}     {max_spacing_count}"
                max_spacing_text = f"{max_spacing} {max_spacing_count:>4}"     #For when count is in brackets


                spacings_data = spacings_data_all[team_number]
                spacing_text = ""
                for spacing in spacings_data:
                    spacing_text += f"{spacing:>2}, "
                spacing_text = spacing_text[:-2]

                team_number_text = colour_text(f"{team_number:>3}", 'blue')

                text_to_add = f"\n  {team_number_text}       {min_spacing_text}{gap_between_sections}{av_spacing_text}{gap_between_sections}{max_spacing_text}{gap_between_sections}{spacing_text}"

                output_text += text_to_add

            #Spacing stuff:     [team_num, list_of_spacings]
            #output_text += "\n  Team   Spacings"
            # for n, spacings_data in enumerate(spacings_data_all):
            #     text_to_add = f"\n  {n+1:>3}    "
            #     for spacing in spacings_data:
            #         text_to_add += f"{spacing:>2}, "
            #     text_to_add = text_to_add[:-2]
            #     output_text += text_to_add

        output_text += "\n\n"
    return output_text, summary_of_checks

def get_facings_data(match_schedule, specific_team_number, in_blocks=False):
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule, in_blocks)
    number_of_appearances = get_appearances_from_schedule(match_schedule, in_blocks)
    #get_facings_data()
    facings_data = {}
    for team_number in list_of_team_numbers:
        facings_data[team_number] = 0

    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                if specific_team_number in match:
                    for team_number in list_of_team_numbers:
                        if team_number in match:
                            facings_data[team_number] += 1
    else:
        for match in match_schedule:
            if specific_team_number in match:
                for team_number in list_of_team_numbers:
                    if team_number in match:
                        facings_data[team_number] += 1

    #analyse_facings_data()
    facing_repeats_data = [0]   #Accounts for facing a team 0 times.
    for n in range(number_of_appearances):
        facing_repeats_data.append(0)   #Accounts for facing a team up to the number of appearances times.
    for team_number in list_of_team_numbers:
        if team_number != specific_team_number:
            facing_repeats_data[facings_data[team_number]] += 1
    return facing_repeats_data

def get_appearances_data(match_schedule, specific_team_number, in_blocks=False):
    number_of_teams = get_number_of_teams_from_schedule(match_schedule, in_blocks)
    appearances = 0

    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                if specific_team_number in match:
                    appearances += 1
    else:
        for match in match_schedule:
            if specific_team_number in match:
                appearances += 1

    return appearances

def facings_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    number_of_teams = get_number_of_teams_from_schedule(match_schedule)
    number_of_appearances = get_appearances_from_schedule(match_schedule)
    output_text = "\n## Facings\n"
    output_text += "\n#### This looks at which how many teams a team faces and how many they do not face.\n"
    facings_data_all = {}
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)
    list_of_team_numbers_for_repeats = get_list_of_team_numbers_from_schedule(match_schedule)
    for team_number in list_of_team_numbers:
        if not team_number in exclude_teams_list:
            facings_data = get_facings_data(match_schedule, team_number)
            # print(f"{team_number}: {facings_data}")
            # facings_data_all.append(facings_data)
            facings_data_all[team_number] = facings_data
    
    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    best_faces = number_of_appearances*(number_of_teams_per_match-1)
    if best_faces > number_of_teams-1:
        best_faces = number_of_teams-1

    output_text += f"\nNumber of teams that have a specific 'faces (misses)'"
    text_to_add = f"faces {best_faces} ({number_of_teams-1-best_faces})"
    output_text += f" ({colour_text(text_to_add, 'dark green')} is best):"

    strong_alert_level = best_faces-10
    medium_alert_level = best_faces-6
    weak_alert_level = best_faces-4
    strong_alert_level_count, medium_alert_level_count, weak_alert_level_count = 0, 0, 0
    
    n = best_faces
    while n >= 0:
        total_teams = 0
        total_teams_list = []
        for m in facings_data_all.keys():
            facings_data = facings_data_all[m]
            total_non_zero = 0
            for q in range(number_of_appearances):
                total_non_zero += facings_data[q+1]
            
            if total_non_zero == n:
                total_teams += 1
                total_teams_list.append(m)
        
        if total_teams > 0:
            text_to_add = f"  faces {n:>3} {f'({number_of_teams-1-n})':>5}: {total_teams:>3} teams"
            if n == best_faces and total_teams == number_of_teams:
                text_to_add = colour_text(text_to_add, "green")
                checks_text_to_add = f"{total_teams:>3} teams face {n:>3} {f'({number_of_teams-1-n})':>5}."
                summary_of_checks[3].append(["facings", f"{colour_text(checks_text_to_add, 'green')} This means all the teams have a perfect facing."])
                add_team_numbers = False
            elif n == best_faces:
                text_to_add = colour_text(text_to_add, "dark green")
                add_team_numbers = False
            elif n < strong_alert_level:
                text_to_add = colour_text(text_to_add, "red")
                strong_alert_level_count += total_teams
                add_team_numbers = True
            elif n < medium_alert_level:
                text_to_add = colour_text(text_to_add, "orange")
                medium_alert_level_count += total_teams
                add_team_numbers = True
            elif n < weak_alert_level:
                text_to_add = colour_text(text_to_add, "yellow")
                weak_alert_level_count += total_teams
                add_team_numbers = True
            else:
                add_team_numbers = False
            
            if add_team_numbers:
                team_list_text = tidy_list_of_team_numbers(total_teams_list)
            else:
                team_list_text = ""

            output_text += f"\n{text_to_add}{team_list_text}"
        n -= 1
    output_text += "\n"

    if strong_alert_level_count > 0:
        text = f"{strong_alert_level_count:>3} teams have a facing more than {best_faces-strong_alert_level} away from the best possible facing."
        strong_alert_level_text = f"{colour_text(text, 'red')} These teams miss facing a lot ({number_of_teams-strong_alert_level}) of teams."
        summary_of_checks[0].append(["facings", strong_alert_level_text])
        output_text += f"\n{strong_alert_level_text}"
        output_text += "\n"
    
    if medium_alert_level_count > 0:
        text = f"{strong_alert_level_count+medium_alert_level_count:>3} teams have a facing more than {best_faces-medium_alert_level} away from the best possible facing."
        medium_alert_level_text = f"{colour_text(text, 'orange')} These teams miss facing quite a few ({number_of_teams-medium_alert_level}) teams."
        summary_of_checks[1].append(["facings", medium_alert_level_text])
        output_text += f"\n{medium_alert_level_text}"
        output_text += "\n"
    
    if weak_alert_level_count > 0:
        text = f"{strong_alert_level_count+medium_alert_level_count+weak_alert_level_count:>3} teams have a facing more than {best_faces-weak_alert_level} away from the best possible facing."
        weak_alert_level_text = f"{colour_text(text, 'yellow')} These teams miss facing a few ({number_of_teams-weak_alert_level}) teams."
        summary_of_checks[2].append(["facings", weak_alert_level_text])
        output_text += f"\n{weak_alert_level_text}"
        output_text += "\n"
    
    output_text += "\n#### This looks at how many times a team has faced other teams.\n"

    output_text += "\nRepeats:"

    target_repeats = number_of_appearances*(number_of_teams_per_match-1)/number_of_teams

    strong_alert_level_repeats = target_repeats+4
    medium_alert_level_repeats = target_repeats+2
    weak_alert_level_repeats = target_repeats+1
    strong_alert_level_repeats_count, medium_alert_level_repeats_count, weak_alert_level_repeats_count = 0, 0, 0

    for team_number in exclude_teams_list:
        list_of_team_numbers_for_repeats.remove(team_number)

    for q in range(number_of_appearances+1):
        number_of_teams_at_q = 0
        list_of_teams_at_q = []
        for m in facings_data_all.keys():
            if facings_data_all[m][q] > 0:
                number_of_teams_at_q += 1
                list_of_teams_at_q.append(m)
        
        if number_of_teams_at_q > 0:
            if q > strong_alert_level_repeats:
                colour = "red"
                add_team_numbers = True
                strong_alert_level_repeats_count += number_of_teams_at_q
            elif q > medium_alert_level_repeats:
                colour = "orange"
                add_team_numbers = True
                medium_alert_level_repeats_count += number_of_teams_at_q
            elif q > weak_alert_level_repeats:
                colour = "yellow"
                add_team_numbers = True
                weak_alert_level_repeats_count += number_of_teams_at_q
            else:
                colour = None
                add_team_numbers = False
            
            text_to_add = colour_text(f"  faces 1+ teams {q:>2} times: {number_of_teams_at_q:>3} teams", colour)
            if add_team_numbers:
                team_list_text = tidy_list_of_team_numbers_text(list_of_teams_at_q, number_of_teams, exclude_teams_list)
                output_text += f"\n{text_to_add}{team_list_text}"

                number_of_teams_faced_at_q = {}
                number_of_teams_faced_at_q[0] = []
                for b in list_of_team_numbers:
                    number_of_teams_faced_at_q[b] = []

                for team_number in list_of_team_numbers:
                    if not team_number in exclude_teams_list:
                        number_of_teams_faced_at_q[facings_data_all[team_number][q]].append(team_number)

                display_list = []
                for b, list_of_teams_facing_b_teams in number_of_teams_faced_at_q.items():
                    if len(list_of_teams_facing_b_teams) > 0:
                        display_list.append([b, list_of_teams_facing_b_teams])
                
                c = len(display_list)-1
                while c >= 0:
                    b, list_of_teams_facing_b_teams = display_list[c]
                    if b > 0:
                        text_to_add = colour_text(f"    faces {b:>3} teams {q:>2}x: {len(list_of_teams_facing_b_teams):>3} teams", colour)
                        team_list_text = tidy_list_of_team_numbers_text(list_of_teams_facing_b_teams, number_of_teams, exclude_teams_list)
                        output_text += f"\n{text_to_add}{team_list_text}"
                    c -= 1
            else:
                output_text += f"\n{text_to_add}"
        
    output_text += "\n"

    if strong_alert_level_repeats_count > 0:
        text = f"{strong_alert_level_repeats_count:>3} teams play at least one team more than {math.floor(strong_alert_level_repeats)} times."
        strong_alert_level_text = f"{colour_text(text, 'red')} Playing the same team(s) a lot of times is repetitive and can be unfair."
        summary_of_checks[0].append(["repeats", strong_alert_level_text])
        output_text += f"\n{strong_alert_level_text}\n"
    
    if medium_alert_level_repeats_count > 0:
        text = f"{medium_alert_level_repeats_count:>3} teams play at least one team more than {math.floor(medium_alert_level_repeats)} times."
        medium_alert_level_text = f"{colour_text(text, 'orange')} Playing the same team(s) many times times is repetitive and can be unfair."
        summary_of_checks[1].append(["repeats", medium_alert_level_text])
        output_text += f"\n{medium_alert_level_text}\n"
    
    if weak_alert_level_repeats_count > 0:
        text = f"{weak_alert_level_repeats_count:>3} teams play at least one team more than {math.floor(weak_alert_level_repeats)} times."
        weak_alert_level_text = f"{colour_text(text, 'yellow')} Playing the same team(s) a few times is repetitive and can be unfair."
        summary_of_checks[2].append(["repeats", weak_alert_level_text])
        output_text += f"\n{weak_alert_level_text}\n"
    
    output_text += "\n"

    if detailed:
        output_text += "\nFacings more detailed:\n"

        facings_info_array = []

        for n, facings_data in facings_data_all.items():
            total_non_zero = 0
            for q in range(number_of_appearances):
                total_non_zero += facings_data[q+1]
            
            facings_info_array.append([n, total_non_zero, number_of_teams-1-total_non_zero])
        
        facings_info_array = order_array_list(facings_info_array, 1, False)
        for row in facings_info_array:
            if row[1] == best_faces:
                colour = "dark green"
            elif row[1] < strong_alert_level:
                colour = "red"
            elif row[1] < medium_alert_level:
                colour = "orange"
            elif row[1] < weak_alert_level:
                colour = "yellow"
            else:
                colour = None
            facings_part_text = f"faces {row[1]:>3}, misses {row[2]:>3}"
            output_text += f"\n  {row[0]:>3}  {colour_text(facings_part_text, colour)}"
        
        output_text += "\n"

        for m in range(number_of_appearances+1):
            if m > strong_alert_level_repeats:
                colour = "red"
            elif m > medium_alert_level_repeats:
                colour = "orange"
            elif m > weak_alert_level_repeats:
                colour = "yellow"
            else:
                colour = None
            facings_repeats_array = []
            all_zero = True
            for n, facings_data in facings_data_all.items():
                if facings_data[m] > 0:
                    all_zero = False
                facings_repeats_array.append([n, facings_data[m]])
            
            facings_repeats_array = order_array_list(facings_repeats_array, 1, True)

            if not all_zero:
                output_text += f"\nTeams and the number of teams they play {m} times:\n"
                for row in facings_repeats_array:
                    if row[1] == 0:
                        colour = None
                    output_text += colour_text(f"\n  {row[0]:>3} faces {row[1]:>2} teams {m} times", colour)

                output_text += "\n"

    return output_text, summary_of_checks

def appearances_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)
    number_of_teams = get_number_of_teams_from_schedule(match_schedule)-len(exclude_teams_list)
    appearances_list = {}
    output_text = "\n## Appearances\n"
    output_text += "\n#### This looks at how many matches a team has. Every team should play the same number of matches.\n"
    output_text += "\nNumber of appearances for each team:\n"

    for team_number in list_of_team_numbers:
        if not team_number in exclude_teams_list:
            appearances_list[team_number] = get_appearances_data(match_schedule, team_number)
            # appearances_list.append(get_appearances_data(match_schedule, team_number))
    
    list_of_appearance_numbers = []
    for appearance_count in appearances_list.values():
        if not appearance_count in list_of_appearance_numbers:
            list_of_appearance_numbers.append(appearance_count)
    
    appearances_and_team_count = []
    red_appearances = False

    appearances_list_totals = Counter(appearances_list.values())

    for appearance_count in list_of_appearance_numbers:
        appearances_and_team_count.append([appearance_count, appearances_list_totals[appearance_count]])
    
    if len(appearances_and_team_count) == 1 and appearances_and_team_count[0][1] == number_of_teams:
        text_to_add = f" {appearances_and_team_count[0][0]:>2} appearances: {appearances_and_team_count[0][1]:>3} teams"
        output_text += colour_text(text_to_add, "green")
        checks_text_to_add = f" {appearances_and_team_count[0][1]:>3} teams have an appearance of {appearances_and_team_count[0][0]:>2}."
        summary_of_checks[3].append(["appearances", f"{colour_text(checks_text_to_add, 'green')} All the teams have the same number of appearances."])
    else:
        max_team_count = order_array_list(appearances_and_team_count, 1)[-1][1]
        sorted_list = order_array_list(appearances_and_team_count, 0)
        n = len(sorted_list)-1
        while n >= 0:
            item = sorted_list[n]
            text_to_add = f" {item[0]:>2} appearances: {item[1]:>3} teams"
            if item[1] == max_team_count:
                colour = "orange"
                team_list_text = ""
            else:
                colour = "red"
                team_list = get_team_list_when_number_matches_dict(appearances_list, item[0])
                tidy_list_of_team_numbers_text(team_list, number_of_teams, exclude_teams_list)
            output_text += colour_text(f"{text_to_add}", colour)
            output_text += f"{team_list_text}\n"
            red_appearances = True
            n -= 1
    
    if red_appearances:
        text_to_add = "Not all teams have the same number of appearances."
        summary_of_checks[0].append(["appearances", f"{colour_text(text_to_add, 'red')} All teams should have the same number of matches. Note that unequal appearances may have resulted in errors elsewhere in the checks."])
        output_text += f"\n{colour_text(text_to_add, 'red')} All teams should have the same number of matches. Note that unequal appearances may have resulted in errors elsewhere in the checks."
    
    output_text += "\n\n"
    return output_text, summary_of_checks

def get_number_of_non_four_robot_matches(match_schedule):
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)
    number_of_three_robot_matches = 0
    number_of_two_robot_matches = 0
    number_of_one_robot_matches = 0
    teams_in_three_robots_matches = {}
    for team_number in list_of_team_numbers:
        teams_in_three_robots_matches[team_number] = 0
    for match in match_schedule:
        teams_in_match = 0
        for team_number in list_of_team_numbers:
            if team_number in match:
                teams_in_match += 1
        if teams_in_match == 3:
            number_of_three_robot_matches += 1
            for team_number in list_of_team_numbers:
                if team_number in match:
                    teams_in_three_robots_matches[team_number] += 1
        elif teams_in_match == 2:
            number_of_two_robot_matches += 1
        elif teams_in_match == 1:
            number_of_one_robot_matches += 1
    return number_of_three_robot_matches, number_of_two_robot_matches, number_of_one_robot_matches, teams_in_three_robots_matches

def non_four_robot_match_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    output_text = "\n## Matches that do not contain 4 Robots\n"
    output_text += "\n#### Sometimes matches containing only 3 robots are required to fill the schedule. This checks that there are not more of these matches than are required."
    output_text += "\n#### However, 1 or 2 robot matches should never be required or aimed for (use 3 robot matches instead), so this also checks to see if any of those are present.\n"

    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)

    number_of_teams = get_number_of_teams_from_schedule(match_schedule)-len(exclude_teams_list)
    number_of_appearances = get_appearances_from_schedule(match_schedule)
    if number_of_teams*number_of_appearances % 4 == 0:
        fake_teams_to_add = 0
    else:
        fake_teams_to_add = 4 - number_of_teams*number_of_appearances % 4

    number_of_three_robot_matches, number_of_two_robot_matches, number_of_one_robot_matches, teams_in_three_robots_matches = get_number_of_non_four_robot_matches(match_schedule)

    if number_of_three_robot_matches == 1:
        add_s = ""
    else:
        add_s = "es"
    
    if number_of_teams_per_match == 2:
        if number_of_one_robot_matches == 1:
            add_s = ""
        else:
            add_s = "es"
        text_to_add = f"\n  Number of 1 robot matches: {number_of_one_robot_matches:>2} match{add_s}"
        checks_text_to_add = f"The number of 1 robot matches is {number_of_one_robot_matches} match{add_s}."
        
        if number_of_one_robot_matches == 0:
            output_text += colour_text(text_to_add, "green")
            alert_text_one_robot = "\n"
            summary_of_checks[3].append(["1 robot matches", f"{colour_text(checks_text_to_add, 'green')} This is the ideal number of 1 robot matches."])
        else:
            output_text += colour_text(text_to_add, "red")
            alert_text_one_robot = "\nThe ideal number of 1 robot matches is 0 matches.\n"
            summary_of_checks[0].append(["1 robot matches", f"{colour_text(checks_text_to_add, 'red')} The ideal number of 1 robot matches is 0 matches."])
        
        output_text += f"\n{alert_text_one_robot}\n"
    else:
        text_to_add = f"\n  Number of 3 robot matches: {number_of_three_robot_matches:>2} match{add_s}"

        if number_of_three_robot_matches == fake_teams_to_add:
            output_text += colour_text(text_to_add, "green")
            alert_text_three_robot = ""
            checks_text_to_add = f"The number of 3 robot matches is {number_of_three_robot_matches} match{add_s}."
            summary_of_checks[3].append(["3 robot matches", f"{colour_text(checks_text_to_add, 'green')} This is the lowest number of 3 robot matches posssible for this number of teams and appearances."])
        else:
            output_text += colour_text(text_to_add, "orange")
            checks_text_to_add = f"The number of 3 robot matches is {number_of_three_robot_matches} match{add_s}."
            if fake_teams_to_add == 1:
                add_s = ""
            else:
                add_s = "es"
            alert_text_three_robot = f"\nThe ideal number of 3 robot matches is {fake_teams_to_add} match{add_s}.\n"
            summary_of_checks[1].append(["3 robot matches", f"{colour_text(checks_text_to_add, 'orange')} The ideal number of 3 robot matches for this number of teams and appearances is {fake_teams_to_add} match{add_s}"])
        
        if number_of_two_robot_matches == 1:
            add_s = ""
        else:
            add_s = "es"
        text_to_add = f"\n  Number of 2 robot matches: {number_of_two_robot_matches:>2} match{add_s}"
        checks_text_to_add = f"The number of 2 robot matches is {number_of_two_robot_matches} match{add_s}."

        if number_of_two_robot_matches == 0:
            output_text += colour_text(text_to_add, "green")
            alert_text_two_robot = ""
            summary_of_checks[3].append(["2 robot matches", f"{colour_text(checks_text_to_add, 'green')} This is the ideal number of 2 robot matches."])
        else:
            output_text += colour_text(text_to_add, "red")
            alert_text_two_robot = "\nThe ideal number of 2 robot matches is 0 matches.\n"
            summary_of_checks[0].append(["2 robot matches", f"{colour_text(checks_text_to_add, 'red')} The ideal number of 2 robot matches is 0 matches."])
            
        if number_of_one_robot_matches == 1:
            add_s = ""
        else:
            add_s = "es"
        text_to_add = f"\n  Number of 1 robot matches: {number_of_one_robot_matches:>2} match{add_s}"
        checks_text_to_add = f"The number of 1 robot matches is {number_of_one_robot_matches} match{add_s}."
        
        if number_of_one_robot_matches == 0:
            output_text += colour_text(text_to_add, "green")
            alert_text_one_robot = ""
            summary_of_checks[3].append(["1 robot matches", f"{colour_text(checks_text_to_add, 'green')} This is the ideal number of 1 robot matches."])
        else:
            output_text += colour_text(text_to_add, "red")
            alert_text_one_robot = "\nThe ideal number of 1 robot matches is 0 matches.\n"
            summary_of_checks[0].append(["1 robot matches", f"{colour_text(checks_text_to_add, 'red')} The ideal number of 1 robot matches is 0 matches."])
        
        output_text += f"\n{alert_text_three_robot}{alert_text_two_robot}{alert_text_one_robot}"

        output_text += "\n"
    
    if detailed:
        output_text += "\nNumber of times each team is present in 3 robot matches:"
        info_array = []
        for team_number in list_of_team_numbers:
            if not team_number in exclude_teams_list:
                info_array.append([team_number, teams_in_three_robots_matches[team_number]])
        
        info_array = order_array_list(info_array, 1, True)

        for row in info_array:
            text_to_add = f"\n  {row[0]:>3}: {row[1]:>2} times"
            if row[1] == 0:
                colour = None
            elif row[1] == 1:
                colour = "orange"
            else:
                colour = "red"
            output_text += colour_text(text_to_add, colour)
        output_text += "\n\n"

    return output_text, summary_of_checks

def get_teams_in_match_multiple_times_data(match_schedule):
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)
    output = []
    for n, match in enumerate(match_schedule):
        if len(match) != len(set(match)):
            check_missing = 0
            for team_num in match:
                if team_num > 0:
                    check_missing += 1
            if check_missing >= 3:
                output.append(n)
    return output

def get_overlap_data(match_schedule, in_blocks=False):
    #get_overlap_data()
    match_list_3_all = []
    match_list_4_all = []
    match_list_3_unique = set()
    match_list_4_unique = set()
    match_list_3_match_num = []
    match_list_4_match_num = []
    counter = 0
    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                match_temp = match.copy()
                match_temp_1 = order_list_insert(match_temp)
                match_list_4_all.append(match_temp_1)
                match_list_4_unique.add(tuple(match_temp_1))
                match_list_4_match_num.append([counter, match_temp_1])
                
                match_temp_1 = order_list_insert([match_temp[0], match_temp[1], match_temp[2]])
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_list_3_match_num.append([counter, match_temp_1])
                match_temp_1 = order_list_insert([match_temp[0], match_temp[1], match_temp[3]])
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_list_3_match_num.append([counter, match_temp_1])
                match_temp_1 = order_list_insert([match_temp[0], match_temp[2], match_temp[3]])
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_list_3_match_num.append([counter, match_temp_1])
                match_temp_1 = order_list_insert([match_temp[1], match_temp[2], match_temp[3]])
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_list_3_match_num.append([counter, match_temp_1])
                counter += 1
    else:
        for match in match_schedule:
            match_temp = match.copy()
            match_temp_1 = order_list_insert(match_temp)
            match_list_4_all.append(match_temp_1)
            match_list_4_unique.add(tuple(match_temp_1))
            match_list_4_match_num.append([counter, match_temp_1])
            
            match_temp_1 = order_list_insert([match_temp[0], match_temp[1], match_temp[2]])
            match_list_3_all.append(match_temp_1)
            match_list_3_unique.add(tuple(match_temp_1))
            match_list_3_match_num.append([counter, match_temp_1])
            match_temp_1 = order_list_insert([match_temp[0], match_temp[1], match_temp[3]])
            match_list_3_all.append(match_temp_1)
            match_list_3_unique.add(tuple(match_temp_1))
            match_list_3_match_num.append([counter, match_temp_1])
            match_temp_1 = order_list_insert([match_temp[0], match_temp[2], match_temp[3]])
            match_list_3_all.append(match_temp_1)
            match_list_3_unique.add(tuple(match_temp_1))
            match_list_3_match_num.append([counter, match_temp_1])
            match_temp_1 = order_list_insert([match_temp[1], match_temp[2], match_temp[3]])
            match_list_3_all.append(match_temp_1)
            match_list_3_unique.add(tuple(match_temp_1))
            match_list_3_match_num.append([counter, match_temp_1])
            counter += 1

    match_lists_3 = []
    for match_temp_tup in match_list_3_unique:
        mtt = match_temp_tup
        match_temp = [mtt[0], mtt[1], mtt[2]]
        count = match_list_3_all.count(match_temp)
        if count > 1:
            match_list = []
            for row in match_list_3_match_num:
                if row[1] == match_temp:
                    match_list.append(row[0])
            match_lists_3.append(match_list)
    
    match_lists_4 = []
    for match_temp_tup in match_list_4_unique:
        mtt = match_temp_tup
        match_temp = [mtt[0], mtt[1], mtt[2], mtt[3]]
        count = match_list_4_all.count(match_temp)
        if count > 1:
            match_list = []
            for row in match_list_4_match_num:
                if row[1] == match_temp:
                    match_list.append(row[0])
            match_lists_4.append(match_list)
    
    for row in match_lists_4:
        n = 0
        while n < len(match_lists_3):
            if row == match_lists_3[n]:
                match_lists_3.pop(n)
                n -= 1
            n += 1
    
    return match_lists_3, match_lists_4

def overlap_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    output_text = "\n## Overlapping matches\n"
    output_text += "\n#### This looks at matches that partially overlap (3 out of the 4 teams are the same) and matches that fully overlap (all 4 teams are the same)\n"

    match_lists_3, match_lists_4 = get_overlap_data(match_schedule)
    
    total_match_lists_3 = 0
    for match_overlap in match_lists_3:
        total_match_lists_3 += len(match_overlap)

    if total_match_lists_3 == 0:
        add_s = "es"
        colour = "green"
    elif total_match_lists_3 == 1:
        add_s = ""
        colour = "yellow"
    else:
        add_s = "es"
        colour = "yellow"
    
    # output_text += colour_text(f"\n  Number of partially overlapped matches: {len(match_lists_3)} match{add_s}.", colour)
    text_to_add = colour_text(f"Number of partially overlapped matches: {total_match_lists_3} match{add_s}", colour)
    output_text += f"\n  {text_to_add}"
    if total_match_lists_3 == 0:
        summary_of_checks[3].append(["partially overlapped matches", f"{text_to_add}"])
    else:
        summary_of_checks[2].append(["partially overlapped matches", f"{text_to_add} No overlapped matches is best."])

    total_match_lists_4 = 0
    for match_overlap in match_lists_4:
        total_match_lists_4 += len(match_overlap)

    if total_match_lists_4 == 0:
        add_s = "es"
        colour = "green"
    elif total_match_lists_4 == 1:
        add_s = ""
        colour = "orange"
    else:
        add_s = "es"
        colour = "orange"

    # output_text += colour_text(f"\n  Number of identical matches: {len(match_lists_4)} match{add_s}.", colour)
    text_to_add = colour_text(f"Number of identical matches: {total_match_lists_4} match{add_s}", colour)
    output_text += f"\n  {text_to_add}"
    if total_match_lists_4 == 0:
        summary_of_checks[3].append(["identical matches", f"{text_to_add}"])
    else:
        summary_of_checks[1].append(["identical matches", f"{text_to_add} No identical (i.e. repeat) matches is best from a competitor and spectator perspective."])

    output_text += "\n"

    if detailed:
        if len(match_lists_3) > 0:
            output_text += "\n  Partially overlapped matches list:"
            for match_list in match_lists_3:
                if not FIRST_MATCH_IS_MATCH_ZERO:
                    match_list_copy = []
                    n = 0
                    while n < len(match_list):
                        match_list_copy.append(match_list[n]+1)
                        n += 1
                else:
                    match_list_copy = match_list.copy()
                row_text = "\n    "
                while len(match_list_copy) > 1:
                    if not FIRST_MATCH_IS_MATCH_ZERO:
                        row_text += f"{match_list_copy[0]}, "
                    match_list_copy.pop(0)
                overlap_set = set(match_schedule[match_list[0]]) & set(match_schedule[match_list[1]])
                overlapping_team_numbers = tidy_list_of_team_numbers(order_list(list(overlap_set)))
                row_text += f"{match_list_copy[0]} partially overlap with each other. (Team numbers in overlap: {overlapping_team_numbers[2:]}"
                output_text += row_text
        output_text += "\n"
        if len(match_lists_4) > 0:
            output_text += "\n  Identical matches list:"
            for match_list in match_lists_4:
                if not FIRST_MATCH_IS_MATCH_ZERO:
                    match_list_copy = []
                    n = 0
                    while n < len(match_list):
                        match_list_copy.append(match_list[n]+1)
                        n += 1
                else:
                    match_list_copy = match_list.copy()
                row_text = "\n    "
                while len(match_list_copy) > 1:
                    row_text += f"{match_list_copy[0]}, "
                    match_list_copy.pop(0)
                overlap_set = set(match_schedule[match_list[0]]) & set(match_schedule[match_list[1]])
                overlapping_team_numbers = tidy_list_of_team_numbers(order_list(list(overlap_set)))
                row_text += f"{match_list_copy[0]} are identical to each other. (Team numbers in overlap: {overlapping_team_numbers[2:]}"
                output_text += row_text
        output_text += "\n"
                
    output_text += "\n"

    return output_text, summary_of_checks

def teams_in_match_multiple_times_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    output_text = "\n## Team Number in a single match multiple times\n"
    output_text += "\n#### Checks to make sure a single team number does not appear in a match multiple times.\n"
    list_data = get_teams_in_match_multiple_times_data(match_schedule)
    if len(list_data) == 0:
        output_text += colour_text(f"\n  Number of matches with multiple team numbers: {len(list_data)} matches", "green")
        checks_text_to_add = f"The number of matches with multiple of the same number in them is {len(list_data)} matches."
        summary_of_checks[3].append(["teams in match multiple times", f"{colour_text(checks_text_to_add, 'green')}"])
    else:
        output_text += colour_text(f"\n  Number of matches with multiple team numbers: {len(list_data)} matches", "red")
        if not FIRST_MATCH_IS_MATCH_ZERO:
            n = 0
            while n < len(list_data):
                list_data[n] += 1
                n += 1
        output_text += f" (Match numbers: {tidy_list_of_team_numbers(list_data)[2:]}"
        
        checks_text_to_add = f"The number of matches with multiple of the same number in them is {len(list_data)} matches."
        summary_of_checks[0].append(["teams in match multiple times", f"{colour_text(checks_text_to_add, 'red')} There should be no matches with the same team number twice. The matches with the same team number twice are: {tidy_list_of_team_numbers(list_data)[2:-1]}."])
    output_text += "\n\n"
    return output_text, summary_of_checks

def get_corners_data(match_schedule, specific_team_number, in_blocks=False):
    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    if number_of_teams_per_match == 2:
        corners_data = [0, 0]
    else:
        corners_data = [0, 0, 0, 0]
    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                if specific_team_number in match:
                    pos = match.index(specific_team_number)
                    corners_data[pos] += 1
    else:
        for match in match_schedule:
            if specific_team_number in match:
                pos = match.index(specific_team_number)
                corners_data[pos] += 1
    return corners_data

def corners_check(match_schedule, summary_of_checks, exclude_teams_list, detailed=False):
    output_text = "\n## Starting Zone Allocations Check\n"
    output_text += "\n#### This checks that teams start in a roughly even proportion of the starting zones.\n"
    number_of_teams = get_number_of_teams_from_schedule(match_schedule)-len(exclude_teams_list)
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule)
    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    corners_data_all = {}
    std_all = []
    std_all_dict = {}
    for specific_team_number in list_of_team_numbers:
        if not specific_team_number in exclude_teams_list:
            corners_data = get_corners_data(match_schedule, specific_team_number)
            corners_data_all[specific_team_number] = corners_data
            std_all.append(statistics.stdev(corners_data))
            std_all_dict[specific_team_number] = statistics.stdev(corners_data)

    fake_corners_data = []

    remaining_corners = number_of_teams_per_match
    appearances_left = get_appearances_from_schedule(match_schedule)
    while remaining_corners > 0:
        if appearances_left%remaining_corners == 0:
            corner_num = int(appearances_left/remaining_corners)
        else:
            corner_num = int(math.floor(appearances_left/remaining_corners))
        fake_corners_data.append(corner_num)
        appearances_left -= corner_num
        remaining_corners -= 1
    target_std = statistics.stdev(fake_corners_data)
    std_unique = list(set(std_all))
    std_unique = order_list(std_unique, True)

    target_std_formatted = colour_text(f"{target_std:.3f}", "dark green")
    output_text += f"\nNumber of teams with each zone standard deviation ({target_std_formatted} is perfect):"

    strong_alert_std_count, medium_alert_std_count, weak_alert_std_count = 0, 0, 0
    strong_alert_level, medium_alert_level, weak_alert_level = 3.0, 1.8, 1.4

    for std_unique_value in std_unique:
        total_teams = 0
        for std_value in std_all:
            if std_value == std_unique_value:
                total_teams += 1
        
        if std_unique_value == target_std:
            colour = "dark green"
            add_team_numbers = False
        elif std_unique_value > strong_alert_level:
            colour = "red"
            strong_alert_std_count += total_teams
            add_team_numbers = True
        elif std_unique_value > medium_alert_level:
            colour = "orange"
            medium_alert_std_count += total_teams
            add_team_numbers = True
        elif std_unique_value > weak_alert_level:
            colour = "yellow"
            weak_alert_std_count += total_teams
            add_team_numbers = True
        else:
            colour = None
            add_team_numbers = False
        
        if total_teams > 0:
            if total_teams == number_of_teams and std_unique_value == target_std:
                text = f"All {total_teams:>3} teams have a zone allocation standard deviation of {std_unique_value:.1f}."
                perfect_level_text = f"{colour_text(text, 'green')} This zone allocation is perfect for this number of appearances."
                summary_of_checks[3].append(["zone allocation", perfect_level_text])
                colour = "green"
                add_s = "s"
            elif total_teams == 1:
                add_s = " "
            else:
                add_s = "s"

            if add_team_numbers:
                team_list_text = get_team_list_text_when_number_matches(std_all, std_unique_value)
            else:
                team_list_text = ""

            text_to_add = colour_text(f"{std_unique_value:.3f}: {total_teams:>3} team{add_s}", colour)
            output_text += f"\n  {text_to_add} {team_list_text}"
    
    output_text += "\n"
    
    if strong_alert_std_count > 0:
        text = f"{strong_alert_std_count:>3} teams have a zone allocation standard deviation larger than {strong_alert_level:.1f}."
        strong_alert_level_text = f"{colour_text(text, 'red')} This zone allocation is very unequally distributed.\n"
        summary_of_checks[0].append(["zone allocation", strong_alert_level_text])
        output_text += f"\n{strong_alert_level_text}"
    
    if medium_alert_std_count > 0:
        text = f"{medium_alert_std_count+strong_alert_std_count:>3} teams have a zone allocation standard deviation larger than {medium_alert_level:.1f}."
        medium_alert_level_text = f"{colour_text(text, 'orange')} This zone allocation is quite unequally distributed.\n"
        summary_of_checks[1].append(["zone allocation", medium_alert_level_text])
        output_text += f"\n{medium_alert_level_text}"
    
    if weak_alert_std_count > 0:
        text = f"{weak_alert_std_count+medium_alert_std_count+strong_alert_std_count:>3} teams have a zone allocation standard deviation larger than {weak_alert_level:.1f}."
        weak_alert_level_text = f"{colour_text(text, 'yellow')} This zone allocation is a bit unequally distributed.\n"
        summary_of_checks[2].append(["zone allocation", weak_alert_level_text])
        output_text += f"\n{weak_alert_level_text}"
    
    # if strong_alert_std_count > 0 or medium_alert_std_count > 0 or weak_alert_std_count > 0:
    #     output_text += "\n"
    
    if detailed:
        output_text += "\nDetailed zones data:"
        detailed_std_array = []
        for n in corners_data_all.keys():
            detailed_std_array.append([n, std_all_dict[n], corners_data_all[n]])
        
        detailed_std_array = order_array_list(detailed_std_array, 1, True)
        for row in detailed_std_array:
            if row[1] == target_std:
                colour = "dark green"
            elif row[1] > strong_alert_level:
                colour = "red"
            elif row[1] > medium_alert_level:
                colour = "orange"
            elif row[1] > weak_alert_level:
                colour = "yellow"
            else:
                colour = None
            std_text = colour_text(f"{row[0]:>3} is {row[1]:.3f}", colour)
            corners_text = "(zones: "
            for corner_num in row[2]:
                corners_text += f"{corner_num:>2},"
            corners_text = corners_text[:-1]
            corners_text += ")"

            output_text += f"\n  {std_text}    {corners_text}"
        output_text += "\n"

    return output_text, summary_of_checks


def print_summary_of_checks(match_schedule, summary_of_checks, exclude_teams_list):
    summary_of_checks_text = colour_text("\n## Summary of Checks\n\n", "blue")
    summary_of_checks_text = colour_text(summary_of_checks_text, "bold")
    print(summary_of_checks_text)

    number_of_teams = get_number_of_teams_from_schedule(match_schedule)
    number_of_appearances = get_appearances_from_schedule(match_schedule)
    number_of_matches = len(match_schedule)
    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    if NUMBER_OF_ARENAS == 1:
        arena_s = ""
    else:
        arena_s = "s"
    print(f" {number_of_teams:>3} Teams\n {number_of_appearances:>3} Appearances per team\n {number_of_matches:>3} Matches, with {number_of_teams_per_match} teams per match, across {NUMBER_OF_ARENAS} Arena{arena_s}.")
    if len(exclude_teams_list) > 0:
        print(colour_text(f"\nNOTE: Some team numbers have been excluded from these checks", "red"))
        print(f"  Team numbers excluded from checks: {tidy_list_of_team_numbers(exclude_teams_list)[2:-1]}")

    print("\n")

    time.sleep(0.75)

    extra_info_for_checks_list = [[colour_text("### Critical Concerns", 'red'), f"{colour_text('O', 'green')} There are no critical concerns."],
                                  [colour_text("### Strong Concerns", 'orange'), f"{colour_text('O', 'green')} There are no strong concerns."],
                                  [colour_text("### Mild Concerns", 'yellow'), f"{colour_text('O', 'green')} There are no mild concerns."],
                                  [colour_text("### Perfect sections", 'green'), f"{colour_text('X', 'red')} There are no perfect sections."]]

    for n, checks_list in enumerate(summary_of_checks):
        print(f"{extra_info_for_checks_list[n][0]}")
        if n == 3:
            list_symbol = colour_text("O", 'green')
        else:
            list_symbol = colour_text("X", 'red')
        if len(checks_list) == 0:
            print(f"\n  {extra_info_for_checks_list[n][1]}")
        else:
            for check in checks_list:
                print(f"\n  {list_symbol} {check[0]:<30}: {check[1]}")
        print("\n")
        time.sleep(1)

def collate_summary_of_checks(match_schedule, summary_of_checks):
    summary_of_checks_text = colour_text("\n## Summary of Checks\n\n", "blue")
    summary_of_checks_text = colour_text(summary_of_checks_text, "bold")

    number_of_teams = get_number_of_teams_from_schedule(match_schedule)
    number_of_appearances = get_appearances_from_schedule(match_schedule)
    number_of_matches = len(match_schedule)
    summary_of_checks_text += f"{number_of_teams} Teams; {number_of_appearances} Appearances per team; {number_of_matches} Matches.\n\n"

    extra_info_for_checks_list = [[colour_text("### Critical Concerns", 'red'), f"{colour_text('O', 'green')} There are no critical concerns."],
                                  [colour_text("### Strong Concerns", 'orange'), f"{colour_text('O', 'green')} There are no strong concerns."],
                                  [colour_text("### Mild Concerns", 'yellow'), f"{colour_text('O', 'green')} There are no mild concerns."],
                                  [colour_text("### Perfect sections", 'green'), f"{colour_text('X', 'red')} There are no perfect sections."]]

    for n, checks_list in enumerate(summary_of_checks):
        summary_of_checks_text += f"\n{extra_info_for_checks_list[n][0]}\n"
        if n == 3:
            list_symbol = colour_text("O", 'green')
        else:
            list_symbol = colour_text("X", 'red')
        if len(checks_list) == 0:
            summary_of_checks_text += f"\n  {extra_info_for_checks_list[n][1]}"
        else:
            for check in checks_list:
                summary_of_checks_text += f"\n  {list_symbol} {check[0]:<30}: {check[1]}"
        summary_of_checks_text += "\n"
    return summary_of_checks_text

def run_all_checks(match_schedule, exclude_teams_list, detailed=False):
    summary_of_checks = [[], [], [], []]
    #order is red, orange, yellow, green, (dark green?)
    number_of_teams_per_match = get_number_of_teams_per_match_from_schedule(match_schedule)
    output_text_all = ""
    text_to_add, summary_of_checks = appearances_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
    output_text_all += text_to_add
    text_to_add, summary_of_checks = teams_in_match_multiple_times_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
    output_text_all += text_to_add
    text_to_add, summary_of_checks = non_four_robot_match_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
    output_text_all += text_to_add
    text_to_add, summary_of_checks = spacing_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
    output_text_all += text_to_add
    text_to_add, summary_of_checks = facings_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
    output_text_all += text_to_add
    if number_of_teams_per_match == 4:
        text_to_add, summary_of_checks = overlap_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
        output_text_all += text_to_add
    text_to_add, summary_of_checks = corners_check(match_schedule, summary_of_checks, exclude_teams_list, detailed)
    output_text_all += text_to_add
    return output_text_all, summary_of_checks

def interact_with_checks(match_schedule, exclude_teams_list=[]):
    output_text_all, summary_of_checks = run_all_checks(match_schedule, exclude_teams_list, False)
    print_summary_of_checks(match_schedule, summary_of_checks, exclude_teams_list)

    response = input("\nWould you like to see the basic overview of all the checks? (Y/N): ")

    if response.casefold()[:1] == "y":
        print(output_text_all)
        output_text_all, summary_of_checks = run_all_checks(match_schedule, exclude_teams_list, True)
        repeat_detailed_checks = True
        while repeat_detailed_checks:
            print("\nWould you like to see a detailed version of some/all of the checks?")
            print("(A) - ALL; (F) - Facings; (M) - teams in match multiple times; (N) - Non 4 robot matches; (O) - Overlap/Identical matches; (P) - Appearances; (S) - Spacing; (Z) - zone allocation")
            response = input("\n(A/F/M/N/O/P/S/Z): ")
            lower = response.casefold()[:1]
            summary_of_checks = [[], [], [], []]
            if lower == "y" or lower == "a":
                print(output_text_all)
                repeat_detailed_checks = False
            elif lower == "e":
                exclude_text = input("\nNumbers to exclude: ")
                exclude_teams_list = number_array_from_list(exclude_text)
                output_text_all, summary_of_checks = run_all_checks(match_schedule, exclude_teams_list, False)
                print_summary_of_checks(match_schedule, summary_of_checks, exclude_teams_list)

                response = input("\nWould you like to see the basic overview of all the checks? (Y/N): ")
                if response.casefold()[:1] == "y":
                    print(output_text_all)
                elif response.casefold()[:1] == "d":
                    output_text_all, summary_of_checks = run_all_checks(match_schedule, True)
                    print(output_text_all)
                else:
                    repeat_detailed_checks = False
            elif lower == "f":
                text_to_add, summary_of_checks = facings_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            elif lower == "m":
                text_to_add, summary_of_checks = teams_in_match_multiple_times_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            elif lower == "n":
                text_to_add, summary_of_checks = non_four_robot_match_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            elif lower == "o":
                text_to_add, summary_of_checks = overlap_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            elif lower == "p":
                text_to_add, summary_of_checks = appearances_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            elif lower == "s":
                text_to_add, summary_of_checks = spacing_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            elif lower == "z":
                text_to_add, summary_of_checks = corners_check(match_schedule, summary_of_checks, exclude_teams_list, True)
                print(text_to_add)
            else:
                repeat_detailed_checks = False
    elif response.casefold()[:1] == "d":
        output_text_all, summary_of_checks = run_all_checks(match_schedule, True)
        print(output_text_all)


location = ""
"""
Various different schedules with different concerns as described.
These are useful for checking all the different check features are working as expected.
"""
# location = "Test Schedules/test_23_8_awful2.txt"                       # 3,2,1 robot match concerns; unequal appearances; team number in same match twice; no perfect sections.
# location = "Test Schedules/schedule_t12-a4.txt"                        # All concerns for minimum spacing.
location = "Test Schedules/SR2024-final-schedule.txt"                  # Strong and weak concerns for both minimum and maximum spacing.
# location = "Test Schedules/SR2024-final-schedule_optimised.txt"        # Perfect facings.
# location = "Test Schedules/SR2023-yabms-36.txt"                        # Perfect corner standard deviation.
# location = "Test Schedules/schedule_t24-a12_2.txt"                     # Terrible corner standard deviation.
# location = "Test Schedules/schedule_overlaps_bad.txt"                  # Couple of partial overlaps and 1 full overlap
# location = "Test Schedules/schedule_overlaps_awful.txt"                # Lots and lots of partial and full overlaps
# location = "Test Schedules/schedule_t27-a12_3.txt"                     # Completely perfect facings and repeats (each team faces 36 opponents across their 12 appearances - every single team plays 16 teams once and 10 teams twice)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs='?', help="Provide the location of a .txt schedule to run the checks on it", default="")
    parser.add_argument("--arenas", type=int, help="Number of arenas, just used for making sure the match spacing is still accurate", default=1)
    args = parser.parse_args()
    NUMBER_OF_ARENAS = args.arenas
    if os.path.isfile(args.location):
        match_schedule = import_schedule(args.location)
        interact_with_checks(match_schedule)
    elif os.path.isfile(location):
        match_schedule = import_schedule(location)
        interact_with_checks(match_schedule)
    else:
        print("No schedule found at that location.")