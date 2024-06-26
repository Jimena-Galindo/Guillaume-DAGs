from otree.api import *
import numpy as np
import random

doc = """
Get the note written in Guess if the sound is heard or not for a single trial for which only one light is shown.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Part3'
    PLAYERS_PER_GROUP = None
    # there is only one round because only one case is selected for the guess.
    # The case selected is random at participant level
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
    guess = models.IntegerField(choices=[[1, 'Ding'], [0, 'No Ding']], label='')

    row = models.StringField()
    case = models.IntegerField()
    # make the fields where the light is chosen (the first input is the label and the number
    # indicates the number of lights in the case (2 or 3)
    light1 = make_field(' ', 2)
    light2 = make_field(' ', 2)
    light3 = make_field(' ', 2)
    light4 = make_field(' ', 2)
    light5 = make_field(' ', 2)
    light6 = make_field(' ', 2)
    light7 = make_field(' ', 2)

    password = models.StringField()


# FUNCTIONS
# translate each case to html table with the lights
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


# make the column with the notes for the light choices
def notes_table(notes):
    # this function takes all the notes from part one and prints them out in a column of the table.
    # If the height of the divs is modified here, you will also have to modify it in the html for the fields columns
    table = '<table class="table" style="width: 100%; margin: auto; padding-right: 0px; " ><tr>' \
            '<th><h4>Machine</h4></th><th><h4>Notes</h4></th>'\
            '</tr>'
    for i in range(len(notes)):
        table = table + '<tr> <td style="padding-right:0; text-align: center">' + str(i+1) + \
                        '</td> <td><div ' \
                        'style="background: ghostwhite;'\
                                    'font-size: 20px;'\
                                    'width: 500px;'\
                                    'height: 200px;'\
                                    'overflow-y: auto;'\
                                    'padding: 5px;'\
                                    'border: 2px solid lightgray;'\
                                    'margin: 10px;">' \
                        + notes[i] + '</div></td></tr>'
    table = table + '</table>'
    return table


# PAGES
class MyWaitPage(WaitPage):
    # wait between stages 2 and 3.
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    title_text = "End of Part 2"
    body_text = "You have reached the end of Part 2. " \
                "Before we move on to Part 3 we will wait for all other participants to finish Part 2"
    wait_for_all_groups = True


class Instructions(Page):
    form_model = 'player'
    form_fields = ['password']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        if values['password'] != '46RT':
            return 'the password is incorrect'


class LightChoice(Page):
    form_model = 'player'

    # need to add all the light fields here
    form_fields = ['light1',
                   'light2',
                   'light3',
                   'light4',
                   'light5',
                   'light6',
                   'light7']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # get all the notes from part 1 and pass them to the function that makes the html code
        all_notes = participant.notes
        return dict(notes=notes_table(all_notes), all_notes=all_notes)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # save all the light choices at the participant level
        participant = player.participant

        # all the light fields must be added here as well
        participant.light_list = [player.light1,
                                  player.light2,
                                  player.light3,
                                  player.light4,
                                  player.light5,
                                  player.light6,
                                  player.light7]


class Guess1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number

        participant = player.participant
        all_notes = participant.notes

        # get the case corresponding to the round and sample only one row at random
        cases = participant.realized_cases

        # draw a random case number (random number at the participant level)
        # The index only indicates the position in the list of shuffled cases
        # so two participants with the same index might get different cases
        index = int(random.randint(0, len(cases)-1))
        player.case = index + 1

        # get the selected case and the notes corresponding to it
        case = cases[index]
        notes = all_notes[index]

        # sample one row from the case at random
        row = random.sample([i for i in range(len(case))], 1)[0]
        case_1 = case[row]

        n_lights = len(case_1)
        # save the row sampled as a string for the player
        player.row = str(case_1)

        # get the light that they chose in the previous stage and pass it to the function that writes the html code
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
        participant.sound.append(row[-1])
        if player.guess == row[-1]:
            participant.guesses.append(1)
        else:
            participant.guesses.append(0)


class Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        part = random.randint(2, 3)
        pay2 = 0
        pay3 = 0
        if part == 2:
            draw = random.sample([i for i in range(len(participant.guesses)-1)], 1)
            if participant.guesses[draw[0]] == participant.sound[draw[0]]:
                pay2 = 25
                player.payoff += 25
            else:
                player.payoff += 0

        else:
            if participant.sound[-1] == participant.guesses[-1]:
                player.payoff += 25
                pay3 = 25
            else:
                player.payoff += 0
                pay3 = 0

        return dict(pay=participant.payoff, guesses=sum(participant.guesses), p=part, p2=pay2, p3=pay3,
                    total=participant.payoff_plus_participation_fee())


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [MyWaitPage, Instructions, LightChoice, Guess1, Feedback]
