import Tkinter as tk
import socket
import os
import threading
import sys

border_width = 10; border_height = 10
PLAYER = '1'; ENEMY = '2'

ready_flag = False
BUFFER = 512
ip_of_server = '127.0.0.1'
port = 5250

clientsocket = None
shipsettleflag = 5

buttons_player = []
buttons_enemy = []

ready_button = None
gamestat = None
playerstat = None
enemystat = None

ship_locations = []  # Player's ships' locations
direction = 'h'
button_disable_flags = []

button_color = ""
bg_color = '#000000'
game_status_color = '#9d99fc'
player_status_color = '#a50415'
player_color = '#f0e1d2'
game_name_color = '#00ff99'
hit_color = '#f01200'
miss_color = '#00e1aa'
ship_color = '#a0b2c4'


def disable_ready():
    ready_button['state'] = 'disabled'


def enable_ready():
    ready_button['state'] = 'normal'


def disable_player_grid():
    for x in range(border_height):
        for y in range(border_width):
            buttons_player[x][y]['state'] = 'disabled'


def enable_player_grid():
    global button_color
    for x in range(border_height):
        for y in range(border_width):
            buttons_player[x][y].configure(background=button_color)
            buttons_player[x][y]['state'] = 'normal'


def disable_enemy_grid():
    for x in range(border_height):
        for y in range(border_width):
            buttons_enemy[x][y]['state'] = 'disabled'


def enable_enemy_grid():
    for x in range(border_height):
        for y in range(border_width):
            buttons_enemy[x][y]['state'] = 'normal'


def enable_enemy_grid_partialy():
    for x in range(border_height):
        for y in range(border_width):
            buttons_enemy[x][y]['state'] = 'normal'


def getAttackInstruction():
    global clientsocket
    instruction = clientsocket.recv(BUFFER)
    performOperation(instruction)


def sendInstruction(attackPosition):
    global clientsocket
    clientsocket.send(attackPosition)


def checkOperationToPerform():
    global clientsocket
    while True:
        try:
            hit_or_miss = clientsocket.recv(BUFFER)
            instruction = clientsocket.recv(BUFFER)
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
    global clientsocket
    if instruction == 'attack':
        gamestat.config(text="ATTACK!")
        enable_enemy_grid()
    elif instruction == 'wait':
        gamestat.config(text="HOLD!")
        disable_enemy_grid()
    elif instruction.startswith('hit'):
        # Change GUI accordingly to RED as it HIT.
        # Check if this is HIT on player or opponent
        if instruction[3] == PLAYER:
            # Change player's board
            x = int(instruction[4])
            y = int(instruction[5])
            buttons_player[x][y].configure(bg=hit_color)
        else:
            # Change enemy's board
            x = int(instruction[4])
            y = int(instruction[5])
            buttons_enemy[x][y].configure(bg=hit_color)
        playerstat.configure(text="Your Ships Destroyed - " + instruction[6])
        enemystat.configure(text="Opponent's Ships Destroyed - " + instruction[7])
    elif instruction.startswith('miss'):
        # Change GUI accordingly to LIGHT BLUE as it's MISS.
        # Check if this is MISS on player or opponent
        if instruction[4] == PLAYER:
            # Changes in player board
            x = int(instruction[5])
            y = int(instruction[6])
            buttons_player[x][y].configure(bg=miss_color)
        else:
            # Change enemy's board
            x = int(instruction[5])
            y = int(instruction[6])
            buttons_enemy[x][y].configure(bg=miss_color)
        playerstat.configure(text="Your Ships destroyed - " + instruction[7])
        enemystat.configure(text="Opponent's Ships destroyed - " + instruction[8])
    elif instruction == 'win':
        # Game over and player wins the game
        gamestat.config(text="You Conquered the Sea")
        clientsocket.close()
        disable_enemy_grid()  # Disables enemy grid when player won.
        return
    elif instruction == 'lost':
        # Game over and player lost the game
        gamestat.config(text="You're Drowned. Rest in Peace!")
        clientsocket.close()
        return


def send_ready():
    global clientsocket, ship_locations
    if ready_flag == False:
        gamestat.config(text="Select ship positions")
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
    clientsocket.send(ships)

    gamestat.configure(text='Waiting for oppenent to be ready!')
    disable_player_grid()
    my_thread = threading.Thread(target=getAttackInstruction)
    my_thread.start()
    my_thread = threading.Thread(target=checkOperationToPerform)
    my_thread.start()


def player_board_fn(x, y):
    set_ship_position(x, y)


def set_ship_position(x, y):
    global shipsettleflag
    global ready_flag

    # validates x & y and sets 5 block of ship
    if shipsettleflag == 5:
        if set_ship(5, x, y):
            shipsettleflag = shipsettleflag - 1
            gamestat.config(text="Select ship of 4 blocks")
    # validates x & y and sets 4 block of ship
    elif shipsettleflag == 4:
        if set_ship(4, x, y):
            shipsettleflag = shipsettleflag - 1
            gamestat.config(text="Select ship of 3 blocks")
    # validates x & y and sets 3 block of ship
    elif shipsettleflag == 3:
        if set_ship(3, x, y):
            shipsettleflag = shipsettleflag - 1
            gamestat.config(text="Select ship of 2 blocks")
    # validates x & y and sets 2 block of ship
    elif shipsettleflag == 2:
        if set_ship(2, x, y):
            shipsettleflag = shipsettleflag - 1
            gamestat.config(text="Select ship of 1 blocks")
    # sets 1 block of ship
    elif shipsettleflag == 1:
        if set_ship(1, x, y):
            shipsettleflag = shipsettleflag - 1
            gamestat.config(text="Let's Play!")
            ready_flag = True


def set_ship(ship_length, x, y):
    global direction
    if direction == 'h':
        return set_ship_horizontal(ship_length, x, y)
    else:
        return set_ship_vertical(ship_length, x, y)


def set_ship_vertical(ship_length, x, y):
    if x + ship_length > border_width:
        return False
    ship = []
    for i in range(ship_length):
        loc = str(x + i) + str(y)
        if is_already_in_list(loc):
            return False
    for i in range(ship_length):
        loc = str(x + i) + str(y)
        ship.append(loc)
        buttons_player[x + i][y].configure(bg=ship_color)
        buttons_player[x + i][y]['state'] = 'disabled'
    ship_locations.append(ship)
    return True


def set_ship_horizontal(ship_length, x, y):
    if y + ship_length > border_height:
        return False
    ship = []
    for i in range(ship_length):
        loc = str(x) + str(y + i)
        if is_already_in_list(loc):
            return False
    for i in range(ship_length):
        loc = str(x) + str(y + i)
        ship.append(loc)
        buttons_player[x][y + i].configure(bg=ship_color)
        buttons_player[x][y + i]['state'] = 'disabled'
    ship_locations.append(ship)
    return True


def is_already_in_list(location):
    for ship in ship_locations:
        for loc in ship:
            if location == loc:
                return True
    return False

def changeorientation(event=None):
    global direction
    if direction == 'v':
        direction = 'h'
        gamestat.configure(text='Set ships horizontally')
    else:
        direction = 'v'
        gamestat.configure(text='Set ships vertically')

def enemy_board_fn(x, y):
    global button_disable_flags
    if button_disable_flags[x][y] == False:
        button_disable_flags[x][y] = True
        send_thread = threading.Thread(target=sendInstruction, args=['' + str(x) + str(y)])
        send_thread.start()


def connect_to_server():
    global clientsocket
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((ip_of_server, port))
        gamestat.configure(text="Let's Play!")


        server_ready = clientsocket.recv(BUFFER)

        enable_player_grid()
        enable_ready()
        #reset_button['state'] = 'normal'
        #vertical_button['state'] = 'normal'
        gamestat.config(text="Select ship of 5 blocks")
    except Exception as e:
        print e
        print e.message
        print e.args
        gamestat.configure(text="Connection cannot be established..")


try:
    ip_of_server = " 172.16.16.184"
    port = 5250
except:
    print "Unable to connect. IP or Port not available."
    sys.exit()

# GUI rendering
root = tk.Tk()
root.title("Sink The Ship")
fr_main = tk.Frame(root, bg=bg_color)
fr_main.pack()

# Temp button for getting default background color
button_color = tk.Button(root).cget('background')

fr_upper = tk.Frame(fr_main, bg=bg_color)
fr_upper.grid(row=0, column=0)

# Statuses
playerstat = tk.Label(fr_upper, text="", font=("Helvetica", 15), bg=bg_color, fg=player_status_color)
enemystat = tk.Label(fr_upper, text="", font=("Helvetica", 15), bg=bg_color, fg=player_status_color)
gamestat = tk.Label(fr_upper, text="Let's Play!", font=("Helvetica", 15), bg=bg_color, fg=game_status_color)

playerstat.grid(row=0, column=0)
gamestat.grid(row=0, column=2, columnspan=2, pady=3, padx=10)
enemystat.grid(row=0, column=5)

fr_lower = tk.Frame(fr_main, bg=bg_color)
fr_lower.grid(row=1, column=0, rowspan=10)

fr_1 = tk.Frame(fr_lower, bg=bg_color)
fr_1.grid(row=0, column=0, columnspan=5, padx=10)

# Rendering player's board
for x in range(border_height):
    temp_buttons = []
    for y in range(border_width):
        b = tk.Button(fr_1, command=lambda x=x, y=y: player_board_fn(x, y), text=" ", height=2, width=3)
        b.grid(row=x, column=y)
        temp_buttons.append(b)
    buttons_player.append(temp_buttons)
disable_player_grid()

fr_2 = tk.Frame(fr_lower, bg=bg_color)
fr_2.grid(row=0, column=5, columnspan=2)

ready_button = tk.Button(fr_2, text="PLAY!", height=3, width=12, command=send_ready)
ready_button.grid(row=0, column=0, rowspan=4, pady=100, padx=10)
disable_ready()
fr_3 = tk.Frame(fr_lower, bg=bg_color)
fr_3.grid(row=0, column=7, columnspan=5, padx=10)

# Rendering enemy's board
for x in range(border_height):
    temp_buttons = []
    temp_flag_list = []
    for y in range(border_width):
        b = tk.Button(fr_3, command=lambda x=x, y=y: enemy_board_fn(x, y), text=" ", height=2, width=3)
        b.grid(row=x, column=y)
        temp_buttons.append(b)
        temp_flag_list.append(False)
    buttons_enemy.append(temp_buttons)
    button_disable_flags.append(temp_flag_list)
disable_enemy_grid()

fr_bottom = tk.Frame(fr_main, bg=bg_color)
fr_bottom.grid(row=11, column=0)

# Statuses
l_player = tk.Label(fr_bottom, text="Player's Ships", font=("Helvetica", 15), bg=bg_color, fg=player_color)
l_enemy = tk.Label(fr_bottom, text=" Opponent's Ships", font=("Helvetica", 15), bg=bg_color, fg=player_color)
l_game_name = tk.Label(fr_bottom, text=">>>> SINK THE SHIP <<<<", font=("Times New Roman", 20), bg=bg_color,
                       fg=game_name_color)

l_player.grid(row=0, column=0)
l_game_name.grid(row=0, column=2, columnspan=2, pady=3, padx=10)
l_enemy.grid(row=0, column=5)

# Information
"""
tk.Button(fr_bottom, text=" ", height=2, width=3, bg=ship_color).grid(row=1, column=0)
tk.Button(fr_bottom, text=" ", height=2, width=3, bg=hit_color).grid(row=2, column=0)
tk.Button(fr_bottom, text=" ", height=2, width=3, bg=miss_color).grid(row=3, column=0)
tk.Label(fr_bottom, text="Ship Color", font=("Helvetica", 10), bg=bg_color).grid(row=1, column=1)
tk.Label(fr_bottom, text="HIT Color", font=("Helvetica", 10), bg=bg_color).grid(row=2, column=1)
tk.Label(fr_bottom, text="MISS Color", font=("Helvetica", 10), bg=bg_color).grid(row=3, column=1)
"""

# Connect to server
connection = threading.Thread(target=connect_to_server)
connection.start()

# Display GUI
root.resizable(width=False, height=False)
root.bind("<space>", changeorientation)
root.mainloop()
os._exit(0)
