from os import name, system
from time import sleep

from word_list_dictionary import Dictionary, EmptyInputError, BadSyntaxInputError, WordListNotFoundError, \
    LexisExhaustedError

start_with = "a"
spent_words = []
words_source_path, clear_command = (
    (".\\words_list\\", "cls") if name == "nt"
    else ("./words_list/", "clear")
)
dictionary = Dictionary(words_source_path)


# helpers functions for class Players
def add_to_spent_words(word):
    global spent_words
    spent_words.append(word.lower())


def change_start_with(word):
    global start_with
    start_with = word[-1].lower()


# class Players
class Players:
    def __init__(self, player_name):
        self.name = player_name
        self.score = 0

    def take_input(self):
        print(f"{self.name} [{self.score}] [{start_with}]: ", end="")

    def add_score(self, score_points=1):
        self.score += score_points


# helper functions for class User
def print_result(*, user_player, bot_player):
    print(
        f"\nYou [{user_player.score}]\nBot [{bot_player.score}]"
    )

    score_difference = user_player.score - bot_player.score

    if score_difference == 0:
        print("It was a tie. :)")

    elif score_difference < 0:
        print(
            f"{user_player.name} lost by {abs(score_difference)} points. :("
        )

    elif score_difference > 0:
        print(
            f"{user_player.name} won by {score_difference} points. :):)"
        )


def ask_to_exit():
    print("Exit? [y/n]: ", end="")
    if input() == "y":
        print_result(user_player=player1, bot_player=player2)
        print("\nEnter any key to exit..", end="")
        input()
        print("\n")
        exit()
    else:
        print()


def is_valid_word(word):
    global start_with
    global spent_words

    invalid_word_error = ""

    try:

        this_word = dictionary.sanitized_string(word)

        if not dictionary.check_word(this_word):
            invalid_word_error = "Not an english word."

        elif this_word[0] != start_with:
            invalid_word_error = f"Word does not start with '{start_with}'"

        elif word in spent_words:
            invalid_word_error = "Word has already been used."

    except EmptyInputError:
        ask_to_exit()
        return False
    except (BadSyntaxInputError, WordListNotFoundError):
        invalid_word_error = "Not an english word."

    if invalid_word_error:
        print(f"Error[{word}]: {invalid_word_error}")
        return False
    return True


class User(Players):
    def __init__(self, player_name=None, lives=3):
        self.life_wasted = 0
        self.life_total = lives
        if not player_name:
            player_name = "You"
        super(User, self).__init__(player_name)

    def play(self):
        self.take_input()
        input_word = input()

        if is_valid_word(input_word):
            self.life_wasted = 0
            self.add_score()
            change_start_with(input_word)
            add_to_spent_words(input_word)
            return
        else:
            self.life_wasted += 1
            if self.life_wasted < self.life_total:
                print(
                    f"{' ' * (9 + len(input_word))}{self.life_wasted} out of {self.life_total} chances wasted.\n"
                )
                self.play()
            else:
                self.life_wasted = 0
                print(f"""\
Error[Chances exhausted]: Bot will get chance to respond
                          press any key to continue..""", end="")
                input()
                return


def type_as_human(type_this, typing_delay=0.03):
    system(clear_command)
    for character in type_this:
        print(character, end="", flush=True)
        sleep(typing_delay)


def get_response():
    global start_with
    return dictionary.get_word(start_with)


class Bot(Players):
    def __init__(self, player_name=None):
        if not player_name:
            player_name = "Bot"
        super(Bot, self).__init__(player_name)

    def play(self):
        self.add_score()

        self.take_input()
        try:
            response = get_response()
            type_as_human(response + "\n")
            add_to_spent_words(response)
            change_start_with(response)
            return
        except LexisExhaustedError:
            response = f"I have exhausted my vocabulary of '{start_with}'.\n"
            type_as_human(response)
            print("Error[Bot exhausted words]: You will get chance to respond.\n")


if __name__ == "__main__":

    print("""\
    _=====================================_
    *              WORD QUIZ              *
    *                                     *           
    * joe [10] [a]:______________________ *
    * |   |    |    |                     *
    * |   |    |    enter your word here, *
    * |   |    |    enter without writing *
    * |   |    |    word to exit          *
    * |   |    |                          *
    * |   |    Enter word starting        *
    * |   |    with this letter           *
    * |   |                               *
    * |   player's score                  *
    * |                                   *
    * player's name                       *
    *=====================================*

    How To Play? 
    -Enter valid words as long as you can
    -Bot will try to keep up
    -One who lasts wins

    Rules:
    -Enter valid english words
    -Don't reuse words

    Disclaimer:
    -Word lists are a derivative of google ngrams,
     read ATTRIBUTIONS.txt for more details
    -Words are case-insensitive
    """)

    username = input("Enter your name: ").strip().capitalize()
    player1 = User(username)
    player2 = Bot(f"{'Bot':{len(player1.name)}}")

    print("")
    while True:
        player1.play()
        player2.play()
