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
def html_table(case, freq):
    # case should be an array of dimensions kxn. k is the number of unique trials and n is n_lights + others + sound
    # frequency should be a vector of size k with each element i equal to the number or repetitions of trial i wanted
    # the total number of trials will be sum(freq)

    n_lights = len(case[0])

    # 2 lights: Red, Blue (and Others) then the case matrix has 4 columns
    if n_lights == 4:

        # Add the repetitions for each row
        h = np.tile(case[0], (freq[0], 1))
        for i in range(len(freq) - 1):
            a = np.tile(case[i + 1], (freq[i + 1], 1))
            h = np.vstack((h, a))

        # Shuffle the rows of html matrix with repeated trials
        # np.random.shuffle(h) for this stage we don't shuffle the order of the rows

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        sound = ['{{ formfield.guess1 }}',
                 '{{ formfield player.guess2 }}',
                 '{{formfield player.guess3}}',
                 '{{formfield player.guess4}}',
                 '{{formfield player.guess5}}',
                 '{{formfield player.guess6}}',
                 '{{formfield player.guess7}}',
                 '{{formfield player.guess8}}',
                 '{{formfield player.guess9}}',
                 '{{formfield player.guess10}}']
        other = ['&#x3f'] * sum(freq)

        for i in range(sum(freq)):
            # red lights
            if h[i][0] == 1:
                red.append('<div class="circle_red"></div>')
            else:
                red.append('<div class="circle_red_off"></div>')

            # blue lights
            if h[i][1] == 1:
                blue.append('<div class="circle_blue"></div>')
            else:
                blue.append('<div class="circle_blue_off"></div>')

        html_mat = np.column_stack((red, blue, other, sound))

        # Write out the html table code
        table = '<table class="table" style="text-align: center">' \
                '<tr><th>Red Light</th><th>Blue Light</th><th>Other Lights</th></tr>'

        for i in range(sum(freq)):
            table = table + '<tr height="95px" ><td>' + html_mat[i][0] + '</td>'\
                                 '<td>' + html_mat[i][1] + '</td>'\
                                 '<td>' + html_mat[i][2] + '</td></tr>'

        table = table + '</table>'

    # 3 lights: Red, Blue, Green (and Others) then the case matrix has 5 columns
    if n_lights == 5:

        # Add the repetitions for each row
        h = np.tile(case[0], (freq[0], 1))
        for i in range(len(freq) - 1):
            a = np.tile(case[i + 1], (freq[i + 1], 1))
            h = np.vstack((h, a))

        # Shuffle the rows of html matrix with repeated trials
        # np.random.shuffle(h)

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        green = []
        sound = ['{{formfield player.guess1}}',
                 '{{formfield player.guess2}}',
                 '{{formfield player.guess3}}',
                 '{{formfield player.guess4}}',
                 '{{formfield player.guess5}}',
                 '{{formfield player.guess6}}',
                 '{{formfield player.guess7}}',
                 '{{formfield player.guess8}}',
                 '{{formfield player.guess9}}',
                 '{{formfield player.guess10}}']
        other = ['&#x3f'] * sum(freq)

        for i in range(sum(freq)):
            # red lights
            if h[i][0] == 1:
                red.append('<div class="circle_red"></div>')
            else:
                red.append('<div class="circle_red_off"></div>')

            # blue lights
            if h[i][1] == 1:
                blue.append('<div class="circle_blue"></div>')
            else:
                blue.append('<div class="circle_blue_off"></div>')

            # green lights
            if h[i][1] == 1:
                green.append('<div class="circle_green"></div>')
            else:
                green.append('<div class="circle_green_off"></div>')

        html_mat = np.column_stack((red, blue, green, other, sound))

        # Write out the html table code
        table = '<table class="table" style="text-align: center">' \
                '<tr><th>Red Light</th><th>Blue Light</th><th>Green Light</th><th>Other Lights</th></tr>'

        for i in range(sum(freq)):
            table = table + '<tr height="95px"><td>' + html_mat[i][0] + '</td>'\
                                 '<td>' + html_mat[i][1] + '</td>'\
                                 '<td>' + html_mat[i][2] + '</td>'\
                                 '<td>' + html_mat[i][3] + '</td></tr>'

        table = table + '</table>'

    return table, h


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.light_list = []
        r = player.round_number
        cases = participant.realized_cases
        case = cases[r - 1]
        n_lights = len(case[0])
        player.n_lights = n_lights



class Guess10(Page):
    form_model = 'player'
    form_fields = ['light',
                   'guess1',
                   'guess2',
                   'guess3',
                   'guess4',
                   'guess5',
                   'guess6',
                   'guess7',
                   'guess8',
                   'guess9',
                   'guess10']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        all_notes = participant.notes
        notes = all_notes[r-1]
        cases = participant.realized_cases
        case = cases[r-1]
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

        evaluated = html_table(case_10, [1]*10)

        return dict(notes=notes, table=evaluated[0], round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Compute the number of correct guesses in each round
        guesses = [player.guess1,
                   player.guess2,
                   player.guess3,
                   player.guess4,
                   player.guess5,
                   player.guess6,
                   player.guess7,
                   player.guess8,
                   player.guess9,
                   player.guess10]
        rows = [[int(s) for s in player.row1[1:-1].split(' ')],
                [int(s) for s in player.row2[1:-1].split(' ')],
                [int(s) for s in player.row3[1:-1].split(' ')],
                [int(s) for s in player.row4[1:-1].split(' ')],
                [int(s) for s in player.row5[1:-1].split(' ')],
                [int(s) for s in player.row6[1:-1].split(' ')],
                [int(s) for s in player.row7[1:-1].split(' ')],
                [int(s) for s in player.row8[1:-1].split(' ')],
                [int(s) for s in player.row9[1:-1].split(' ')],
                [int(s) for s in player.row10[1:-1].split(' ')]]
        n_correct = 0
        for i in range(len(guesses)):
            if guesses[i] == rows[i][-1]:
                n_correct = n_correct + 1

        player.n_correct = n_correct

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


page_sequence = [Instructions, Guess10]
