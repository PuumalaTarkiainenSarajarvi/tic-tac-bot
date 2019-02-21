#Requires python 3.6.x
import discord
import random
import time
import tictacdb

gameRunning = False
startTime = 0
endTime = 0

lastTurn = [0,0]
incrementedRow = 0
firstRound = True


TOKEN = ' '
prefix = '!'
client = discord.Client()

        #1    2     3
game = [['\t', '\t', '\t'],    #A
        ['\t', '\t', '\t'],    #B
        ['\t', '\t', '\t']]    #C
rows = ['A', 'B', 'C']

def checkBoardFull():
    counter = 0
    for x in range(0,3):
        for y in range(0,3):
            if not game[x][y].strip():
                1+1
            else:
                counter += 1
    if counter == 9:
        return True
    else:
        return False
    
def botInput():

    if(checkBoardFull()):
        return False
    global firstRound
    
    found = False
    counter = 0

    if firstRound == False:
        x = lastTurn[0]
        y = lastTurn[1]
    
    while not found:
        if firstRound == True:
            x = random.randint(0,2)
            y = random.randint(0,2)
            lastTurn[0] = x
            lastTurn[1] = y

        
        
        if firstRound == False:
            if lastTurn[0] + 1 <= 2 and not game[lastTurn[0]+1][y].strip():
                x = lastTurn[0] + 1
                print("increment x")
                
            elif lastTurn[0] - 1 >=0 and not game[lastTurn[0]-1][y].strip():
                x = lastTurn[0] - 1
                print("decrement x")
            elif lastTurn[1] + 1 <= 2 and not game[x][lastTurn[1]+1].strip():
                y = lastTurn[1] + 1
                print("increment y")
            elif lastTurn[1] -1 >= 0 and not game[x][lastTurn[1]-1].strip():
                y = lastTurn[1] - 1
                print("decrement y")
            else:
                x = random.randint(0,2)
                y = random.randint(0,2)
                print("randomize")
                
        if not game[x][y].strip():
            game[x][y] = '  O '
            found = True
        
    if firstRound == True:
        firstRound = False

    lastTurn[0] = x
    lastTurn[1] = y
    print("end of loop", x,y)
        
    return found
        


def playerInput(message):
    msg = message.content.replace('!play','').strip()
    correctInput = False
    token = '  X '
    #Row 1
    if(msg == 'A1'):
        if not game[0][0].strip():
            game[0][0] = token
            correctInput = True

    elif(msg == 'A2'):
        if not game[0][1].strip():
            game[0][1] = token
            correctInput = True

    elif(msg == 'A3'):
        if not game[0][2].strip():
            game[0][2] = token
            correctInput = True
        
    #Row 2
    elif(msg == 'B1'):
        if not game[1][0].strip():
            game[1][0] = token
            correctInput = True
    
    elif(msg == 'B2'):
        if not game[1][1].strip():
            game[1][1] = token
            correctInput = True
        
    elif(msg == 'B3'):
        if not game[1][2].strip():
            game[1][2] = token
            correctInput = True
        
    #Row 3
    elif(msg == 'C1'):
        if not game[2][0].strip():
            game[2][0] = token
            correctInput = True
        
    elif(msg == 'C2'):
        if not game[2][1].strip():
            game[2][1] = token
            correctInput = True
        
    elif(msg == 'C3'):
        if not game[2][2].strip():
            game[2][2] = token
            correctInput = True
    
    
    return correctInput

def checkGameResult(playerToken):
    #Check if game ended from victory and return true if player with given token won

    #Check horizontal rows 
    for x in range(0,3):
        winCounter = 0
        for y in range(0,3):
            if playerToken in game[x][y]:
                winCounter = winCounter + 1
            if winCounter == 3:
                return True
            
    #Check vertical columns
    for y in range(0,3):
        winCounter = 0
        for x in range(0,3):
            if playerToken in game[x][y]:
                winCounter = winCounter + 1
            if winCounter == 3:
                return True

    #Check from upleft corner to downright corner
    winCounter = 0
    for i in range(0,3):
        if playerToken in game[i][i]:
            winCounter = winCounter + 1
        if winCounter == 3:
            return True

    #Check from upright corner to downleft corner
    winCounter = 0
    y = 2
    for x in range(0,3):
        if playerToken in game[x][y]:
            winCounter = winCounter + 1
        if winCounter == 3:
            return True
        y = y-1
        
    
    return False
        

def printBoard():
    board = "```_|  1 |  2 |  3 |\t\n"
    for y in range(0, 3):
            
            board += rows[y]+"|"
            for x in range(0, 3):
                location = game[y][x]
                board += location + "|"
            board += "\n"
    board +="```"
    return board

def endGame():
    global gameRunning
    for y in range(0, 3):
            for x in range(0, 3):
                game[y][x] = "\t"
    gameRunning = False

def getElapsedTime():
    global startTime
    endTime = time.time()
    elapsed = endTime - startTime
    elapsed = round(elapsed, 2)
    return elapsed
    

def setStartTime():
    global startTime
    startTime = time.time()
    

@client.event
async def on_ready():
    print('All set! Logged in as',  client.user.name)
    await client.change_presence(game=discord.Game(name="!help", type=0))
    
@client.event
async def on_message(message):
    msg = ""
    if message.content.startswith('!board'):

        msg = printBoard()
        
        await client.send_message(message.channel, msg)
        
    if message.content.startswith('!play'):
        
        global gameRunning
        if gameRunning == False:
            gameRunning = True
            await client.change_presence(game=discord.Game(name="TicTacToe", type=0))
            setStartTime()
            
        if(playerInput(message)):
            if(checkGameResult("X")):
                msg = "Game ended! You Won!\n"+"Game lasted for: "+str(getElapsedTime())+" seconds\n"+printBoard()
                endGame()
                await client.change_presence(game=discord.Game(name="!help", type=0))
                tictacdb.insertHighScore(str(message.author), getElapsedTime())
            elif(botInput()):
                if(checkGameResult("O")):
                    msg = "Game ended! You lost!\n"+"Game lasted for: "+str(getElapsedTime())+" seconds\n"+printBoard()
                    tictacdb.insertHighScore("TicTacBot", getElapsedTime())
                    endGame()
                    await client.change_presence(game=discord.Game(name="!help", type=0))
                else:
                    msg = printBoard()
            else:
                msg = "Game ended!\n"+printBoard()
                endGame()
        else: msg ="Incorrect input"
        
        await client.send_message(message.channel, msg)

    if message.content.startswith('!help'):
        msg = """```I'm a bot that plays TicTacToe with you!\n\nWrite !play following with coordinates where you want to play.\nA B C for horizontal rows and 1 2 3 for vertical columns i.e. !play A1\n
!board to see the gameboard\n!scores to see high scores```"""
        await client.send_message(message.channel, msg)

    if message.content.startswith('!scores'):
        scoresList = tictacdb.getHighScores()
        length = len(scoresList)
        msg="```-----Hall of fame-----\n"
        for x in range(0,length):
            for y in range(0,2):
                msg += str(scoresList[x][y])+" "
            msg+="seconds\n"
        msg+="```"
        await client.send_message(message.channel, msg)
        
        
        
        

client.run(TOKEN)
