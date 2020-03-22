import os
import enchant
import random
import sys
import time

#nomination
scoreboard=[["Null",0],["Bot",0]]
def nomination():
    print("WORD QUIZ")
    global scoreboard
    scoreboard[0][0]=input("Enter Your Name: ")
    print("Let's Play,"+scoreboard[0][0])

#add score
player_turn=0
def add_score():
    global player_turn
    global scoreboard

    if player_turn==0:
        scoreboard[0][1]=scoreboard[0][1]+1

    if player_turn==1:
        scoreboard[1][1]=scoreboard[1][1]+1
        

#print score
def print_score():
    global scoreboard
    print("\nScore:",scoreboard[0][0]+"["+str(scoreboard[0][1])+"] |",scoreboard[1][0]+"["+str(scoreboard[1][1])+"]")
    
#print start_with

start_with="Any Letter"
def print_start_with():
    global start_with
    print("Enter A Word Starting With,'"+start_with+"'.")


#check if input is a valid  word
input_word=""
spent_words=[]
def is_valid_word():
    dictionary=enchant.Dict("en_US")
    global input_word
    global start_with
    global spent_words

    try:
        input_word=input_word.lower()
    except AttributeError:
        print("Invalid Word!")
        return False

    if len(input_word)==1:
        print("Invalid Word!")
        return False

    if  dictionary.check(input_word)==False:
        print("Invalid Word!")
        return False

    if start_with!="Any Letter" and input_word[0]!=start_with:
        print(input_word,"Does Not Starts With",start_with+"!")
        return False

    if input_word in spent_words:
        print(input_word,"Has Already Been Used!")
        return False

    else:
        return True



#end game
def endgame():
    global input_word
    global scoreboard

    if input_word=="exit00":
        print_score()
        score_difference=scoreboard[0][1]-scoreboard[1][1]

        if score_difference<0:
            print(scoreboard[1][0],"Won By",abs(score_difference)+".")
        elif score_difference>0:
            print(scoreboard[0][0],"Won By",abs(score_difference)+".")
        else:
            print("It Was A Tie.")
        print("\nGoodBye!")
        sys.exit()

#player input

def player_input():
    while True:
        global player_turn
        global scoreboard
        global input_word
        global spent_words
        global start_with

        if player_turn==0:
            print_score()
            print_start_with()
            print(scoreboard[0][0]+": ",end="")
            input_word=input()

            endgame()

            if is_valid_word():
                start_with=input_word[-1].lower()
                spent_words.append(input_word.lower())
                add_score()
                player_turn=1
                break
            else:
                print("Try Again!")


#-starting to build me-#

#import words to an array from word files

if os.name == "nt":
    path=".\\wordsFiltered\\"
else:
    path="./wordsFiltered/"

lexis=[[] for i in range(97,123)]

def preparation():
    global path
    global lexis
    
    print("Preparing...\nImporting Words...")
    for i in range(97,123):
        temp_path=path+chr(i)+".txt"
        temp_lexis=open(temp_path).read().splitlines()

        for j in temp_lexis:
            lexis[i-97].append(j)

    print("Done.\n")
    
    

#pick a word and respond

response=""
def me_response():
    global start_with
    global lexis
    global response
    global spent_words
    global input_word
    global player_turn

    while True:
        lexis_target_array=ord(start_with.lower())-97
        length=(len(lexis[lexis_target_array])-1)
        
        if length <= 0:
            print("Bot exhausted all words starting with,"+start_with.lower()+" :(")
            print("\nTo Win Enter a word starting with,"+start_with.lower()+": ",end="")
            input_word=input()
            if is_valid_word():
                input_word="exit00"
                endgame()
            else:
                print("It Was A Tie")
                sys.exit()
                
        
        lexis_target_position=random.randint(0,length)
        

        response=lexis[lexis_target_array][lexis_target_position]

        if response in spent_words:
            pass
        else:
            break

    lexis[lexis_target_array].pop(lexis_target_position)
    spent_words.append(response)
    start_with=response[-1].lower()
    add_score()
    
    for i in response:
        print(i,end="")
        time.sleep(0.05)

    print("\n")
    player_turn=0



#giving platform for me to write

def me_input():
    global player_turn

    if player_turn==1:
            print_score()
            print_start_with()
            print(scoreboard[1][0]+": ",end="")
            me_response()

        

    

#gameplay
preparation()
nomination()

while True:
    player_input()
    me_input()
            
            
            
            































