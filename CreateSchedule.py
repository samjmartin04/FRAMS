import copy
import time
import math
import argparse

from GlobalConstants import *
from GeneralFunctions import *
from CheckSchedule import interact_with_checks

time_taken_spacing, time_taken_facings, time_taken_overlap, time_taken_shuffling = 0, 0, 0, 0

#Various scores from schedule::

def get_overall_corner_score_from_schedule(match_schedule, in_blocks=False):
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule, in_blocks)
    overall_score = 0
    for specific_team_number in list_of_team_numbers:
        #get_corner_score()
        target_number = get_appearances_from_schedule(match_schedule, in_blocks)/NUMBER_OF_TEAMS_PER_MATCH
        corners_data = []
        for _ in range(NUMBER_OF_TEAMS_PER_MATCH):
            corners_data.append(0)
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
        corner_score = 0
        #corner_score += np.std(corners_data)   #option to add/just do std on corners data.
        for corner_count in corners_data:
            if corner_count < target_number:
                corner_score += (target_number-corner_count)**3     #Lower than target corners. Could increase 3 a little if you want to make sure each team plays in each corner at least once.
            else:
                corner_score += (corner_count-target_number)**3     #Higher than target corners
        overall_score += corner_score
    return overall_score

def get_overall_facings_score_from_schedule(match_schedule, in_blocks=False):
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule, in_blocks)
    number_of_teams = get_number_of_teams_from_schedule(match_schedule, in_blocks)
    number_of_appearances = get_appearances_from_schedule(match_schedule, in_blocks)
    target_repeats = (NUMBER_OF_TEAMS_PER_MATCH-1)*number_of_appearances/number_of_teams
    #get_facings_data()
    facings_data = {}
    for team_number in list_of_team_numbers:
        facings_data[team_number] = 0
    
    facings_data[-1] = 0    #Extra one for -1 to avoid having to check for every single team_number in a match.
    facings_data[0] = 0     #Might need to look at a better way of doing this.

    facings_data_all = []
    for team_number in list_of_team_numbers:
        facings_data_all.append(facings_data.copy())

    if in_blocks:
        for league_block in match_schedule:
            for match in league_block:
                for specific_team_number in match:
                    if specific_team_number > 0:
                        for team_number in match:
                            facings_data_all[specific_team_number-1][team_number] += 1
    else:
        for match in match_schedule:
            for specific_team_number in match:
                if specific_team_number > 0:
                    for team_number in match:
                        facings_data_all[specific_team_number-1][team_number] += 1

    #analyse_facings_data()
    facing_repeats_data = [0]   #Accounts for facing a team 0 times.
    for n in range(number_of_appearances):
        facing_repeats_data.append(0)   #Accounts for facing a team up to the number of appearances times.

    for m, facings_data in enumerate(facings_data_all):
        for team_number in list_of_team_numbers:
            if team_number != (m+1):
                facing_repeats_data[facings_data[team_number]] += 1

    sum_weighting = 0
    for n in range(number_of_appearances+1):
        sum_weighting += facing_repeats_data[n] * (math.exp(2*(target_repeats-n)) + math.exp(2.25*(n-target_repeats)))
    weighting_for_zero = (math.exp(2*(target_repeats-0)) + math.exp(2.25*(0-target_repeats)))
    if weighting_for_zero < 20:
        sum_weighting += (20 - weighting_for_zero) * facing_repeats_data[0]
    return 0.58*FACINGS_WEIGHTING_OVERALL*sum_weighting

def get_overall_overlap_score_from_schedule(match_schedule, in_blocks=False):
    #get_overlap_data()
    if NUMBER_OF_TEAMS_PER_MATCH == 4:
        match_list_3_all = []
        match_list_4_all = []
        match_list_3_unique = set()
        match_list_4_unique = set()
        if in_blocks:
            for league_block in match_schedule:
                for match in league_block:
                    match_temp = match.copy()
                    match_temp_1 = match_temp
                    match_temp_1.sort()
                    match_list_4_all.append(match_temp_1)
                    match_list_4_unique.add(tuple(match_temp_1))
                    
                    match_temp_1 = [match_temp[0], match_temp[1], match_temp[2]]
                    match_temp_1.sort()
                    match_list_3_all.append(match_temp_1)
                    match_list_3_unique.add(tuple(match_temp_1))
                    match_temp_1 = [match_temp[0], match_temp[1], match_temp[3]]
                    match_temp_1.sort()
                    match_list_3_all.append(match_temp_1)
                    match_list_3_unique.add(tuple(match_temp_1))
                    match_temp_1 = [match_temp[0], match_temp[2], match_temp[3]]
                    match_temp_1.sort()
                    match_list_3_all.append(match_temp_1)
                    match_list_3_unique.add(tuple(match_temp_1))
                    match_temp_1 = [match_temp[1], match_temp[2], match_temp[3]]
                    match_temp_1.sort()
                    match_list_3_all.append(match_temp_1)
                    match_list_3_unique.add(tuple(match_temp_1))
        else:
            for match in match_schedule:
                match_temp = match.copy()
                match_temp_1 = match_temp
                match_temp_1.sort()
                match_list_4_all.append(match_temp_1)
                match_list_4_unique.add(tuple(match_temp_1))
                
                match_temp_1 = [match_temp[0], match_temp[1], match_temp[2]]
                match_temp_1.sort()
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_temp_1 = [match_temp[0], match_temp[1], match_temp[3]]
                match_temp_1.sort()
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_temp_1 = [match_temp[0], match_temp[2], match_temp[3]]
                match_temp_1.sort()
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))
                match_temp_1 = [match_temp[1], match_temp[2], match_temp[3]]
                match_temp_1.sort()
                match_list_3_all.append(match_temp_1)
                match_list_3_unique.add(tuple(match_temp_1))

        number_of_overlaps_3 = len(match_list_3_all)-len(match_list_3_unique)
        number_of_overlaps_4 = len(match_list_4_all)-len(match_list_4_unique)

        #overlap_score()
        weighting = 0
        weighting += number_of_overlaps_3*OVERLAP_3_WEIGHTING*3
        weighting += number_of_overlaps_4*OVERLAP_4_WEIGHTING*4
    elif NUMBER_OF_TEAMS_PER_MATCH == 2:
        weighting = 0
    else:
        weighting = 0
    return OVERLAP_WEIGHTING_OVERALL*weighting

def get_overall_spacing_score_from_schedule(match_schedule, in_blocks=False):
    number_of_teams = get_number_of_teams_from_schedule(match_schedule, in_blocks)
    list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule, in_blocks)

    #get_match_spacing()
    last_match_number = {}
    spacings_data = []
    for team_number in list_of_team_numbers:
        last_match_number[team_number] = -1

    if NUMBER_OF_ARENAS > 0:
        counter = 0
        half_counter = 0
        if in_blocks:
            for league_block in match_schedule:
                for match in league_block:
                    for team_number in match:
                        if team_number > 0:
                            if last_match_number[team_number] > -1:
                                previous_match_number = last_match_number[team_number]
                                spacings_data.append(counter-previous_match_number-1)
                            last_match_number[team_number] = counter
                    half_counter += 1
                    if half_counter == NUMBER_OF_ARENAS:
                        counter += 1
                        half_counter = 0
        else:
            for match in match_schedule:
                for team_number in match:
                    if team_number > 0:
                        if last_match_number[team_number] > -1:
                            previous_match_number = last_match_number[team_number]
                            spacings_data.append(counter-previous_match_number-1)
                        last_match_number[team_number] = counter
                half_counter += 1
                if half_counter == NUMBER_OF_ARENAS:
                    counter += 1
                    half_counter = 0
    else:
        counter = 0
        if in_blocks:
            for league_block in match_schedule:
                for match in league_block:
                    for team_number in match:
                        if team_number > 0:
                            if last_match_number[team_number] > -1:
                                previous_match_number = last_match_number[team_number]
                                spacings_data.append(counter-previous_match_number-1)
                            last_match_number[team_number] = counter
                    counter += 1
        else:
            for match in match_schedule:
                for team_number in match:
                    if team_number > 0:
                        if last_match_number[team_number] > -1:
                            previous_match_number = last_match_number[team_number]
                            spacings_data.append(counter-previous_match_number-1)
                        last_match_number[team_number] = counter
                counter += 1

    #match_spacing_score()
    match_spacing_target = (number_of_teams/NUMBER_OF_TEAMS_PER_MATCH)-1
    weighting = 0
    for match_spacing in spacings_data:
        weighting += MATCH_SPACING_WEIGHTING_OVERALL * (abs(match_spacing_target-match_spacing)**2 + 4*math.exp((5.5-match_spacing)))
    return weighting


#Various scores from schedule combined::

def get_overall_score_from_schedule(match_schedule, in_blocks=False):
    global time_taken_facings, time_taken_overlap, time_taken_spacing
    overall_weighting = 0
    start_time = time.time()
    overall_weighting += get_overall_spacing_score_from_schedule(match_schedule, in_blocks)
    end_time = time.time()
    time_taken_spacing += end_time-start_time
    start_time = time.time()
    overall_weighting += get_overall_facings_score_from_schedule(match_schedule, in_blocks)
    end_time = time.time()
    time_taken_facings += end_time-start_time
    start_time = time.time()
    overall_weighting += get_overall_overlap_score_from_schedule(match_schedule, in_blocks)
    end_time = time.time()
    time_taken_overlap += end_time-start_time
    return overall_weighting


#Corner Stuff::

def change_corner_order(match, adjust_num):
    if NUMBER_OF_TEAMS_PER_MATCH == 4:
        c0, c1, c2, c3 = match
        if adjust_num == 0:
            return [c0, c1, c2, c3]
        elif adjust_num == 1:
            return [c0, c1, c3, c2]
        elif adjust_num == 2:
            return [c0, c2, c1, c3]
        elif adjust_num == 3:
            return [c0, c2, c3, c1]
        elif adjust_num == 4:
            return [c0, c3, c1, c2]
        elif adjust_num == 5:
            return [c0, c3, c2, c1]
        elif adjust_num == 6:
            return [c1, c0, c2, c3]
        elif adjust_num == 7:
            return [c1, c0, c3, c2]
        elif adjust_num == 8:
            return [c1, c2, c0, c3]
        elif adjust_num == 9:
            return [c1, c2, c3, c0]
        elif adjust_num == 10:
            return [c1, c3, c0, c2]
        elif adjust_num == 11:
            return [c1, c3, c2, c0]
        elif adjust_num == 12:
            return [c2, c0, c1, c3]
        elif adjust_num == 13:
            return [c2, c0, c3, c1]
        elif adjust_num == 14:
            return [c2, c1, c0, c3]
        elif adjust_num == 15:
            return [c2, c1, c3, c0]
        elif adjust_num == 16:
            return [c2, c3, c0, c1]
        elif adjust_num == 17:
            return [c2, c3, c1, c0]
        elif adjust_num == 18:
            return [c3, c0, c1, c2]
        elif adjust_num == 19:
            return [c3, c0, c2, c1]
        elif adjust_num == 20:
            return [c3, c1, c0, c2]
        elif adjust_num == 21:
            return [c3, c1, c2, c0]
        elif adjust_num == 22:
            return [c3, c2, c0, c1]
        elif adjust_num == 23:
            return [c3, c2, c1, c0]
        else:
            return match
    elif NUMBER_OF_TEAMS_PER_MATCH == 2:
        c0, c1 = match
        if adjust_num == 0:
            return [c0, c1]
        elif adjust_num == 1:
            return [c1, c0]
    else:
        return match

def shuffle_corners_specific_block(match_schedule, block_num):
    n = 0
    while n < len(match_schedule[block_num]):
        match = match_schedule[block_num][n]
        test_schedule = copy.deepcopy(match_schedule)
        current_best_schedule = copy.deepcopy(test_schedule)
        current_best_score = get_overall_corner_score_from_schedule(test_schedule, True)
        for p in range(1, math.factorial(NUMBER_OF_TEAMS_PER_MATCH)):   # The range goes from 1 to n! as 0 is the current corner ordering (i.e. the current best score)
            test_schedule[block_num][n] = change_corner_order(match, p)
            test_score = get_overall_corner_score_from_schedule(test_schedule, True)
            if test_score < current_best_score:
                current_best_score = test_score
                current_best_schedule = copy.deepcopy(test_schedule)
        match_schedule = copy.deepcopy(current_best_schedule)
        n += 1
    return match_schedule

def shuffle_corners_whole_schedule(match_schedule, in_blocks=False):
    if in_blocks:
        m = 0
        while m < len(match_schedule):
            n = 0
            while n < len(match_schedule[m]):
                match = match_schedule[m][n]
                test_schedule = copy.deepcopy(match_schedule)
                current_best_schedule = copy.deepcopy(test_schedule)
                current_best_score = get_overall_corner_score_from_schedule(test_schedule, True)
                for p in range(1, math.factorial(NUMBER_OF_TEAMS_PER_MATCH)):   # The range goes from 1 to n! as 0 is the current corner ordering (i.e. the current best score)
                    test_schedule[m][n] = change_corner_order(match, p)
                    test_score = get_overall_corner_score_from_schedule(test_schedule, True)
                    if test_score < current_best_score:
                        current_best_score = test_score
                        current_best_schedule = copy.deepcopy(test_schedule)
                match_schedule = copy.deepcopy(current_best_schedule)
                n += 1
            m += 1
    else:
        n = 0
        while n < len(match_schedule):
            match = match_schedule[n]
            test_schedule = copy.deepcopy(match_schedule)
            current_best_schedule = copy.deepcopy(test_schedule)
            current_best_score = get_overall_corner_score_from_schedule(test_schedule)
            for p in range(1, math.factorial(NUMBER_OF_TEAMS_PER_MATCH)):   # The range goes from 1 to n! as 0 is the current corner ordering (i.e. the current best score)
                test_schedule[n] = change_corner_order(match, p)
                test_score = get_overall_corner_score_from_schedule(test_schedule)
                if test_score < current_best_score:
                    current_best_score = test_score
                    current_best_schedule = copy.deepcopy(test_schedule)
            match_schedule = copy.deepcopy(current_best_schedule)
            n += 1
    return match_schedule


#Shuffling specific block::

def shuffle_schedule_specific_block(match_schedule, block_num, optimisation_level=0):
    global time_taken_shuffling
    m = 0
    while m < len(match_schedule[block_num]):
        for n in range(NUMBER_OF_TEAMS_PER_MATCH):
            specific_team_number = match_schedule[block_num][m][n]

            current_best_schedule = copy.deepcopy(match_schedule)
            current_best_score = get_overall_score_from_schedule(match_schedule, True)

            p = 0
            while p < len(match_schedule[block_num]):
                if optimisation_level == 2:
                    index = p-2
                    total_count = 5
                elif optimisation_level == 1:
                    index = p-1
                    total_count = 3
                else:
                    index = p
                    total_count = 1
                
                if_test = True
                if index < 0:
                    count = -index
                else:
                    count = 0
                while count < total_count:
                    try:
                        if specific_team_number in match_schedule[block_num][index+count] and (index+count) != m:
                            if_test = False
                            break
                    except:
                        pass
                    count += 1

                if if_test:
                    for q in range(NUMBER_OF_TEAMS_PER_MATCH):
                        if optimisation_level == 2:
                            index = m-2
                            total_count = 5
                        elif optimisation_level == 1:
                            index = m-1
                            total_count = 3
                        else:
                            index = m
                            total_count = 1
                        
                        if_test_2 = True
                        if index < 0:
                            count = -index
                        else:
                            count = 0
                        while count < total_count:
                            try:
                                if match_schedule[block_num][p][q] in match_schedule[block_num][index+count] and (index+count) != p:
                                    if_test_2 = False
                                    break
                            except:
                                pass
                            count += 1
                        
                        if if_test_2:
                            start_time = time.time()
                            test_schedule = copy.deepcopy(match_schedule)
                            test_schedule[block_num][m][n] = test_schedule[block_num][p][q]
                            test_schedule[block_num][p][q] = specific_team_number
                            end_time = time.time()
                            test_score = get_overall_score_from_schedule(test_schedule, True)
                            time_taken_shuffling += end_time-start_time
                            if test_score < current_best_score:
                                current_best_schedule = copy.deepcopy(test_schedule)
                                current_best_score = test_score
                p += 1
            match_schedule = copy.deepcopy(current_best_schedule)
        m += 1
    return match_schedule

def shuffle_schedule_specific_block_multiple(match_schedule, block_num, optimisation_level=0, silent=False):
    previous_score = get_overall_score_from_schedule(match_schedule, True)
    unchanged = False
    shuffle_count = 0
    if not silent:
        print(f"({get_current_time()}) Schedule after 0 shuffles has a score of {int(round(previous_score,0))}.")
    while not unchanged:
        start_time = int(time.time())
        match_schedule = shuffle_schedule_specific_block(match_schedule, block_num, optimisation_level)
        shuffle_count += 1
        end_time = int(time.time())
        schedule_score = get_overall_score_from_schedule(match_schedule, True)
        if not silent:
            print(f"({get_current_time()}) Schedule after {shuffle_count} shuffles has a score of {int(round(schedule_score,0))}. The shuffle took {end_time-start_time} seconds.")
        if round(schedule_score, 1) == round(previous_score, 1):
            if not silent:
                print(f"Score is now unchanged after {shuffle_count} shuffles.")
            unchanged = True
        else:
            previous_score = schedule_score
    return match_schedule


#Shuffling whole schedule::

def shuffle_schedule_whole_schedule(match_schedule, optimisation_level=0, in_blocks=False):
    if in_blocks:
        b = 0
        while b < len(match_schedule):
            m = 0
            while m < len(match_schedule[b]):
                for n in range(NUMBER_OF_TEAMS_PER_MATCH):
                    specific_team_number = match_schedule[b][m][n]

                    current_best_schedule = copy.deepcopy(match_schedule)
                    current_best_score = get_overall_score_from_schedule(match_schedule)
                    
                    c = 0
                    while c < len(match_schedule):
                        p = 0
                        while p < len(match_schedule[c]):
                            if optimisation_level == 2:
                                index = p-2
                                total_count = 5
                            elif optimisation_level == 1:
                                index = p-1
                                total_count = 3
                            else:
                                index = p
                                total_count = 1
                            
                            if_test = True
                            if index < 0:
                                count = -index
                            else:
                                count = 0
                            while count < total_count:
                                try:
                                    if specific_team_number in match_schedule[c][index+count] and (index+count) != m:
                                        if_test = False
                                        break
                                except:
                                    pass
                                count += 1
                            
                            if if_test:
                                for q in range(NUMBER_OF_TEAMS_PER_MATCH):
                                    if optimisation_level == 2:
                                        index = m-2
                                        total_count = 5
                                    elif optimisation_level == 1:
                                        index = m-1
                                        total_count = 3
                                    else:
                                        index = m
                                        total_count = 1
                                    
                                    if_test_2 = True
                                    if index < 0:
                                        count = -index
                                    else:
                                        count = 0
                                    while count < total_count:
                                        try:
                                            if match_schedule[c][p][q] in match_schedule[b][index+count] and (index+count) != p:
                                                if_test_2 = False
                                                break
                                        except:
                                            pass
                                        count += 1
                                    
                                    if if_test_2:
                                        test_schedule = copy.deepcopy(match_schedule)
                                        test_schedule[b][m][n] = test_schedule[c][p][q]
                                        test_schedule[c][p][q] = specific_team_number
                                        test_score = get_overall_score_from_schedule(test_schedule)
                                        if test_score < current_best_score:
                                            current_best_schedule = copy.deepcopy(test_schedule)
                                            current_best_score = test_score
                            p += 1
                        c += 1
                    match_schedule = copy.deepcopy(current_best_schedule)
                m += 1
            b += 1
    else:
        m = 0
        while m < len(match_schedule):
            for n in range(NUMBER_OF_TEAMS_PER_MATCH):
                specific_team_number = match_schedule[m][n]

                current_best_schedule = copy.deepcopy(match_schedule)
                current_best_score = get_overall_score_from_schedule(match_schedule)

                p = 0
                while p < len(match_schedule):
                    if optimisation_level == 2:
                        index = p-2
                        total_count = 5
                    elif optimisation_level == 1:
                        index = p-1
                        total_count = 3
                    else:
                        index = p
                        total_count = 1
                    
                    if_test = True
                    if index < 0:
                        count = -index
                    else:
                        count = 0
                    while count < total_count:
                        try:
                            if specific_team_number in match_schedule[index+count] and (index+count) != m:
                                if_test = False
                                break
                        except:
                            pass
                        count += 1
                    
                    if if_test:
                        for q in range(NUMBER_OF_TEAMS_PER_MATCH):
                            if optimisation_level == 2:
                                index = m-2
                                total_count = 5
                            elif optimisation_level == 1:
                                index = m-1
                                total_count = 3
                            else:
                                index = m
                                total_count = 1
                            
                            if_test_2 = True
                            if index < 0:
                                count = -index
                            else:
                                count = 0
                            while count < total_count:
                                try:
                                    if match_schedule[p][q] in match_schedule[index+count] and (index+count) != p:
                                        if_test_2 = False
                                        break
                                except:
                                    pass
                                count += 1
                            
                            if if_test_2:
                                test_schedule = copy.deepcopy(match_schedule)
                                test_schedule[m][n] = test_schedule[p][q]
                                test_schedule[p][q] = specific_team_number
                                test_score = get_overall_score_from_schedule(test_schedule)
                                if test_score < current_best_score:
                                    current_best_schedule = copy.deepcopy(test_schedule)
                                    current_best_score = test_score
                    p += 1
                match_schedule = copy.deepcopy(current_best_schedule)
            m += 1
    return match_schedule

def shuffle_schedule_whole_schedule_multiple(match_schedule, optimisation_level=0, in_blocks=False, silent=False):
    previous_score = get_overall_score_from_schedule(match_schedule, in_blocks)
    unchanged = False
    shuffle_count = 0
    if not silent:
        print(f"({get_current_time()}) Schedule after 0 shuffles has a score of {int(round(previous_score,0))}.")
    while not unchanged:
        start_time = int(time.time())
        match_schedule = shuffle_schedule_whole_schedule(match_schedule, optimisation_level, in_blocks)
        match_schedule = shuffle_corners_whole_schedule(match_schedule, in_blocks)
        shuffle_count += 1
        #export_schedule_to_txt(match_schedule, f"schedule_t23-a12-s{shuffle_count}.txt")
        end_time = int(time.time())
        schedule_score = get_overall_score_from_schedule(match_schedule, in_blocks)
        if not silent:
            print(f"({get_current_time()}) Schedule after {shuffle_count} shuffles has a score of {int(round(schedule_score,0))}. The shuffle took {end_time-start_time} seconds.")
        if round(schedule_score, 1) == round(previous_score, 1):
            if not silent:
                print(f"Score is now unchanged after {shuffle_count} shuffles.")
            unchanged = True
        else:
            previous_score = schedule_score
    return match_schedule


#Optimising whole schedule::
def optimise_schedule(match_schedule, optimisation_level=0, silent=False):
    match_schedule = shuffle_schedule_whole_schedule_multiple(match_schedule, optimisation_level, False, silent)
    match_schedule = shuffle_corners_whole_schedule(match_schedule, False)
    return match_schedule

def optimise_schedule_from_file(file_location, optimisation_level=0):
    match_schedule = import_schedule(file_location)
    match_schedule = optimise_schedule(match_schedule, optimisation_level)
    export_schedule_to_txt(match_schedule, check_location(f"{file_location[:-4]}_optimised.txt"))
    export_schedule_to_txt(match_schedule, "schedule_optimised.txt")


#Generating schedule::

def generate_schedule(number_of_teams, number_of_appearances, optimisation_level=0, silent=False, match_schedule=[], teams_to_exclude=[]):
    global time_taken_spacing, time_taken_facings, time_taken_overlap, time_taken_shuffling
    time_taken_spacing, time_taken_facings, time_taken_overlap, time_taken_shuffling = 0, 0, 0, 0
    if number_of_teams*number_of_appearances % NUMBER_OF_TEAMS_PER_MATCH == 0:
        fake_teams_to_add = 0
        print(f"Number of matches: {int(number_of_teams*number_of_appearances//NUMBER_OF_TEAMS_PER_MATCH)}")
    else:
        fake_teams_to_add = NUMBER_OF_TEAMS_PER_MATCH - number_of_teams*number_of_appearances % NUMBER_OF_TEAMS_PER_MATCH
        print(f"Number of matches: {int((number_of_teams*number_of_appearances+fake_teams_to_add)//NUMBER_OF_TEAMS_PER_MATCH)}")
    if fake_teams_to_add >= 3:
        fake_3_added = False
    else:
        fake_3_added = True
    if fake_teams_to_add >= 2:
        fake_2_added = False
    else:
        fake_2_added = True
    if fake_teams_to_add >= 1:
        fake_1_added = False
    else:
        fake_1_added = True
    expected_team_occurences = number_of_teams*number_of_appearances + fake_teams_to_add
    
    if number_of_teams%NUMBER_OF_TEAMS_PER_MATCH == 0:
        rounds_per_block = 1
    elif number_of_teams%(NUMBER_OF_TEAMS_PER_MATCH/2) == 0:
        rounds_per_block = 2
    else:
        rounds_per_block = 4
    
    blocks_needed = number_of_appearances/rounds_per_block
    # match_schedule = []
    blocks_added = 0
    while blocks_needed >= 2:
        match_list_unseparated = []
        for m in range(rounds_per_block):
            for t in range(number_of_teams+len(teams_to_exclude)):
                if not t+1 in teams_to_exclude:
                    match_list_unseparated.append(t+1)
        
        league_block = []
        n = 0
        while n < len(match_list_unseparated)/NUMBER_OF_TEAMS_PER_MATCH:
            match_to_append = []
            q = 0
            while q < NUMBER_OF_TEAMS_PER_MATCH:
                match_to_append.append(match_list_unseparated[NUMBER_OF_TEAMS_PER_MATCH*n+q])
                q += 1
            league_block.append(match_to_append)
            n += 1

        match_schedule.append(league_block)
        blocks_added += 1
        print(f"({get_current_time()}) Adding another block...")
        if optimisation_level == 0:
            match_schedule = shuffle_schedule_specific_block_multiple(match_schedule, block_num=-1, optimisation_level=optimisation_level, silent=silent)
        elif optimisation_level == 1:
            match_schedule = shuffle_schedule_specific_block_multiple(match_schedule, block_num=-1, optimisation_level=optimisation_level, silent=silent)
        elif optimisation_level == 2:   #Runs a level 1 optimisation a couple of times to settle down the schedule first.
            # print(f"Before any shuffling: {round(get_overall_score_from_schedule(match_schedule, True),0)}")
            # match_schedule = shuffle_schedule_specific_block(match_schedule, block_num=-1, optimisation_level=1)
            # print(f"After 1 level 1 shuffle: {round(get_overall_score_from_schedule(match_schedule, True),0)}")
            # match_schedule = shuffle_schedule_specific_block(match_schedule, block_num=-1, optimisation_level=1)
            match_schedule = shuffle_schedule_specific_block_multiple(match_schedule, block_num=-1, optimisation_level=optimisation_level, silent=silent)

        match_schedule = shuffle_corners_specific_block(match_schedule, block_num=-1)

        if rounds_per_block == 1:
            add_s = ""
        else:
            add_s = "s"
        print(f"({get_current_time()}) Added another {rounds_per_block} appearance{add_s}. Now on {int(blocks_added*rounds_per_block)} appearances.")
        blocks_needed -= 1
    
    remaining = blocks_needed*rounds_per_block*number_of_teams + fake_teams_to_add
    match_list_unseparated = []
    count = 1
    for m in range(int(rounds_per_block*blocks_needed)):
        for t in range(number_of_teams+len(teams_to_exclude)):
            if not t+1 in teams_to_exclude:
                match_list_unseparated.append(t+1)
                count += 1
                if count/remaining >= 0.33 and not fake_1_added:
                    match_list_unseparated.append(-1)
                    fake_1_added = True
                if count/remaining >= 0.66 and not fake_2_added:
                    match_list_unseparated.append(-1)
                    fake_2_added = True
                if count/remaining >= 0.99 and not fake_3_added:
                    match_list_unseparated.append(-1)
                    fake_3_added = True
    
    if not fake_3_added:
        match_list_unseparated.append(-1)
        fake_3_added = True
    
    league_block = []
    n = 0
    while n < len(match_list_unseparated)/NUMBER_OF_TEAMS_PER_MATCH:
        match_to_append = []
        q = 0
        while q < NUMBER_OF_TEAMS_PER_MATCH:
            match_to_append.append(match_list_unseparated[NUMBER_OF_TEAMS_PER_MATCH*n+q])
            q += 1
        league_block.append(match_to_append)
        n += 1

    # print(f"Last league block: {league_block}")
    
    match_schedule.append(league_block)
    blocks_added += blocks_needed
    print(f"({get_current_time()}) Adding last block...")

    if optimisation_level == 0:
        match_schedule = shuffle_schedule_specific_block_multiple(match_schedule, block_num=-1, optimisation_level=optimisation_level, silent=silent)
    elif optimisation_level == 1:
        match_schedule = shuffle_schedule_specific_block_multiple(match_schedule, block_num=-1, optimisation_level=optimisation_level, silent=silent)
    elif optimisation_level == 2:   #Runs a level 1 optimisation a couple of times to settle down the schedule first.
        # print(f"Before any shuffling: {round(get_overall_score_from_schedule(match_schedule, True),0)}")
        # match_schedule = shuffle_schedule_specific_block(match_schedule, block_num=-1, optimisation_level=1)
        # print(f"After 1 level 1 shuffle: {round(get_overall_score_from_schedule(match_schedule, True),0)}")
        # match_schedule = shuffle_schedule_specific_block(match_schedule, block_num=-1, optimisation_level=1)
        match_schedule = shuffle_schedule_specific_block_multiple(match_schedule, block_num=-1, optimisation_level=optimisation_level, silent=silent)

    match_schedule = shuffle_corners_specific_block(match_schedule, block_num=-1)

    print(f"({get_current_time()}) Added a final {int(blocks_needed*rounds_per_block)} appearances. Total is {int(blocks_added*rounds_per_block)} appearances.")

    time_taken_total = time_taken_spacing + time_taken_facings + time_taken_overlap + time_taken_shuffling
    print("\nTime taken Summary:")
    print(f"Spacing  : {round(time_taken_spacing,1):5.1f}s, {round(100*time_taken_spacing/time_taken_total,1):4.1f}%")
    print(f"Facings  : {round(time_taken_facings,1):5.1f}s, {round(100*time_taken_facings/time_taken_total,1):4.1f}%")
    print(f"Overlap  : {round(time_taken_overlap,1):5.1f}s, {round(100*time_taken_overlap/time_taken_total,1):4.1f}%")
    print(f"Shuffling: {round(time_taken_shuffling,1):5.1f}s, {round(100*time_taken_shuffling/time_taken_total,1):4.1f}%")

    return match_schedule


def check_score_schedules():
    """
    Various different schedules with different features to check the schedule score remains unchanged when adjusting score code.
    Expected values:
    2373.546196754647
    2214.7693621679628
    2353.3952133447156
    3523.2019777239598
    12006.54686138994
    10235.060453701393
    14288.865446264084
    7540.193427062924
    2719.7453304795813
    3155.4295571267785
    251310830268.26132
    12758.791257933002
    For these, spacing and facings weightings are both 0.5, arenas is 1, overlap_3_weighting is 15, and overlap_4_weighting is 2.
    """
    match_schedule = import_schedule("Test Schedules/schedule_t30-a12_10.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/schedule_t25-a7_6.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/schedule_t19-a7.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/schedule_t36-a10_2.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/SR2024-final-schedule.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/SR2023-yabms-36.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/SR2023-yabms-30.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/SR2023-yabms-24.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/schedule_overlaps.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/schedule_overlaps_bad.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/schedule_overlaps_awful.txt")
    print(get_overall_score_from_schedule(match_schedule))
    match_schedule = import_schedule("Test Schedules/test_23_8_awful.txt")
    print(get_overall_score_from_schedule(match_schedule))


if __name__ == '__main__':
    #check_score_schedules()
 
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--teams", type=int, help="Number of teams required", required=True)
    parser.add_argument("-a", "--appearances", type=int, help="Number of appearances per team", required=True)
    parser.add_argument("-l", "--location", help="Location of schedule", default="")
    parser.add_argument("-s", "--spacing", type=float, help="Spacing factor", default=0.5)
    parser.add_argument("-f", "--facings", type=float, help="Facings factor", default=0.5)
    parser.add_argument("--arenas", type=int, help="Number of arenas, just used for making sure the match spacing is still accurate", default=1)
    parser.add_argument("-m", "--speed_mode", type=int, help="Speed mode. 0 is slowest; 2 is fastest", default=1, choices=[0,1,2])
    args = parser.parse_args()

    number_of_teams = args.teams
    number_of_appearances = args.appearances
    NUMBER_OF_ARENAS = args.arenas
    speed_mode = args.speed_mode
    total = args.spacing + args.facings
    spacing_ratio = args.spacing/total
    facings_ratio = args.facings/total

    location_name = args.location
    
    if location_name == "":
        location_name = f"Schedules/schedule_t{number_of_teams}-a{number_of_appearances}.txt"
        location = check_location(location_name)
    
    program_start = int(time.time())
    match_schedule = generate_schedule(number_of_teams, number_of_appearances, optimisation_level=speed_mode, silent=True)

    match_schedule = remove_league_blocks_from_schedule(match_schedule)

    match_schedule = shuffle_corners_whole_schedule(match_schedule, False)

    export_schedule_to_txt(match_schedule, location, False)
    schedule_score = int(round(get_overall_score_from_schedule(match_schedule, False),0))

    program_end = int(time.time())
    total_time = program_end-program_start
    program_time_mins, program_time_secs = total_time//60, round((total_time/60 - total_time//60)*60, 0)
    time_taken = f"{int(program_time_mins):02d}:{int(program_time_secs):02d}"
    print(f"\nSchedule for {number_of_teams} teams with {number_of_appearances} appearances each took {time_taken} (min:sec) to generate. Saved as {location}. Schedule score: {schedule_score}.")

    response = input("Press enter to continue and view a summary of the checks...")

    interact_with_checks(match_schedule)

