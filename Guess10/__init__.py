from otree.api import *
import numpy as np
import random

doc = """
Get the note written in Guess if the sound is heard or not for 10 random trials of each case.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Part2'
    PLAYERS_PER_GROUP = None
    # the number of rounds must be equal to the number of cases that will be shown
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    n_lights = models.IntegerField()

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

    n_correct = models.IntegerField(initial=0)

    light = models.IntegerField(label="Which light would you like to see for this case in part 3?",
                                widget=widgets.RadioSelectHorizontal)


# FUNCTIONS
# Determine the lights that can be chosen in stage 2
def light_choices(player):
    if player.n_lights == 4:
        choices = [[1, 'Red'], [2, 'Blue']]
    else:
        choices = [[1, 'Red'], [2, 'Blue'], [3, 'Green']]
    return choices


# translate each case to html table
def html_table(row, n_lights):
    # case should be an array of dimensions kxn. k is the number of unique trials and n is n_lights + others + sound
    # frequency should be a vector of size k with each element i equal to the number or repetitions of trial i wanted
    # the total number of trials will be sum(freq)

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
            '<tr height="95px; vertical-align:middle"><td>' + html_mat[0][0] + '</td><td>' + html_mat[0][1] + '</td><td>' + html_mat[0][2] + \
                '</td><td>' + html_mat[0][3] + '</td></tr></table>'

    return table


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.light_list = []


class Guess1(Page):
    form_model = 'player'
    form_fields = ['guess1']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]
        cases = participant.realized_cases
        case = cases[r-1]

        n_lights = len(case[0])
        player.n_lights = n_lights

        rows = random.sample([i for i in range(len(case))], 10)

        case_10 = []

        for i in rows:
            case_10.append(case[i])

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

        row = player.row1[1:-1]
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, n_lights)

        return dict(notes=notes, table=evaluated, round=r, lights=n_lights)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


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
        row = [int(s) for s in row.split(',')]

        evaluated = html_table(row, player.n_lights)

        return dict(notes=notes, table=evaluated, round=r)


class LightChoice(Page):
    form_model = 'player'
    form_fields = ['light']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        return dict(round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Save the choice of lights at the participant level to pass it on to stage 3
        if player.round_number == C.NUM_ROUNDS:
            participant = player.participant
            light_list = []
            for p in player.in_all_rounds():
                light_list.append(p.light)
            light_list.append(player.light)
            participant.light_list = light_list


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions,
                 Guess1, Guess2, Guess3, Guess4, Guess5, Guess6, Guess7, Guess8, Guess9, Guess10,
                 LightChoice]
