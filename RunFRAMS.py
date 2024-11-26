from GlobalConstants import *
from GeneralFunctions import *
from CheckSchedule import *
#from CreateSchedule import optimise_schedule_from_file, optimise_schedule, generate_schedule
from CreateSchedule import *

while True:
    response = input("\nG  Generate Schedule\nC  Check Schedule\nO  Optimise Schedule\nS  Settings\n\nChoose option: ")

    if response == "":
        break
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

