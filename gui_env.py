import Tkinter as tk
import socket
import os
import threading
import sys


#Constants for Connection
PLAYER = '1'; ENEMY = '2'
BUFFER = 512
serverIP = "127.0.0.1"
port = 50250

clientSocket = None
readySignal = False
settleShipSignal = 5

ship_locations = []  # Player's ships' locations
direction = 'h'


#CONSTANTS for GUI
ROWS = 10
COLUMNS = 10

BACKGROUNDCOLOR = '#000000'
SHIPCOLOR = '#a0b2c4'
HITCOLOR = '#f01200'
MISSCOLOR = '#00e1aa'
GAMESTATCOLOR = '#9d99fc'
PLAYERSTATCOLOR = '#a50415'
PLAYERCOLOR = '#f0e1d2'
GAMETITLECOLOR = '#00ff99'
BUTTONCOLOR = ""

buttonPlay = None
gameStat = None
playerStat = None
enemyStat = None

buttonsGridPlayerArray = []
buttonsGridEnemyArray = []
buttonsDisabledArray = []



#Functions

def enable_ready():
    buttonPlay['state'] = 'normal'

def disable_ready():
    buttonPlay['state'] = 'disabled'


def player_board_setting(x, y):
    set_ship_position(x, y)

def enemy_board_setting(x, y):
    global buttonsDisabledArray
    if buttonsDisabledArray[x][y] == False:
        buttonsDisabledArray[x][y] = True
        send_thread = threading.Thread(target=sendInstruction, args=['' + str(x) + str(y)])
        send_thread.start()


def enable_player_grid():
    global BUTTONCOLOR
    for x in range(COLUMNS):
        for y in range(ROWS):
            buttonsGridPlayerArray[x][y].configure(background=BUTTONCOLOR)
            buttonsGridPlayerArray[x][y]['state'] = 'normal'

def disable_player_grid():
    for x in range(COLUMNS):
        for y in range(ROWS):
            buttonsGridPlayerArray[x][y]['state'] = 'disabled'


def enable_enemy_grid():
    for x in range(COLUMNS):
        for y in range(ROWS):
            buttonsGridEnemyArray[x][y]['state'] = 'normal'

def disable_enemy_grid():
    for x in range(COLUMNS):
        for y in range(ROWS):
            buttonsGridEnemyArray[x][y]['state'] = 'disabled'


def player_board_create():
    # Rendering player's board
    for x in range(COLUMNS):
        tempButtonsArray = []
        for y in range(ROWS):
            # b = tk.Button(bottomSubFrame_ONE, text=" ", height=2, width=3)
            b = tk.Button(bottomSubFrame_ONE, command=lambda x=x, y=y: player_board_setting(x, y), text=" ", height=2,
                          width=3)
            b.grid(row=x, column=y)
            tempButtonsArray.append(b)
        buttonsGridPlayerArray.append(tempButtonsArray)
    disable_player_grid()


def enemy_board_create():
    # Rendering enemy's board
    for x in range(COLUMNS):
        tempButtonsArray = []
        temp_flag_list = []
        for y in range(ROWS):
            # b = tk.Button(bottomSubFrame_THREE, text=" ", height=2, width=3)
            b = tk.Button(bottomSubFrame_THREE, command=lambda x=x, y=y: enemy_board_setting(x, y), text=" ", height=2,
                          width=3)
            b.grid(row=x, column=y)
            tempButtonsArray.append(b)
            temp_flag_list.append(False)
        buttonsGridEnemyArray.append(tempButtonsArray)
        buttonsDisabledArray.append(temp_flag_list)
    disable_enemy_grid()


def getAttackInstruction():
    global clientSocket
    instruction = clientSocket.recv(BUFFER)
    performOperation(instruction)


def sendInstruction(attackPosition):
    global clientSocket
    clientSocket.send(attackPosition)


def checkOperationToPerform():
    global clientSocket
    while True:
        try:
            hit_or_miss = clientSocket.recv(BUFFER)
            instruction = clientSocket.recv(BUFFER)
            performOperation(hit_or_miss)
            performOperation(instruction)
        except:
            pass
            # Game Over Here



"""
    This instruction is received from server informing where hit or miss has occurred
    instruction starts with whether hit or miss has occurred
    followed by a number indicating which grid at client side should be reflected
    (2 for opponent 1 for player) followed by 2 numbers indicating position of attack
    followed by 2 numbers indicating number of ships sank of player 1(player) and 2(enemy) respectively
"""
def performOperation(instruction):
    global clientSocket
    if instruction == 'attack':
        gameStat.config(text="ATTACK!")
        enable_enemy_grid()
    elif instruction == 'wait':
        gameStat.config(text="HOLD!")
        disable_enemy_grid()
    elif instruction.startswith('hit'):
        # Change GUI accordingly to RED as it HIT.
        # Check if this is HIT on player or opponent
        if instruction[3] == PLAYER:
            # Change player's board
            x = int(instruction[4])
            y = int(instruction[5])
            buttonsGridPlayerArray[x][y].configure(bg=HITCOLOR)
        else:
            # Change enemy's board
            x = int(instruction[4])
            y = int(instruction[5])
            buttonsGridEnemyArray[x][y].configure(bg=HITCOLOR)
        playerStat.configure(text="Your Ships Destroyed - " + instruction[6])
        enemyStat.configure(text="Opponent's Ships Destroyed - " + instruction[7])
    elif instruction.startswith('miss'):
        # Change GUI accordingly to LIGHT BLUE as it's MISS.
        # Check if this is MISS on player or opponent
        if instruction[4] == PLAYER:
            # Changes in player board
            x = int(instruction[5])
            y = int(instruction[6])
            buttonsGridPlayerArray[x][y].configure(bg=MISSCOLOR)
        else:
            # Change enemy's board
            x = int(instruction[5])
            y = int(instruction[6])
            buttonsGridEnemyArray[x][y].configure(bg=MISSCOLOR)
        playerStat.configure(text="Your Ships destroyed - " + instruction[7])
        enemyStat.configure(text="Opponent's Ships destroyed - " + instruction[8])
    elif instruction == 'win':
        # Game over and player wins the game
        gameStat.config(text="You Conquered the Sea")
        clientSocket.close()
        disable_enemy_grid()  # Disables enemy grid when player won.
        return
    elif instruction == 'lost':
        # Game over and player lost the game
        gameStat.config(text="You're Drowned. Rest in Peace!")
        clientSocket.close()
        return


def send_ready():
    global clientSocket, ship_locations
    if readySignal == False:
        gameStat.config(text="Select ship positions")
        return
    disable_ready()

    ships = ''
    for ship in ship_locations:
        for loc in ship:
            ships += loc
            ships += ','
        ships = ships[0:-1]
        ships += '|'
    ships = ships[0:-1]
    clientSocket.send(ships)

    gameStat.configure(text='Waiting for oppenent to be ready!')
    disable_player_grid()
    my_thread = threading.Thread(target=getAttackInstruction)
    my_thread.start()
    my_thread = threading.Thread(target=checkOperationToPerform)
    my_thread.start()


def set_ship_position(x, y):
    global settleShipSignal
    global readySignal

    # validates x & y and sets 5 block of ship
    if settleShipSignal == 5:
        if set_ship(5, x, y):
            settleShipSignal = settleShipSignal - 1
            gameStat.config(text="Select ship of 4 blocks")
    # validates x & y and sets 4 block of ship
    elif settleShipSignal == 4:
        if set_ship(4, x, y):
            settleShipSignal = settleShipSignal - 1
            gameStat.config(text="Select ship of 3 blocks")
    # validates x & y and sets 3 block of ship
    elif settleShipSignal == 3:
        if set_ship(3, x, y):
            settleShipSignal = settleShipSignal - 1
            gameStat.config(text="Select ship of 2 blocks")
    # validates x & y and sets 2 block of ship
    elif settleShipSignal == 2:
        if set_ship(2, x, y):
            settleShipSignal = settleShipSignal - 1
            gameStat.config(text="Select ship of 1 blocks")
    # sets 1 block of ship
    elif settleShipSignal == 1:
        if set_ship(1, x, y):
            settleShipSignal = settleShipSignal - 1
            gameStat.config(text="Let's Play!")
            readySignal = True


def set_ship(ship_length, x, y):
    global direction
    if direction == 'h':
        return set_ship_horizontal(ship_length, x, y)
    else:
        return set_ship_vertical(ship_length, x, y)


def set_ship_horizontal(ship_length, x, y):
    if y + ship_length > COLUMNS:
        return False
    ship = []
    for i in range(ship_length):
        loc = str(x) + str(y + i)
        if is_already_in_list(loc):
            return False
    for i in range(ship_length):
        loc = str(x) + str(y + i)
        ship.append(loc)
        buttonsGridPlayerArray[x][y + i].configure(bg=SHIPCOLOR)
        buttonsGridPlayerArray[x][y + i]['state'] = 'disabled'
    ship_locations.append(ship)
    return True

def set_ship_vertical(ship_length, x, y):
    if x + ship_length > ROWS:
        return False
    ship = []
    for i in range(ship_length):
        loc = str(x + i) + str(y)
        if is_already_in_list(loc):
            return False
    for i in range(ship_length):
        loc = str(x + i) + str(y)
        ship.append(loc)
        buttonsGridPlayerArray[x + i][y].configure(bg=SHIPCOLOR)
        buttonsGridPlayerArray[x + i][y]['state'] = 'disabled'
    ship_locations.append(ship)
    return True


def is_already_in_list(location):
    for ship in ship_locations:
        for loc in ship:
            if location == loc:
                return True
    return False


def connect_to_server():
    global clientSocket
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverIP, port))
        gameStat.configure(text="Let's Play!")
        server_ready = clientSocket.recv(BUFFER)

        enable_player_grid()
        enable_ready()
        gameStat.config(text="Select ship of 5 blocks")
    except Exception as e:
        print e
        print e.message
        print e.args
        gameStat.configure(text="Connection cannot be established..")


#Function to change orientation for aligning ships
def changeOrientation(event=None):
    global direction
    if direction == 'v':
        direction = 'h'
        gameStat.configure(text='Set ships horizontally')
    else:
        direction = 'v'
        gameStat.configure(text='Set ships vertically')



#Creating Tkinter window and frames
root = tk.Tk()
root.title("Sink The Ship")
rootFrame = tk.Frame(root, bg=BACKGROUNDCOLOR)
rootFrame.pack()

topFrame = tk.Frame(rootFrame, bg=BACKGROUNDCOLOR)
topFrame.grid(row=0, column=0)

middleFrame = tk.Frame(rootFrame, bg=BACKGROUNDCOLOR)
middleFrame.grid(row=1, column=0, rowspan=10)

bottomFrame = tk.Frame(rootFrame, bg=BACKGROUNDCOLOR)
bottomFrame.grid(row=11, column=0)


#Top Frame Labels
playerStat = tk.Label(topFrame, text="Game Not Started", font=("Times New Roman", 15), bg=BACKGROUNDCOLOR, fg=PLAYERSTATCOLOR)
playerStat.grid(row=0, column=0)
enemyStat = tk.Label(topFrame, text="Game Not Started", font=("Times New Roman", 15), bg=BACKGROUNDCOLOR, fg=PLAYERSTATCOLOR)
enemyStat.grid(row=0, column=5)
gameStat = tk.Label(topFrame, text="Let's Play!", font=("Times New Roman", 15), bg=BACKGROUNDCOLOR, fg=GAMESTATCOLOR)
gameStat.grid(row=0, column=2, columnspan=2, pady=3, padx=10)


# Bottom Frame Labels
playerLabel = tk.Label(bottomFrame, text="Your Ships", font=("Times New Roman", 15), bg=BACKGROUNDCOLOR, fg=PLAYERCOLOR)
playerLabel.grid(row=0, column=0)
enemyLabel = tk.Label(bottomFrame, text=" Opponent's Ships", font=("Times New Roman", 15), bg=BACKGROUNDCOLOR, fg=PLAYERCOLOR)
enemyLabel.grid(row=0, column=5)
gameLabel = tk.Label(bottomFrame, text=">>>> SINK THE SHIP <<<<", font=("Times New Roman", 20), bg=BACKGROUNDCOLOR, fg=GAMETITLECOLOR)
gameLabel.grid(row=0, column=2, columnspan=2, pady=3, padx=10)


# Subframes inside Middle Frame for creating Player's and Enemy's Grid
bottomSubFrame_ONE = tk.Frame(middleFrame, bg=BACKGROUNDCOLOR)
bottomSubFrame_ONE.grid(row=0, column=0, columnspan=5, padx=10)

bottomSubFrame_TWO = tk.Frame(middleFrame, bg=BACKGROUNDCOLOR)
bottomSubFrame_TWO.grid(row=0, column=5, columnspan=2)

bottomSubFrame_THREE = tk.Frame(middleFrame, bg=BACKGROUNDCOLOR)
bottomSubFrame_THREE.grid(row=0, column=7, columnspan=5, padx=10)


# Temp button for getting default background color
BUTTONCOLOR = tk.Button(root).cget('background')


#buttonPlay = tk.Button(bottomSubFrame_TWO, text="PLAY!", height=3, width=12)
buttonPlay = tk.Button(bottomSubFrame_TWO, text="PLAY!", height=3, width=12, command=send_ready)
buttonPlay.grid(row=0, column=0, rowspan=4, pady=100, padx=10)
#disable_ready()

try:
    serverIP = sys.argv[1]#"192.168.43.43"
    port = 50250
except:
    print "Unable to connect. IP or Port not available."
    sys.exit()

player_board_create()
enemy_board_create()
disable_ready()

# Connect to server
connection = threading.Thread(target=connect_to_server)
connection.start()


# Display GUI
root.resizable(width=False, height=False)
root.bind("<space>", changeOrientation)
root.mainloop()
os._exit(0)




