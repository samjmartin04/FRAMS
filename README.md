# FRAMS

### Four Robot Automatic Match Scheduler

FRAMS is a four team match scheduler designed for use in [Student Robotics](https://www.studentrobotics.org) competitions.

This README is a guide on how to create schedules, optimise existing schedules, and how to check schedules that have been produced.

Note that some parts are still work in progress and contain some testing code that will be removed when complete.

## Requirements

Python 3 is required. No libraries other than those automatically provided by Python are required for either the schedule generator, optimiser, or checker. It is recommended you use [pypy](https://pypy.org/) rather than normal Python, particularly when generating schedules. This will generate the schedule much more quickly (~4 times faster) when compared to normal Python.

## Creating a schedule

To start, run/open 'RunFRAMS.py'. Remember to use pypy if you can for faster generation of schedules.

Press 'G' and then press enter to enter 'Generating Schedule' mode.

You will then be asked for the number of teams and then the number of appearances.

You will then be asked what you would like to prioritise. If this is your first time creating this schedule, it is recommended you use Balanced as this should give a good balance between spacing and facings. If the schedule produced gives worse spacing than you'd like, you might want to try again but this time prioritising Spacing. If you are creating a schedule for a virtual competition, you may want to prioritise Facings as spacing is much less important for a virtual competition. Custom allows you to choose the weighting between Spacing and Facings. Balanced is 0.5 and 0.5 and Spacing/Facings is 0.65 and 0.35. If you do not enter anything, Balanced is used.

You will then be asked what speed mode you would like to use. In almost all cases, you should use the recommended of 1. 0 and 1 should give identical schedules (unless facings is very heavily prioritised), but 0 will take a little longer. 2 is faster still and can result in better or worse schedules, depending on what is chosen for priority above. If nothing is entered, 1 is used.

You will then be asked for a location for the produced schedule. If this is left blank, the schedule is called 'schedule_t{x}-a{y}.txt' where {x} and {y} are the number of teams and number of appearances respectively and will be saved in the 'Schedules' folder. In either case of a provided location or the default location, if there is already a file with this name '_{z}' will be added before '.txt' where {z} is an integer that is increased until there no file called that name exists.

A schedule will then be generated to your given parameters. When finished, the number of teams, number of appearances, time taken, and name of the schedule file will all be given. You can then press enter to view a summary of the checks. See the Checks section to see more information about these checks. If you are not happy with the schedule produced, you can try the following:
 - Generate a new schedule with different priority - you could use one of the suggest priorities, or fully customise it if you want to just slightly tweak the spacing/facings.
 - Run 'Optimise Schedule' - this will take much longer than generating a new schedule, but can help make small improvements to the schedule if it is nearly satisfactory. It will remove separated league blocks though. See the 'Optimise Schedule' section of this readme for more information.

An alternative way to create a schedule is by running `'CreateSchedule.py'` with --teams (-t), --appearances (-a), --location (-l), --spacing (-s), --facings (-f), --speed_mode (-m), and --areans. --teams and --appearances are required, but everything else is option with the default values of 0.5 for spacing, 0.5 for facings, 1 for speed_mode, and 1 for arenas with the default location as described above are used. For example, running `'CreateSchedule.py' -t 30 -a 10` creates a balanced schedule at the default location with 1 arena for 30 teams each getting 10 appearances.

### Notes about the schedule produced
If the number of teams is a multiple of 4, the schedule is generated the quickest.

The schedule is generated in 'league blocks' that have 1 appearance if the number of teams is a multiple of 4, 2 appearances if the number of appearances is even, and 4 appearances if the number of appearances is odd.

If the generation described above would leave an unsuitable number of appearances left (e.g. 1 appearance with an even number of teams), these appearances will be added into the previous league block to create one (larger) final block (e.g. 3 appearances for the case described).

Occassionally, the number of teams and number of appearances (when multiplied together) do not give a multiple of 4. In this case, some (up to 3) 3 robot matches will be required to complete the schedule. The number of these matches will be minimised to be as low as possible and are always added in the last league block (which is a larger than normal block in this circumstance).

## Checks

The scheduler comes built in with checks for the schedule produced in the 'CheckSchedule.py' file. The checks do not need to be run with pypy as they do not take very long to run and do not require any libraries beyond those provided automatically with Python. If you are using just the checks and not the schedule creator, you still need 'CheckSchedule.py', 'GlobalConstants.py', and 'GeneralFunctions.py'. To run these checks, you can:
 - Press enter after generating a schedule
 - Choose 'C' for Check Schedule in the 'RunFRAMS.py' menu and give the path to the schedule
 - Run `'CheckSchedule.py' 'path/to/schedule.txt'`, where 'path/to/schedule.txt' is the location of the schedule. Note that you can also specify `--arenas 2` to specify that this schedule is being used with 2 arenas.

Throughout the checks, colours are used to give clarity and emphasis for different sections. These colours are:
 - Green - section is perfect.
 - Dark green - ideal/target for that section.
 - Yellow - section could be better, but still perfectly fine to use.
 - Orange - recommended to not use the schedule as section needs significant improvements.
 - Red - do NOT use this schedule. There are critical problems with this schedule that means it will not work for a competition.

However you run the checks, you will first be presented with a summary of these checks. This gives a quick overview for the schedule and highlights any problems. You should aim for the follow to all be green to signify that they are perfect: Number of Appearances; Number of 1/2/3 robot matches; Team in same match twice

If a problem is highlighted or you would like to look in more detail, press 'Y' then enter to see the overview of all the checks. This will give each check in a list and a longer summary for each check, with any problems highlighted. If any problems are highlighted, they will also list the team numbers that have the problem.

If you then want to look in even further detail, you can press 'Y' and then enter again to see the detailed version of all of these checks. The overview will be listed as before, followed by the extra detail, which should help further find the problem or analyse the schedule. If you only wish to look at a specific section in detail, you can enter a different letter corresponding to that section to just view that section in detail.

### Number of appearances

Every team must have the same number of appearances to have a fair match schedule.

### Number of 1/2/3 robot matches

Sometimes, 3 robot matches are required to complete the schedule. These should be minimised as much as possible and should always be less than 4.
There should never be any 1 or 2 robot matches.

Detailed 3 robot check will show which teams are present in these 3 robot matches and if any are present in multiple.

### Team in match multiple times check

This checks that the schedule does not have a team listed twice in the same match, which would cause obvious problems!

### Match overlap

Checks to see if any matches are identical (all 4 teams the same) or partially overlap (3 of the teams are the same). These can sometimes happen, but they should (particularly identical matches) be minimised as much as possible. This makes the schedule fairer for teams and avoids the matches being repetitive for the competitors or the audience.

### Zone allocation check

This section checks that teams have a roughly even distribution of starting zones. This is a more minor check, but the standard deviation should still be minimised to avoid a team always being in the same starting zone.

### Spacing

This checks the spacing teams have between matches. By default, this is given as the number of matches between consecutive matches that contain that team. By setting 'INCREMENT_SPACING_CHECK' to True, this can changed to give the difference in the match numbers of the consecutive matches that contain that team (i.e. 1 more than the default way). For example, if a team has (on, off, off, off, on), the former (default) gives this as a spacing of 3 and the latter gives this as a spacing of 4. Throughout the rest of this section, the default method of spacing counting will be used.

Minimum spacing should ideally be at least 3, as this means teams will always have a decent amount of time between their matches. A spacing of 0 is not suitable for a physical competition as a team would not have time to leave their previous match before staging closes for their next match. A spacing of 1 is very tight for a physical competition as this only gives a team a few minutes between finishing one match and needing to be at staging for the next match. A spacing of 0 could be used for a virtual competition if needed, but this would result in back-to-back matches with the same team, which may not be desirable from a spectator perspective.

Maximum spacing should not be too high to give a more consistent match spacing. With a large maximum spacing, teams can end up with a lot of dead time between some matches and much closer other matches. With a particularly large spacing, teams may feel that there are not enough matches because they are spaced very unevenly. However, maximum spacing is much less important that minimum spacing.

### Facings

This looks at each team in turn and which of the other teams they face. Ideally, you would want each team to face every other team (i.e. not miss any). Sometimes, the number of teams and number of appearances means that teams cannot face all of the teams. In the facings section, the best facings you can have will be listed in brackets as (faces x (y) is best), where x is the number of teams faced and y is the number of teams missed.

Ideally, you also want each team to play each other team an equal amount and not play any teams a significant number of times more than another team. This is captured by the 'repeats' section. Obviously playing each team equally is almost impossible, but you do want to make sure that there are no outlier teams where they are playing the same team many times, as this is very unfair on the weaker team.

## Checks colours

This section explains the colours that can be found in each section of the checks.

### Number of appearances

If all teams have the same number of appearances, it is green; otherwise, it is red.

### Number of 1/2/3 robot matches

If the number of 1 or 2 robot matches is 0, it is green; otherwise, it is red.
If the number of 3 robot matches is the lowest possible, it is green; otherwise it is orange. The lowest possible number of 3 robot matches required is calculated by multiplying the number of teams by the number of appearances. If this product is a multiple of 4, no 3 robot matches are required. Otherwise, the number needed to get the number to the next multiple of 4 is the number of 3 robot matches required.

### Team in match multiple times check

If the number of matches with teams in them multiple times is 0, it is green; otherwise, it is red.

### Match overlap

If the number of overlapping matches (3 out of 4 team numbers are the same across multiple different matches) is 0, it is green; otherwise, it is yellow.
if the number of identical matches (All 4 teams numbers are the same across multiple different matches) is 0, it is green; otherwise, it is orange.

### Zone allocation check

The standard deviation is calculated from the number of times that team starts in each corner. The target standard deviation for the number of appearances is also calculated. If the number of appearances is a multiple of 4, this standard deviation will be 0; otherwise it will be non-zero. This target standard deviation will be shown in dark green, unless all teams have the ideal standard deviation, where it will then be shown in green as the zone allocation check section will be perfect. The other colours are given when the standard deviation is greater than the following values:

 - Red: standard deviation > 3.0
 - Orange: standard deviation > 1.8
 - Yellow: standard deviation > 1.4

### Spacing

Note that for this whole part, the spacing will be given as the number of matches between matches, such that a spacing of 3 is (on, off, off, off, on).

For minimum spacing, the following numbers are used if the spacing is equal to these numbers:

 - Red: minimum spacing of 0
 - Orange: minimum spacing of 1
 - Yellow: minimum spacing of 2

For maximum spacing, the ideal spacing is first calculating. This is given by: $\textrm{spacing}_\textrm{target}$ = $\frac{\textrm{N}^\textrm{o}\textrm{teams}}{4} - 1$. The maximum spacing is then coloured by the following rules:

 - Orange: $\textrm{spacing}\_\textrm{max} > 3 \times \textrm{spacing}_\textrm{target}$
 - Yellow: $\textrm{spacing}\_\textrm{max} > 2 \times \textrm{spacing}_\textrm{target} + 1$

For average spacing, the team(s) whose average spacing is closest to the $\textrm{spacing}_\textrm{target}$ calculated above are coloured in dark green.

### Facings

For the facings section, the best possible facing for the number of teams and number of appearances is determined. With enough appearances, this will result in all teams being played and 0 misses, but with fewer appearances, the best possible facing is limited by the number of appearances. Teams with this best facing are coloured dark green. If all teams have this best facing, then it will be coloured green as this section is perfect. The other colours are given as follows when the number of teams faced ("facing") is worse than given:

 - Red: $\textrm{facing} < \textrm{facing}_\textrm{best}-10$
 - Orange: $\textrm{facing} < \textrm{facing}_\textrm{best}-6$
 - Yellow: $\textrm{facing} < \textrm{facing}_\textrm{best}-4$

For repeats, the ideal number of times a team should be faced is calculated: $\textrm{repeat}_\textrm{target} = \frac{3 \times \textrm{N}^\textrm{o}\textrm{appearances}}{\textrm{N}^\textrm{o}\textrm{teams}}$. The colours are then given when a team plays at least one team more than that many of times:

 - Red: $\textrm{N}^\textrm{o}\textrm{repeats} > \textrm{repeat}_\textrm{target}+4$
 - Orange: $\textrm{N}^\textrm{o}\textrm{repeats} > \textrm{repeat}_\textrm{target}+2$
 - Yellow: $\textrm{N}^\textrm{o}\textrm{repeats} > \textrm{repeat}_\textrm{target}+1$

## Optimise Schedule

If the schedule generated is not satisfactory and you have already tried generating the schedule again with slightly different priorities, or you have a schedule already, you can try to optimise the schedule. Optimising the schedule will take a while and, depending on the base schedule, may only give slight improvements. After entering the location of the schedule you wish to optimise, you will be given the option of what priority you would like. The priority is the same as described in the 'Creating a Schedule' section. If you are optimsing a schedule that has been generated using FRAMS, it is important to use the same priorities. 

Note: optimising a schedule will mix any (league) blocks in your schedule. If your schedule creates distinct blocks for the league and you wish to not have these blocks merge togther, then you should not optimise the schedule.

## Add to existing schedule

This features enables you to add additional matches to an already existing schedule. This allows for adding a few more appearances to a schedule without having to completely generate a new one. Depending on the number of teams and number of appearances to add, this may result in more than the optimal number of 3 robot matches than would be expected for the overall numbers of appearances for the number of teams in the whole schedule.

The additional matches being added do not have to have the same number of teams as the already existing matches. Whilst this is a feature you do not really want to use, it is useful if a team has been removed from the schedule, the matches start, and then the team turns up, as you cannot substitute in a whole new schedule at this stage. In this circumstance, you can take the already existing schedule and crop it at a number of appearances that is slightly more than have already happen. You can then enter the new correct number of teams and then the remaining number of appearances desired. Remember to assign teams the same numbers they were originally assigned (and to give the new team the new highest number), so that the existing matches still remain the same.

Note: cropping at a multiple of 4 number of appearances is much more likely for the crop to succeed and not give teams in the cropped schedule unequal numbers of appearances.

## Acknowledgements

Thanks to:
 - [Alex](https://github.com/Alexbruvv) for the initial ideal for this match scheduler and for code improvements.
 - [Will](https://github.com/WillB97) for suggestions for the checks and code improvements.
 - [Peter](https://github.com/PeterJCLaw) whose [checks](https://github.com/PeterJCLaw/league-checker) gave inspiration for the checks here.

## How it works

For the curious, this is an explanation of how FRAMS works, including how it scores the schedules.

TL;DR - spacing is scored using this [equation](https://www.desmos.com/calculator/0kp7dkrovc) and facings are scored using this [equation](https://www.desmos.com/calculator/32leritklv). Team numbers in each match are swapped with team numbers in every other match and the swap that gives the lowest score is kept. This is repeated many times until the score does not change. The starting zones are then shuffled for each match in turn to give the smallest spread of starting zones.

### Scoring the schedule

Each schedule is scored to see how good it is. The lower the score, the better. The main sources of increased score are: spacing, facings, and overlapped matches.

#### Spacing score

The equation for the spacing score is given by: $\textrm{score}\_\textrm{spacing} = (x_\textrm{target} - x)^2 + 2 \exp (5.5-x)$, where $x$ is the spacing and $x_\textrm{target}$ is the target match spacing, $\textrm{spacing}_\textrm{target}$ = $\frac{\textrm{N}^\textrm{o}\textrm{teams}}{4} - 1$. This equation can be seen on Desmos [here](https://www.desmos.com/calculator/0kp7dkrovc). The spacing is determined for every team and between every pair of consecutive matches that they are in.

This equation is essentially a parabola with an exponential increase at the lower end to make very low spacing scores heavily unfavourable.

#### Facings score

The equation for the facings score is given by: $\textrm{score}\_\textrm{facings} = 0.58\exp\left(2(x_\textrm{target}-x)\right) + 0.58\exp\left(2.25(x-x_\textrm{target})\right)$, where $x$ is the number of the team has been faced and $x_\textrm{target}$ is the target repeat, $\textrm{repeat}_\textrm{target} = \frac{4 \times \textrm{N}^\textrm{o}\textrm{appearances}}{\textrm{N}^\textrm{o}\textrm{teams}}$. If this score is less than $20$ for $x=0$, then the score is given as $20$. This equation can been seen on Desmos [here](https://www.desmos.com/calculator/32leritklv). Note that the target repeats is based on how many appearances there currently are, not the overall number of appearances once the schedule is finished. Each team is looked at in turn and the number of times that teams plays every other team is considered. This number of times a team has faced each team becomes $x$ in the formula above. 

This equation gives quite a narrow range of allowed repeats for each team. This is to try and reduce the number of repeats a team facing as this is quite undesirable. This is also why the upper end of repeats has a slightly higher factor in the exponential. The $0.58$ pre-factor reduces this score such that a weighting of 0.5-0.5 for facings and spacing produces a fairly balanced schedule. The increase when teams have been faced 0 times is to try and encourage teams to have played all other teams and discourage missing facing teams where possible.

#### Overlaps score

The match schedule is analysed to find any partial overlaps (3 of the 4 teams in the match multiple times) and any identical matches (All of the 4 teams in the match multiple times). Any pair of matches that have a partial overlap are given a score of $+45$. Identical matches can also have a similar increase in score, but as any identical matches will also trigger the partial overlap 4 times and therefore give a score of $+180$, this is turned off as it is not really necessary to increase it any further.

#### Zones score

This is considered separately to the rest of the scores, but it is calculated by: $\textrm{score}\_\textrm{zone} = |x_\textrm{target} - x|^3$, where $x$ is the number of times a team plays in that corner and $x_\textrm{target}$ is the target number of times a team plays in that corner, which is $\frac{\textrm{N}^\textrm{o}\textrm{appearances}}{4}$.

### How a schedule is generated

The first step is to add a league block to the schedule. If the number of teams is a multiple of 4, then all the number are added in order, with 4 per match, until all the teams have been added. If the number of teams is even (but not a multiple of 4), all the numbers are added in order twice, to get to a multiple of 4. For example, with 10 teams, they would be added as: [1,2,3,4], [5,6,7,8], [9,10,1,2], [3,4,5,6], [7,8,9,10]. If the number of teams is odd, all numbers are added in order four times to get to a multiple of 4. This block is then shuffled until its score is unchanged.

Shuffling a league block is done by taking the first team in the first match and swapping that team with the first team in the second match. The match schedule's score is then calculated. If this score is lower than the previous score, this new schedule is the current best schedule. The team is then swapped with the second team in the second match and so on until this first team in the first match has been swapped to each of the 4 teams in every match (other than the first match). Whichever swap gave the lowest score (the current best schedule) then replaces the current match schedule. This process is then repeated for the second team in the first match, etc in the first match, then repeated for every match in that block. After this point, the league block has been shuffled once. The league block is then shuffled multiple times until the schedule score remains unchanged.

Next, another league block as described as above is added to the schedule so it comprises of 2 league blocks. The last league block (the one just added) is then shuffled as described above. This takes slightly longer as the scoring is done for the whole schedule.

After every league block has been added and shuffled to reach local minimum, the zones are shuffled to reduce the zone score as described above. To shuffle the zones, each match is considered in turn. For each match, the team numbers for that match are shuffled into all of the 24 possible different arrangements. Each of these are scored with the whole schedule and whichever is lowest is used for the schedule. This process is repeated for each match.

More league blocks are added until the desired number of appearances is reached. If adding a block will leave a number of appearances that is less than the number of appearances in each block (e.g. if the number of teams is even, adding a league block of 2 appearances results in only 1 appearance left to add to the schedule), this last set of appearances is added to this league block to create a final, larger league block. If the product of the number of teams and number of appearances in this final block is not a multiple of 4, -1 is added as a team number to the block until it is a multiple of 4. This -1 represents an out of range team number and serves as an empty slot for the match.A maximum of 3 of these may be added to fill the schedule, but will always be found in the last block.

### How a schedule is optimised

Optimising a schedule is done by shuffling the whole schedule at once. So the first team in the first match is swapped with the first team in the second match. The match schedule's score is then calculated. If this score is lower than the previous score, this new schedule is the current best schedule. The team is then swapped with the second team in the second match and so on until this first team in the first match has been swapped to each of the 4 teams in every match (other than the first match). Whichever swap gave the lowest score (the current best schedule) then replaces the current match schedule. This process is then repeated for the second team in the first match, etc in the first match, then repeated for every match in the whole schedule. After this point, the schedule has been shuffled once. The whole schedule is then shuffled multiple times until the schedule score remains unchanged. This is why optimising a schedule takes a long time and why it breaks any league block separation as league blocks are completely ignored for optimising a schedule.
