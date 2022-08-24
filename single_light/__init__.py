from otree.api import *
import numpy as np
import random

doc = """
Get the note written in Guess if the sound is heard or not for a single trial for which only one light is shown.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Part3'
    PLAYERS_PER_GROUP = None
    # the number of rounds must be equal to the number of cases that will be shown
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    n_lights = models.IntegerField()

    guess = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')

    row = models.StringField()

    light = models.IntegerField()

    correct = models.IntegerField()

# FUNCTIONS
# translate each case to html table
def html_table(case, light):
    # case should be an array of dimensions kxn. k is the number of unique trials and n is n_lights + others + sound
    # frequency should be a vector of size k with each element i equal to the number or repetitions of trial i wanted
    # the total number of trials will be sum(freq)

    n_lights = len(case)

    # 2 lights: Red, Blue (and Others). The case matrix has 4 columns
    if n_lights == 4:
        if light == 1:
            blue = ['&#x3f']
            other = ['&#x3f']
            if case[0] == 1:
                red = ['<div class="circle_red"></div>']
            else:
                red = ['<div class="circle_red_off"></div>']

        else:
            red = ['&#x3f']
            other = ['&#x3f']

            if case[1] == 1:
                blue = ['<div class="circle_blue"></div>']
            else:
                blue = ['<div class="circle_blue_off"></div>']

        html_mat = np.column_stack((red, blue, other))

        # Write out the html table code
        table1 = '<table class="table" style="text-align: center; vertical-align:middle">' \
                '<tr><th>Red Light</th><th>Blue Light</th><th>Other Lights</th></tr>'

        table1 = table1 + '<tr height="95px" ><td>' + html_mat[0][0] + '</td>'\
                                 '<td>' + html_mat[0][1] + '</td>'\
                                 '<td>' + html_mat[0][2] + '</td></tr>'

        table1 = table1 + '</table>'

    # 3 lights: Red, Blue, Green (and Others). the case matrix has 5 columns
    if n_lights == 5:
        if light == 1:
            blue = ['&#x3f']
            green = ['&#x3f']
            other = ['&#x3f']
            if case[0] == 1:
                red = ['<div class="circle_red"></div>']
            else:
                red = ['<div class="circle_red_off"></div>']

        elif light == 2:
            red = ['&#x3f']
            green = ['&#x3f']
            other = ['&#x3f']

            if case[1] == 1:
                blue = ['<div class="circle_blue"></div>']
            else:
                blue = ['<div class="circle_blue_off"></div>']

        else:
            red = ['&#x3f']
            blue = ['&#x3f']
            other = ['&#x3f']

            if case[2] == 1:
                green = ['<div class="circle_green"></div>']
            else:
                green = ['<div class="circle_green_off"></div>']

        html_mat = np.column_stack((red, blue, green, other))

        # Write out the html table code
        table1 = '<table class="table" style="text-align: center; vertical-align:middle">' \
                '<tr><th>Red Light</th><th>Blue Light</th><th>Green Light</th><th>Other Lights</th></tr>'

        table1 = table1 + '<tr height="95px" ><td>' + html_mat[0][0] + '</td>'\
                                 '<td>' + html_mat[0][1] + '</td>'\
                                 '<td>' + html_mat[0][2] + '</td>' \
                                 '<td>' + html_mat[0][3] + '</td></tr>'
        table1 = table1 + '</table>'

    return table1


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Guess1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number

        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]
        cases = participant.realized_cases
        case = cases[r-1]
        row = random.sample([i for i in range(len(case))], 1)[0]

        case_1 = case[row]

        n_lights = len(case_1)

        player.row = str(case_1)

        player.n_lights = n_lights

        light_list = participant.light_list
        show_light = light_list[r - 1]

        evaluated = html_table(case_1, show_light)

        return dict(notes=notes, table=evaluated, lights=n_lights, round=r)

    form_model = 'player'
    form_fields = ['guess']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and add one point to player payoff if it was
        row = player.row[1:-1]
        row = [int(s) for s in row.split(',')]
        if player.guess == row[-1]:
            player.payoff += 1


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions, Guess1]
