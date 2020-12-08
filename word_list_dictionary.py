from os import name, scandir
from random import choice


class DictionaryError(Exception):
    """
    raise errors occurred in dictionary class
    Attributes:
        expression - value which caused error
        message - explanation of error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class EmptyInputError(DictionaryError):
    pass


class BadSyntaxInputError(DictionaryError):
    pass


class WordListNotFoundError(DictionaryError):
    pass


class LexisExhaustedError(DictionaryError):
    pass


class Dictionary:
    """\
Dictionary:
    -get words/check if word exists from/in a small word list
    -helper for word_quiz.py

    usage:
        myDict = Dictionary("path_to_wordlist")

    functions:
        myDict.get_word("letter")
            -returned word starts with letter from wordlist
            -used by bot to get words to respond

        myDict.check_word("word")
            -returns True if word exists in wordlist
            -used to check if word entered by user is valid
            -as wordlist is fairly small this not always works correctly

    extras:
        myDict.stat_wordlist()
            -prints all letters and number of words from that letter in wordlist
"""

    def __init__(self, word_list_path):
        self.word_list_path = word_list_path
        self.lexis = {}

    def sanitized_string(self, this_string):
        try:
            if ord(this_string.strip()[0]) in range(97, 123):
                return this_string.strip().lower()
            else:
                raise WordListNotFoundError(this_string.strip()[0], "wordlist unavailable")

        except IndexError:
            raise EmptyInputError("", "Empty input")
        except SyntaxError:
            raise BadSyntaxInputError(this_string, "Input has bad syntax")

    def __words_is_used__(self, word):
        self.lexis[word[0]][0].remove(word)
        self.lexis[word[0]][1].append(word)

    def __lexis_maker__(self, letter):
        with open(self.word_list_path + letter) as word_file_path:
            self.lexis[letter] = word_file_path.read().splitlines(), []

    def get_word(self, letter):
        starting_with_this_letter = self.sanitized_string(letter)
        try:
            response = choice(self.lexis[starting_with_this_letter][0])
            self.__words_is_used__(response)
            return response

        except KeyError:
            self.__lexis_maker__(starting_with_this_letter)
            return self.get_word(starting_with_this_letter)

        except IndexError:
            raise LexisExhausted(starting_with_this_letter, "lexis exhausted")

    def check_word(self, word):
        check_this_word = self.sanitized_string(word)
        if len(check_this_word) < 2 or not check_this_word.isalpha():
            return False
        try:
            if (
                    check_this_word in self.lexis[check_this_word[0]][0]
                    or check_this_word in self.lexis[check_this_word[0]][1]
            ):
                self.__words_is_used__(check_this_word)
                return True
            return False

        except KeyError:
            self.__lexis_maker__(check_this_word[0])
            return self.check_word(check_this_word)

    def stat_wordlist(self):
        total_words = 0
        with scandir(self.word_list_path) as word_files:
            print(f"\nwordlist path: {self.word_list_path}")
            print("-------------------------------------------")
            print("letter     number of words from this letter")
            print("-------------------------------------------")
            for word_file in word_files:
                with open(word_file.path) as word_list:
                    word_list_length = len(word_list.read().splitlines())
                    total_words += word_list_length
                    print(f"""\
   {word_file.name:7}     {word_list_length:10} words
-------------------------------------------""")


if __name__ == "__main__":
    words_source_path = (
        ".\\words_list\\" if name == "nt"
        else "./words_list/"
    )
    my_dictionary = Dictionary(words_source_path)
    print(my_dictionary.__doc__)
    print("""\
DEMO
Enter show_stat to get stats of current wordlist or
Enter letters/words separated by commas,
to get word from letter or to check if word is valid\n:""", end="")
    user_choice = input().split(",")
    for item in user_choice:
        try:
            if item.strip() == "show_stat":
                my_dictionary.stat_wordlist()

            elif len(item.strip()) == 1:
                print(f"get word[{item.strip()}]: ", end="")
                print(my_dictionary.get_word(item))

            else:
                print(f"check word[{item.strip()}]: ", end="")
                print(my_dictionary.check_word(item))
        except (EmptyInputError, BadSyntaxInputError, WordListNotFoundError) as error:
            print(error)
    input("\nPress any key to exit...")
