from GlobalConstants import *
from GeneralFunctions import *
from CheckSchedule import *
#from CreateSchedule import optimise_schedule_from_file, optimise_schedule, generate_schedule
from CreateSchedule import *

while True:
    response = input("\nC  Check Schedule\nG  Generate Schedule\nM  Modify existing schedule\nO  Optimise Schedule\nS  Settings\n\nChoose option: ")

    if response == "":
        break
    elif response.casefold()[:1] == "c":
        found_schedule = False
        while not found_schedule:
            response = input("Please enter the path to the schedule: ")
            if os.path.isfile(response):
                found_schedule = True
                match_schedule = import_schedule(response)
                interact_with_checks(match_schedule)
            else:
                print("No schedule found at that location. Please try again.")
    elif response.casefold()[:1] == "g":
        print("\nGenerate Schedule:\n")
        number_of_teams_int_check = True
        while number_of_teams_int_check:
            number_of_teams = input("Number of Teams: ")
            try:
                number_of_teams = int(number_of_teams)
                number_of_teams_int_check = False
            except:
                print("Please enter a number.")
        
        number_of_appearances_int_check = True
        while number_of_appearances_int_check:
            number_of_appearances = input("Number of Appearances: ")
            try:
                number_of_appearances = int(number_of_appearances)
                number_of_appearances_int_check = False
            except:
                print("Please enter a number.")
        schedule_priority = input("Would you like to prioritise (S)pacing, (B)alanced, (F)acings, or (C)ustom: ")
        if schedule_priority == "":
            schedule_priority = "b"
        
        if schedule_priority.casefold()[:1] == "b":
            spacing_ratio = 0.5
            facings_ratio = 0.5
        elif schedule_priority.casefold()[:1] == "s":
            spacing_ratio = 0.65
            facings_ratio = 0.35
        elif schedule_priority.casefold()[:1] == "f":
            spacing_ratio = 0.35
            facings_ratio = 0.65
        elif schedule_priority.casefold()[:1] == "c":
            response_spacing = input("What spacing ratio would you like: ")
            response_facings = input("What facings ratio would you like: ")
            try:
                response_spacing = float(response_spacing)
                response_facings = float(response_facings)
                total = response_spacing + response_facings
                spacing_ratio = response_spacing/total
                facings_ratio = response_facings/total
            except:
                print("Error using your requested ratios, using balanced instead.")
                spacing_ratio = 0.5
                facings_ratio = 0.5
        else:
            spacing_ratio = 0.5
            facings_ratio = 0.5

        speed_mode = input("What speed mode would you like to use? 0, 1 (rec.), or 2: ")
        if speed_mode == "0":
            speed_mode = 0
        elif speed_mode == "1":
            speed_mode = 1
        elif speed_mode == "2":
            speed_mode = 2
        else:
            speed_mode = 1  #Default speed_mode if nothing else given.

        location_name = input("File/location for schedule (must end in .txt): ")
        if location_name == "":
            if os.path.isdir("Schedules"):
                location_name = f"Schedules/schedule_t{number_of_teams}-a{number_of_appearances}.txt"
            else:
                location_name = f"schedule_t{number_of_teams}-a{number_of_appearances}.txt"
        
        location = check_location(location_name)

        program_start = int(time.time())
        start_schedule = []
        start_exclude_list = []
        match_schedule = generate_schedule(number_of_teams, number_of_appearances, optimisation_level=speed_mode, silent=True, match_schedule=start_schedule, teams_to_exclude=start_exclude_list)

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
    elif response.casefold()[:1] == "m":
        print("")
        found_schedule = False
        while not found_schedule:
            old_schedule_location = input("Path of schedule to add to: ")
            if os.path.isfile(old_schedule_location):
                found_schedule = True
                match_schedule_old = import_schedule(old_schedule_location)
            else:
                print("No schedule found at that location. Please try again.")
        
        truncate_schedule_check = True
        number_of_teams_old_schedule = get_number_of_teams_from_schedule(match_schedule_old)
        while truncate_schedule_check:
            response = input("Truncate schedule using (A)ppearance number, (M)atch Number, (N)o truncation? Response (A/M/N): ")
            if response.casefold()[:1] == "a":
                crop_appearances = int(input("(Minimum) number of appearances before cut-off: "))
                num_appearances = get_appearances_from_schedule(match_schedule_old)
                exclude_from_appearance_check = []
                for specific_team_number in list_of_team_numbers:
                    appearances_for_team = get_appearances_data(cropped_schedule, specific_team_number)
                    if appearances_for_team != num_appearances:
                        exclude_from_appearance_check.append(specific_team_number)
                list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule_old)
                success = False
                n = 1
                while n < len(match_schedule_old)+1 and not success:
                    success_n = True
                    cropped_schedule = match_schedule_old[:n]
                    for specific_team_number in list_of_team_numbers:
                        if not specific_team_number in exclude_from_appearance_check:
                            appearances_for_team = get_appearances_data(cropped_schedule, specific_team_number)
                            if appearances_for_team != crop_appearances:
                                success_n = False
                                break
                    if success_n:
                        success = True
                    else:
                        n += 1
                if success:
                    match_schedule = [match_schedule_old[:n]]
                    print(f"Successfully cut the existing schedule to have only {n} matches, which gives {crop_appearances} appearances per team.")
                    truncate_schedule_check = False
                else:
                    print("Failed to cut the match schedule for that number of appearances. Please try a different number of appearances.")
            elif response.casefold()[:1] == "m":
                crop_match_num = int(input("(Minimum) number of matches before cut-off: "))
                list_of_team_numbers = get_list_of_team_numbers_from_schedule(match_schedule_old)
                num_appearances = get_appearances_from_schedule(match_schedule_old)
                exclude_from_appearance_check = []
                for specific_team_number in list_of_team_numbers:
                    appearances_for_team = get_appearances_data(match_schedule_old, specific_team_number)
                    if appearances_for_team != num_appearances:
                        exclude_from_appearance_check.append(specific_team_number)
                success = False
                n = crop_match_num
                while n < len(match_schedule_old)+1 and not success:
                    cropped_schedule = match_schedule_old[:n]
                    appearances_dict = {}                    
                    for specific_team_number in list_of_team_numbers:
                        appearances_for_team = get_appearances_data(cropped_schedule, specific_team_number)
                        if not specific_team_number in exclude_from_appearance_check:
                            if appearances_for_team in appearances_dict.keys():
                                appearances_dict[appearances_for_team] += 1
                            else:
                                appearances_dict[appearances_for_team] = 1
                    number_of_teams = get_number_of_teams_from_schedule(match_schedule_old)
                    for key in appearances_dict.keys():
                        if appearances_dict[key] == number_of_teams-len(exclude_from_appearance_check) and key > 0:
                            success = True
                    if n == len(match_schedule_old):
                        success = False
                        break
                    if not success:
                        n += 1

                if success:
                    crop_appearances = key
                    print(f"Successfully cut the existing schedule to have only {n} matches, which gives {crop_appearances} appearances per team.")
                    truncate_schedule_check = False
                else:
                    print("Failed to find a point to crop the schedule after that number of matches that gave all teams the same number of appearances.")
                match_schedule = [match_schedule_old[:n]]
            elif response.casefold()[:1] == "n":
                truncate_schedule_check = False
                crop_appearances = get_appearances_from_schedule(match_schedule_old)
                match_schedule = [match_schedule_old]

        number_of_teams_int_check = True
        while number_of_teams_int_check:
            number_of_teams = input("Number of Teams: ")
            try:
                number_of_teams = int(number_of_teams)
                number_of_teams_int_check = False
            except:
                print("Please enter a number.")
            
        teams_to_exclude_text = input("Team numbers to exclude: ")
        teams_to_exclude = number_array_from_list(teams_to_exclude_text)

        if len(teams_to_exclude) == (number_of_teams_old_schedule-number_of_teams):
            number_to_exclude = number_of_teams_old_schedule
            while number_to_exclude > number_of_teams:
                teams_to_exclude.append(number_to_exclude)
                number_to_exclude -= 1

        unique_teams_to_exclude = set()
        for team_number in exclude_from_appearance_check:
            unique_teams_to_exclude.add(team_number)
        
        for team_number in teams_to_exclude:
            unique_teams_to_exclude.add(team_number)
        
        if number_of_teams > number_of_teams_old_schedule:
            number_to_exclude = number_of_teams_old_schedule+1
            while number_to_exclude <= number_of_teams:
                unique_teams_to_exclude.add(number_to_exclude)
                number_to_exclude += 1
        
        teams_to_exclude_from_checks = list(unique_teams_to_exclude)
        
        number_of_appearances_int_check = True
        old_appearances = get_appearances_from_schedule(match_schedule_old)
        recommended_appearances = old_appearances-key
        if recommended_appearances > 0:
            recommended_appearances_text = print(f"Recommended number of additional appearances is {recommended_appearances}")
        while number_of_appearances_int_check:
            number_of_appearances = input("Number of additional Appearances: ")
            try:
                number_of_appearances = int(number_of_appearances)
                number_of_appearances_int_check = False
            except:
                print("Please enter a number.")
        
        schedule_priority = input("Would you like to prioritise (S)pacing, (B)alanced, (F)acings, or (C)ustom: ")
        if schedule_priority == "":
            schedule_priority = "b"
        
        if schedule_priority.casefold()[:1] == "b":
            spacing_ratio = 0.5
            facings_ratio = 0.5
        elif schedule_priority.casefold()[:1] == "s":
            spacing_ratio = 0.65
            facings_ratio = 0.35
        elif schedule_priority.casefold()[:1] == "f":
            spacing_ratio = 0.35
            facings_ratio = 0.65
        elif schedule_priority.casefold()[:1] == "c":
            response_spacing = input("What spacing ratio would you like: ")
            response_facings = input("What facings ratio would you like: ")
            try:
                response_spacing = float(response_spacing)
                response_facings = float(response_facings)
                total = response_spacing + response_facings
                spacing_ratio = response_spacing/total
                facings_ratio = response_facings/total
            except:
                print("Error using your requested ratios, using balanced instead.")
                spacing_ratio = 0.5
                facings_ratio = 0.5
        else:
            spacing_ratio = 0.5
            facings_ratio = 0.5
        
        speed_mode = 1

        location_name = input("File/location for new schedule (must end in .txt): ")
        if location_name == "":
            location_name = f"{old_schedule_location[:-4]}_modified.txt"
        
        location = check_location(location_name)

        program_start = int(time.time())
        match_schedule = generate_schedule(number_of_teams, number_of_appearances, optimisation_level=speed_mode, silent=True, match_schedule=match_schedule, teams_to_exclude=teams_to_exclude)

        match_schedule = remove_league_blocks_from_schedule(match_schedule)

        export_schedule_to_txt(match_schedule, location, False)
        schedule_score = int(round(get_overall_score_from_schedule(match_schedule, False),0))

        program_end = int(time.time())
        total_time = program_end-program_start
        program_time_mins, program_time_secs = total_time//60, round((total_time/60 - total_time//60)*60, 0)
        time_taken = f"{int(program_time_mins):02d}:{int(program_time_secs):02d}"
        print(f"\nAdded {number_of_teams} teams, each with {number_of_appearances} appearances to schedule. This took {time_taken} (min:sec) to generate. Saved as {location}. Schedule score: {schedule_score}.")

        response = input("Press enter to continue and view a summary of the checks...")

        interact_with_checks(match_schedule, teams_to_exclude_from_checks)
    elif response.casefold()[:1] == "o":
        found_schedule = False
        while not found_schedule:
            response = input("Please enter the path to the schedule you would like to optimise: ")
            if os.path.isfile(response):
                found_schedule = True
                location = response
                match_schedule = import_schedule(location)
                ##ADD THE PREFERENCE (e.g. SPACING/FACINGS PREFERRED) STUFF FROM GENERATING SCHEDULE WHEN THAT WORKS
                response = input("Would you like the optimisation to update you on how it is going? (Y/N): ")
                if response.casefold()[:1] == "y":
                    silent = False
                else:
                    silent = True
                program_start = int(time.time())
                match_schedule = optimise_schedule(match_schedule, 1, silent)
                new_location = check_location(f"{location[:-4]}_optimised.txt")
                export_schedule_to_txt(match_schedule, new_location)

                schedule_score = int(round(get_overall_score_from_schedule(match_schedule, False),0))
                program_end = int(time.time())
                total_time = program_end-program_start
                program_time_mins, program_time_secs = total_time//60, round((total_time/60 - total_time//60)*60, 0)
                time_taken = f"{int(program_time_mins):02d}:{int(program_time_secs):02d}"
                print(f"\nSchedule took {time_taken} (min:sec) to optimise. Saved at new location: {new_location}. Schedule score: {schedule_score}.")

                response = input("Press enter to continue and view a summary of the checks...")

                interact_with_checks(match_schedule)
            else:
                print("No schedule found at that location. Please try again.")

