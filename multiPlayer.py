import enchant
d=enchant.Dict("en_US")


print("Word Quiz")


playerTurn=int(0)
word=""
startWith="any letter"
spentWords=[]

#nomination
nPlayers=int(2)
player=[[] for i in range(nPlayers)]

def nomination(nPlayers):
    for i in range(nPlayers):
        print("Name player",i+1,":",end = " ")
        player[i].append(input())
    for i in range(nPlayers):
        player[i].append(0)


def addScoreFor(value01):
    newScore=player[value01][1]+1
    player[value01].pop(1)
    player[value01].append(newScore)

def printScore():
    print("\n")
    print("SCORE:",player[0],"vs",player[1])

def printNextWord(startWith):
    print("enter a word starting with",startWith)

def isValid(word):
    if len(word)==int(1):
        print(word,"is alphabet or digit")
        return False
    try:
        word=int(word)
    except ValueError:
        pass
    else:
        print(word,"is a number")
        return False

    if d.check(word)==False:
        print(word,"is not a valid word")
        return False
    if word in spentWords:
        print(word,"has already been used")
        return False
    if startWith!="any letter" and wordTemp(0)!=startWith:
        
        print(word,"does not starts with",startWith)
        return False
    else:
        return True


def exitNow(phrase):
    if phrase=="khatam":
        printScore()
        print("\n goodbye")
        exit()

def inputWord(playerTurn,startWith,word,spentWords):
    while True:
        if playerTurn==int(0):
            printScore()
            printNextWord(startWith)
            print(player[playerTurn][0],": ",end="")
            wordTemp=input()
            exitNow(wordTemp)
            
            if isValid(wordTemp):
                word=wordTemp
                spentWords.append(word)
                startWith=word[-1]
                addScoreFor(playerTurn)
                playerTurn=int(1)
            else:
                
                print("try again!")
        
        if playerTurn==int(1):
            printScore()
            printNextWord(startWith)
            print(player[playerTurn][0],": ",end="")
            wordTemp=input()
            exitNow(wordTemp)
            
            if isValid(wordTemp):
                word=wordTemp
                spentWords.append(word)
                startWith=word[-1]
                addScoreFor(playerTurn)
                playerTurn=int(0)
            else:
                
                print("try again!")
		 	
		
		
	

nomination(nPlayers)
inputWord(playerTurn,startWith,word,spentWords)
	
	
	
