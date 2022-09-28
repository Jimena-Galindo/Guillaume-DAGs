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
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(label, n_lights):
    if n_lights == 2:
        return models.IntegerField(
        choices=[[1, 'Red'], [2, 'Blue']],
        label=label,
        widget=widgets.RadioSelectHorizontal,
        )
    else:
        return models.IntegerField(
            choices=[[1, 'Red'], [2, 'Blue'], [3, 'Green']],
            label=label,
            widget=widgets.RadioSelectHorizontal,
        )


class Player(BasePlayer):
    n_lights = models.IntegerField()

    guess = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')

    row = models.StringField()

    light1 = make_field(' ', 2)
    light2 = make_field(' ', 2)


# FUNCTIONS
# translate each case to html table
def html_table(case, light):
    # case should be an array of dimensions kxn. k is the number of unique trials and n is n_lights + others + sound
    # frequency should be a vector of size k with each element i equal to the number or repetitions of trial i wanted
    # the total number of trials will be sum(freq)

    n_lights = len(case)

    # 2 lights: Red, Blue (and Others). The case matrix has 4 columns
    if n_lights == 4:
        # Only show the selected light
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


def notes_table(notes):
    table = '<table class="table" style="width: 100%; margin: auto; padding-right: 0px; " ><tr>' \
            '<th><h4>Cases</h4></th><th><h4>Notes</h4></th>'\
            '</tr>'
    for i in range(len(notes)):
        table = table + '<tr> <td style="border-bottom: transparent; padding-right:0;"> </td> <td><div ' \
                        'style="background: ghostwhite;'\
                                    'font-size: 20px;'\
                                    'width: 400px;'\
                                    'height: 100px;'\
                                    'overflow-y: auto;'\
                                    'padding: 5px;'\
                                    'border: 2px solid lightgray;'\
                                    'margin: 10px;">' \
                        + notes[i] + '</div></td></tr>'
    table = table + '</table>'
    return table

# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class LightChoice(Page):
    form_model = 'player'

    # need to add all the light fields here
    form_fields = ['light1',
                   'light2']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        all_notes = participant.notes
        return dict(notes=notes_table(all_notes), all_notes=all_notes)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # save all the light choices at the participant level
        participant = player.participant
        participant.light_list = [player.light1, player.light2]


class Guess1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number

        participant = player.participant
        all_notes = participant.notes

        # get the case corresponding to the round and sample only one row at random
        cases = participant.realized_cases

        # draw a random case
        index = int(random.randint(0, len(cases)-1))

        # get the selected case and the notes corresponding to it
        case = cases[index]
        notes = all_notes[index]

        #sample one row from the case at random
        row = random.sample([i for i in range(len(case))], 1)[0]
        case_1 = case[row]

        n_lights = len(case_1)
        # save the row sampled as a string for the player
        player.row = str(case_1)

        player.n_lights = n_lights

        # get the light that they chose in the previous stage
        light_list = participant.light_list
        show_light = light_list[index]

        evaluated = html_table(case_1, show_light)

        return dict(notes=notes, table=evaluated, lights=n_lights, round=r)

    form_model = 'player'
    form_fields = ['guess']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if the guess was right and add one point to player payoff if it was
        row = player.row[1:-1]
        participant = player.participant
        row = [int(s) for s in row.split(' ')]
        if player.guess == row[-1]:
            player.payoff += 1
            participant.guesses += 1
        else:
            player.payoff += 0
            participant.guesses += 0


class Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(pay=participant.payoff, guesses=participant.guesses)


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions, LightChoice, Guess1, Feedback]
