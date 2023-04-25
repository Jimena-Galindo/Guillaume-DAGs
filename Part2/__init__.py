from otree.api import *
import numpy as np
import random

doc = """
Get the note written in Guess if the sound is heard or not for 27 random trials of each machine. Each row is shown 
in a different page (there are 27 pages of guesses per round). The machine changes on each round in the same order as 
they were shown in part1. The order of trials is shuffled again
"""


class C(BaseConstants):
    NAME_IN_URL = 'Part2'
    PLAYERS_PER_GROUP = None
    # the number of rounds must be equal to the number of cases that will be shown
    NUM_ROUNDS = 11


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the number of lights that the case has. It can be Red and Blue (+ others and sound) or Red, Blue, Green.
    n_lights = models.IntegerField()

    # the guess made for each row shown in a random order (randomized at participant level.
    # The randomization happens in the sampling procedure in the Guess1 page)
    guess1 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess2 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess3 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess4 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess5 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess6 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess7 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess8 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess9 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess10 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess11 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess12 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess13 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess14 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess15 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess16 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess17 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess18 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess19 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess20 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess21 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess22 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess23 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess24 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess25 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess26 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')
    guess27 = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')

    # Save each of the sampled rows as strings
    row1 = models.StringField()
    row2 = models.StringField()
    row3 = models.StringField()
    row4 = models.StringField()
    row5 = models.StringField()
    row6 = models.StringField()
    row7 = models.StringField()
    row8 = models.StringField()
    row9 = models.StringField()
    row10 = models.StringField()
    row11 = models.StringField()
    row12 = models.StringField()
    row13 = models.StringField()
    row14 = models.StringField()
    row15 = models.StringField()
    row16 = models.StringField()
    row17 = models.StringField()
    row18 = models.StringField()
    row19 = models.StringField()
    row20 = models.StringField()
    row21 = models.StringField()
    row22 = models.StringField()
    row23 = models.StringField()
    row24 = models.StringField()
    row25 = models.StringField()
    row26 = models.StringField()
    row27 = models.StringField()

    password = models.StringField()
    original_color = models.IntegerField()


# FUNCTIONS
# translate each of the sampled case rows to the html table it can take 2 or 3 lights
def html_table_original(row, n_lights):
    # row is a row taken from a case from part 1. The case can have either 4 columns (Red, Blue, others, sound) or
    # it can have 5 columns (Red, Blue, Green, others, Sound)

    # 2 lights: Red, Blue (and Others)
    if n_lights == 4:

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        other = ['&#x3f']

        # red lights
        if row[0] == 1:
            red.append('<div class="circle_red"></div>')
        else:
            red.append('<div class="circle_red_off"></div>')

        # blue lights
        if row[1] == 1:
            blue.append('<div class="circle_blue"></div>')
        else:
            blue.append('<div class="circle_blue_off"></div>')

        html_mat = np.column_stack((red, blue, other))

        # Write out the html table code
        table = '<table class="table" style="text-align: center; vertical-align:middle">' \
            '<tr><th>Red Light</th><th>Blue Light</th><th>Other Lights</th></tr><tr height="95px"><td>' \
                + html_mat[0][0] + '</td><td>' + html_mat[0][1] + '</td><td>' + html_mat[0][2] + '</td></tr></table>'

    # 3 lights: Red, Blue, Green (and Others)
    if n_lights == 5:

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        green = []
        other = ['&#x3f']

        # red lights
        if row[0] == 1:
            red.append('<div class="circle_red"></div>')
        else:
            red.append('<div class="circle_red_off"></div>')

        # blue lights
        if row[1] == 1:
            blue.append('<div class="circle_blue"></div>')
        else:
            blue.append('<div class="circle_blue_off"></div>')

        # green lights
        if row[1] == 1:
            green.append('<div class="circle_green"></div>')
        else:
            green.append('<div class="circle_green_off"></div>')

        html_mat = np.column_stack((red, blue, green, other))

        # Write out the html table code
        table = '<table class="table" style="text-align: center; vertical-align:middle">' \
            '<tr><th>Red Light</th><th>Blue Light</th><th>Green Light</th><th>Other Lights</th></tr>'\
            '<tr height="95px; vertical-align:middle"><td>' + html_mat[0][0] + '</td><td>' + html_mat[0][1] + \
                '</td><td>' + html_mat[0][2] + \
                '</td><td>' + html_mat[0][3] + '</td></tr></table>'

    return table


def html_table_flipped(row, n_lights):
    # this table has the opposite colors but takes the data in in the same order.
    # row is a row taken from a case from part 1. The case can have either 4 columns (Red, Blue, others, sound) or
    # it can have 5 columns (Red, Blue, Green, others, Sound)

    # 2 lights: Red, Blue (and Others)
    if n_lights == 4:

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        other = ['&#x3f']

        # red lights (they are still called red but the color shown is blue)
        if row[0] == 1:
            red.append('<div class="circle_blue"></div>')
        else:
            red.append('<div class="circle_blue_off"></div>')

        # blue lights (they are still called blue but the color shown is red)
        if row[1] == 1:
            blue.append('<div class="circle_red"></div>')
        else:
            blue.append('<div class="circle_red_off"></div>')

        html_mat = np.column_stack((red, blue, other))

        # Write out the html table code
        table = '<table class="table" style="text-align: center; vertical-align:middle">' \
            '<tr><th>Blue Light</th><th>Red Light</th><th>Other Lights</th></tr><tr height="95px"><td>' \
                + html_mat[0][0] + '</td><td>' + html_mat[0][1] + '</td><td>' + html_mat[0][2] + '</td></tr></table>'

    # 3 lights: Red, Blue, Green (and Others)
    if n_lights == 5:

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        green = []
        other = ['&#x3f']

        # red lights
        if row[0] == 1:
            red.append('<div class="circle_blue"></div>')
        else:
            red.append('<div class="circle_blue_off"></div>')

        # blue lights
        if row[1] == 1:
            blue.append('<div class="circle_red"></div>')
        else:
            blue.append('<div class="circle_red_off"></div>')

        # green lights
        if row[1] == 1:
            green.append('<div class="circle_green"></div>')
        else:
            green.append('<div class="circle_green_off"></div>')

        html_mat = np.column_stack((red, blue, green, other))

        # Write out the html table code
        table = '<table class="table" style="text-align: center; vertical-align:middle">' \
            '<tr><th>Blue Light</th><th>Red Light</th><th>Green Light</th><th>Other Lights</th></tr>'\
            '<tr height="95px; vertical-align:middle"><td>' + html_mat[0][0] + '</td><td>' + html_mat[0][1] + \
                '</td><td>' + html_mat[0][2] + \
                '</td><td>' + html_mat[0][3] + '</td></tr></table>'

    return table


# PAGES
class Instructions(Page):
    # form_model = 'player'
    # form_fields = ['password']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    # @staticmethod
    # def error_message(player, values):
        # if values['password'] != '45RT':
            # return 'the password is incorrect'


class Transition(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        player.original_color = participant.original_color[player.round_number - 1]
        return dict(r=player.round_number)


class Guess1(Page):
    # All 10 pages follow the same structure as this one. Only the code in Page1 has comments (sorry)
    form_model = 'player'
    form_fields = ['guess1']

    @staticmethod
    def vars_for_template(player: Player):
        # in each round, get the case that should be shown in that round. The cases are stores in the right order in
        # participant.realized_cases. This already includes all the realized repetitions or each row
        r = player.round_number
        participant = player.participant
        # we also need to get the notes from part 1
        all_notes = participant.notes
        notes = all_notes[r-1]
        cases = participant.realized_cases
        case = cases[r-1]
        # determine how many lights are in the case 2 or 3 (plus the others column)
        n_lights = len(case[0])
        player.n_lights = n_lights
        # sample 10 out of the realized rows (this is the step that randomizes the order of rows at the participant
        # level relative to the order in which they appeared in the case in part 1
        rows = random.sample([i for i in range(len(case))], 27)

        case_10 = []

        for i in rows:
            case_10.append(case[i])
        # save each of the sampled rows as strings
        player.row1 = str(case_10[0])
        player.row2 = str(case_10[1])
        player.row3 = str(case_10[2])
        player.row4 = str(case_10[3])
        player.row5 = str(case_10[4])
        player.row6 = str(case_10[5])
        player.row7 = str(case_10[6])
        player.row8 = str(case_10[7])
        player.row9 = str(case_10[8])
        player.row10 = str(case_10[9])
        player.row11 = str(case_10[10])
        player.row12 = str(case_10[11])
        player.row13 = str(case_10[12])
        player.row14 = str(case_10[13])
        player.row15 = str(case_10[14])
        player.row16 = str(case_10[15])
        player.row17 = str(case_10[16])
        player.row18 = str(case_10[17])
        player.row19 = str(case_10[18])
        player.row20 = str(case_10[19])
        player.row21 = str(case_10[20])
        player.row22 = str(case_10[21])
        player.row23 = str(case_10[22])
        player.row24 = str(case_10[23])
        player.row25 = str(case_10[24])
        player.row26 = str(case_10[25])
        player.row27 = str(case_10[26])


        row = [int(s) for s in case_10[0]]

        # pass the row to the function that prints out the html
        if player.original_color == 1:
            evaluated = html_table_original(row, n_lights)
        else:
            evaluated = html_table_flipped(row, n_lights)

        return dict(notes=notes, table=evaluated, round=r, lights=n_lights)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and add one point to player payoff if it was
        row = player.row1[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess1 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess2(Page):
    form_model = 'player'
    form_fields = ['guess2']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row2[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row2[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess2 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess3(Page):
    form_model = 'player'
    form_fields = ['guess3']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row3[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row3[1:-1]
        participant = player.participant
        participant.sound.append(row[-1])
        row = [int(s) for s in row.split(' ')]
        if player.guess3 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess4(Page):
    form_model = 'player'
    form_fields = ['guess4']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row4[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row4[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        participant.sound.append(row[-1])
        if player.guess4 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess5(Page):
    form_model = 'player'
    form_fields = ['guess5']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row5[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row5[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess5 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess6(Page):
    form_model = 'player'
    form_fields = ['guess6']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row6[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row6[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        participant.sound.append(row[-1])
        if player.guess6 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess7(Page):
    form_model = 'player'
    form_fields = ['guess7']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row7[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row7[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        participant.sound.append(row[-1])
        if player.guess7 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess8(Page):
    form_model = 'player'
    form_fields = ['guess8']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row8[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row8[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess8 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess9(Page):
    form_model = 'player'
    form_fields = ['guess9']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row9[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row9[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        participant.sound.append(row[-1])
        if player.guess9 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess10(Page):
    form_model = 'player'
    form_fields = ['guess10']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row10[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row10[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess10 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)

class Guess11(Page):
    form_model = 'player'
    form_fields = ['guess11']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row11[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row11[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess11 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess12(Page):
    form_model = 'player'
    form_fields = ['guess12']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row12[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row12[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess12 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess13(Page):
    form_model = 'player'
    form_fields = ['guess13']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row13[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row13[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess13 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess14(Page):
    form_model = 'player'
    form_fields = ['guess14']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row14[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row14[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess14 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess15(Page):
    form_model = 'player'
    form_fields = ['guess15']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row15[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row15[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess15 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess16(Page):
    form_model = 'player'
    form_fields = ['guess16']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row16[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row16[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess16 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess17(Page):
    form_model = 'player'
    form_fields = ['guess17']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row17[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row17[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess17 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess18(Page):
    form_model = 'player'
    form_fields = ['guess18']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row18[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row18[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess18 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess19(Page):
    form_model = 'player'
    form_fields = ['guess19']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row19[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row19[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess19 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess20(Page):
    form_model = 'player'
    form_fields = ['guess20']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row20[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row20[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess20 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess21(Page):
    form_model = 'player'
    form_fields = ['guess21']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row21[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row21[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess21 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess22(Page):
    form_model = 'player'
    form_fields = ['guess22']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row22[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row22[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess22 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess23(Page):
    form_model = 'player'
    form_fields = ['guess23']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row23[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row23[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess23 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess24(Page):
    form_model = 'player'
    form_fields = ['guess24']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row24[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row24[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess24 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess25(Page):
    form_model = 'player'
    form_fields = ['guess25']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row25[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row25[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess25 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess26(Page):
    form_model = 'player'
    form_fields = ['guess26']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row26[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row26[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess26 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Guess27(Page):
    form_model = 'player'
    form_fields = ['guess27']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]

        row = player.row27[1:-1]
        row = [int(s) for s in row.split(' ')]

        if player.original_color == 1:
            evaluated = html_table_original(row, player.n_lights)
        else:
            evaluated = html_table_flipped(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and save in a vector of guesses
        row = player.row27[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        participant.sound.append(row[-1])
        if player.guess27 == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions, Transition,
                 Guess1, Guess2, Guess3, Guess4, Guess5, Guess6, Guess7, Guess8, Guess9, Guess10,
                 Guess11, Guess12, Guess13, Guess14, Guess15, Guess16, Guess17, Guess18, Guess19, Guess20,
                 Guess21, Guess22, Guess23, Guess24, Guess25, Guess26, Guess27]
