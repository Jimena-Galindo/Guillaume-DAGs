from otree.api import *
import numpy as np
import random

doc = """
Get the note written in Guess if the sound is heard or not for 10 random trials of each case. Each row is shown 
in a different page (there are 10 pages of guesses per round. The case changes on each round in the same order as 
they were shown in part1. The order of rows is shuffled again
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


# FUNCTIONS
# translate each of the sampled case rows to the html table it can take 2 or 3 lights
def html_table(row, n_lights):
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


# PAGES
class Instructions(Page):
    # this page is only necessary if you want to have some page to indicate that they are moving on to part 2
    @staticmethod
    # if you want to have a page to indicate when they are changing from one case to the next, get rid of this part
    # and show the page in all rounds
    def is_displayed(player: Player):
        return player.round_number == 1


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
        rows = random.sample([i for i in range(len(case))], 10)

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

        row = [int(s) for s in case_10[0]]

        # pass the row to the function that prints out the html
        evaluated = html_table(row, n_lights)

        return dict(notes=notes, table=evaluated, round=r, lights=n_lights)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and add one point to player payoff if it was
        row = player.row1[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess1 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row2[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess2 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row3[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess3 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row4[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        if player.guess4 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row5[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess5 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row6[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        if player.guess6 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row7[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        if player.guess7 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row8[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess8 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row9[1:-1]
        row = [int(s) for s in row.split(' ')]
        participant = player.participant
        if player.guess9 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


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

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right
        row = player.row10[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess10 == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions,
                 Guess1, Guess2, Guess3, Guess4, Guess5, Guess6, Guess7, Guess8, Guess9, Guess10]
