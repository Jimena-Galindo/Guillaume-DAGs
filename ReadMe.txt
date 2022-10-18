To run the experiment upload the otree zip file to heroku. Make sure the debug mode is off.
The code to move on to part 2 is '45RT' and the code to move on to part 3 is '46RT' Caps matter.
When the experiment is done download the regular data as well as the participant data.

Player variables:

Part 1: Each round is a case in random order. The order of cases/machines is saved as a string variable for round 1.
The case/machine order is also saved in the participant variables as a list of [matrix, freq] as well as a list of the
names provided in the spreadsheet. Each round also has the corresponding case/machine as a string and the notes written
for it.

Part 2: Each round is a case/machine in the same order as in Part 1. The variables each round are each of the 10 rows
sampled and each of the 10 guesses. For the guesses sound on/off is 1/0.
Players also have a variable called n_lights. This is because the code is flexible to showing 3 lights instead of 2.
In the current version all cases show only 2 lights.

Part 3: There is only one round. The variables are the 11 lights chosen, the row that was shown, the index of the case
that was selected (from that particular participant's ordered cases), and the guess that they made for the sound. So if
the case is X, the light that was shown was lightX of row. The list of all lights that were chosen is also saved in the
participant variables

Participant Variables:
notes - a list of all the notes in the order in which they saw the cases
cases_ordered - list of [matrix, frequencies] in the order in which they were shown
realized_cases - list of matrices each matrix represent the order in which they saw the 27 trials
light_list - list of the chosen lights from part 3
order_names - list of the names of each case in the order that they were shown
guesses - a list of whether their guesses were right (1) or wrong (0) (110 guesses from part 2 and 1 guess from part 3)
sound - a list of the correct choice for each of the trials where they had to guess (same length and order as guesses)


Specifics of Each Part:

Part 1: 
participants are shown N rows from a DAG that consists of 2 (Red and Blue) or 3 (Red, Blue and Green) lights, other
lights (hidden) and the outcome is a sound that may be on or not.

To specify the case, a matrix must be entered in the ____init____.py file of Part1, in Instruction Page and in the
before_next_page section. In this Part the Instructions page is where a lot of the variables are set so it should not be
skipped.

The Case should be a binary matrix the columns are Red light, Blue light, Green light (optional), Others, Sound. A 1
means the light/sound is on; a 0 means the light/sound is off. (In the example the matrix is called case1)

Each case must be accompanied by a vector that specifies the frequency with which each row is to be repeated. The vector
should have as many elements in it as the matrix has rows. In addition, the elements in the vector need to add up to at
least 10 for Part 2 to work. (In the example there are 11 frequency vectors  called freq1, …, freq11)

You can enter as many pairs of (case, frequencies) as you would like. The number of rounds specified in C(BaseConstants)
should be the number of such pairs. (In the example the same case is paired with 11 different frequency vectors so there
are 11 rounds).

Once all the case matrices and all the frequency vectors are specified the case _list needs to be built. The variable
case_list is a list of the bundles (case, freq) that you want to show participants. The length of this list needs to be
equal to the number of rounds specified.

The order of the case_list will be shuffled at a participant level, so all participants will see the cases in a
different order. The ordered list for each participant is saved as a binary matrix at the participant level (this data
needs to be downloaded separately) AND as a string variable for round 1 of each participant.

The for each specified (case, freq) the rows of the matrix are repeated as in freq and then shuffled at the participant
level. This all happens within the function html_table_freqs. The function then takes the matrix and translates it into
html code to be passed to the page template.

The realized case (with the repetitions and shuffled rows is saved as a string variable at the player level). The list
of all realized matrices is also saved as a list of matrices at the participant level. If you want to have this data you
must download the participant data separately.

The code can also accommodate entering the probabilities with which each row of the matrix should be drawn. In this case
you should specify the probabilities vectors instead of the frequency vectors. In addition you should change the function
being used in the DAG1 page. In vars_for_template, the variable evaluated should be html_table_probs(case[0], case[1], n)
Here you need to specify n (the number of draws that you want to have) inside the function.


Part 2: 
There must be as many rounds as there are cases (as in part 1). This is set in C(BaseConstants, num_rounds). 

The instructions page has the instructions for part 2 to be read on the screen. In order to proceed the subjects must
enter a code. The code is 45RT
 
There are 10 guess pages in this part. Each of these pages shows a randomly drawn row from the realized matrix in part 1,
shows the notes written for the case and shows the lights on/off. It conceals the sound and asks the participant to
guess it. All 10 sampled rows are drawn in the page for Guess1 and saved at the player level. The case changes across
rounds.

The order in which cases are shown is the same as in part 1. But the rows that are sampled are different for each
participant and the order in which they appear is different (in a random way) from the order in which they appeared in
the case in part 1.

Players get one point for every correct answer. 


Part 3: 
The participants are shown a list of all cases with the notes that they wrote in part1 (in the same order as they saw
them in parts 1 and 2) and they are asked to choose a light for each of the cases. Then a single case and a single row
is drawn at random (at the participant level) and they are shown only that light. They have to choose if the sound is on
or not.

This part has only one round. 

The player must have as many fields for lights as there are choices. To generate an additional field, in ___init___.py
for part3, in the Player(BasePlayer) class, call the function make_field( . , . ). The first input for the function is
the label for the choice (the example has no label. It appears at the top of the table) and the second input is the
number of lights that the case has. If there are Red and Blue only it is 2. If the case has Red, Blue and Green then it
should be 3.

Once all the fields are defined for the player, they need to be passed to the LightChoice page. The variable form_fields
should have all of them. They also need to be saved at the participant level in the list light_list.



























