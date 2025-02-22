MATCH_SPACING_WEIGHTING_OVERALL = 0.5
FACINGS_WEIGHTING_OVERALL = 0.5
OVERLAP_WEIGHTING_OVERALL = FACINGS_WEIGHTING_OVERALL
OVERLAP_3_WEIGHTING = 15     #Each overlapped match of 3 will get a weighting of 3*15=45.
OVERLAP_4_WEIGHTING = 2      #Each match will get +188 weighting: +180 for overlapped matches above for each group of 3 numbers in the match + 4*2 for identical.

NUMBER_OF_TEAMS_PER_MATCH = 4
NUMBER_OF_ARENAS = 1

INCREMENT_SPACING_CHECK = False      #If True, 1 is added to all the spacing results to match these checks: 
COLOURED_TEXT = True
FIRST_MATCH_IS_MATCH_ZERO = False    #If True, the first match is referred to as match 0; otherwise the first match is match 1.