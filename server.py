import socket
import threading
import sys


class Playground:

    def getcoordinates(self, conn, player):
        
        self.player1List = []  # contains ship positions of player 1
        self.player2List = []  # contains ship positions of player 2
        positions = ''
        try:
            positions = str(conn.recv(512)).strip()
        except:
            print "Error : Player is not reachable."
            return
        
        positionlist = positions.split("|")
        
        if player == 1:
            for i in positionlist:
                self.player1List.append(i.split(","))
        else:
            for i in positionlist:
                self.player2List.append(i.split(","))
                
        self.no_ship = len(self.player1List)

    def establishconnection(self, sock):
        
        self.playerconn1, addr = sock.accept()
        self.playerconn2, addr = sock.accept()
        self.startgame()
        print "New Arena created."


    def startgame(self):
        
        self.playerconn1.send('ready')
        self.playerconn2.send('ready')


    def stopgame(self):
    
        self.game_running_flag = False
        self.playerconn1.close()
        self.playerconn2.close()

    def checkwin(self, player):
        
        if player == 1:
            if len(self.player2List) == 0:
                self.playerconn1.send("win")
                self.playerconn2.send("lost")
                self.stopgame()
                return True
        else:
            if len(self.player1List) == 0:
                self.playerconn1.send("lost")
                self.playerconn2.send("win")
                self.stopgame()
                return True
            
        return False


    def checkhit(self, pos, player):
        
        if player == 1:
            for i in self.player2List:
                if pos in i:
                    i.remove(pos)
                    if len(i) == 0:
                        self.player2List.remove(i)
                    return True
            return False
        else:
            for i in self.player1List:
                if pos in i:
                    i.remove(pos)
                    if len(i) == 0:
                        self.player1List.remove(i)
                    return True
            return False


    def attack(self, conn, player):
        
        self.drownedShip1 = "0"
        self.drownedShip2 = "0"
        try:
            while True:
                pos = conn.recv(512)
                if self.game_running_flag == False:
                    return
                if player == 1:
                    if self.checkhit(pos, player):
                        # This instruction is sent to both client informing where hit or miss has occurred
                        # instruction starts with whether hit or miss has occurred
                        # followed by a number indicating which grid at client side should be reflected
                        # (2 for opponent 1 for player) followed by 2 numbers indicating position of attack
                        # followed by 2 numbers indicating number of ships sank of player and opponent respectively
                        self.drownedShip2=str(self.no_ship-len(self.player2List))
                        self.playerconn1.send("hit2" + pos+self.drownedShip1+self.drownedShip2)
                        self.playerconn2.send("hit1" + pos+self.drownedShip2+self.drownedShip1)
                        if self.checkwin(player):
                            return
                        self.playerconn1.send("attack")
                        self.playerconn2.send("wait")
                    else:
                        self.playerconn1.send("miss2" + pos+self.drownedShip1+self.drownedShip2)
                        self.playerconn2.send("miss1" + pos+self.drownedShip2+self.drownedShip1)
                        self.playerconn1.send("wait")
                        self.playerconn2.send("attack")
                else:
                    if self.checkhit(pos, player):
                        self.drownedShip1 = str(self.no_ship - len(self.player1List))
                        self.playerconn1.send("hit1" + pos+self.drownedShip1+self.drownedShip2)
                        self.playerconn2.send("hit2" + pos+self.drownedShip2+self.drownedShip1)
                        if self.checkwin(player):
                            return
                        self.playerconn1.send("wait")
                        self.playerconn2.send("attack")
                    else:
                        self.playerconn1.send("miss1" + pos+self.drownedShip1+self.drownedShip2)
                        self.playerconn2.send("miss2" + pos+self.drownedShip2+self.drownedShip1)
                        self.playerconn1.send("attack")
                        self.playerconn2.send("wait")
        except Exception as e:
            print e.message
            print "Error : Player forcefully terminated connection."


    def __init__(self, sock):
        
        try:
            self.establishconnection(sock)
            game_thread = threading.Thread(target=self.create)
            game_thread.start()
        except Exception as e:
            print e.message

    
    def create(self):
        
        try:
            t1 = threading.Thread(target=self.getcoordinates, args=[self.playerconn1, 1])  
            t2 = threading.Thread(target=self.getcoordinates, args=[self.playerconn2, 2])
            
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            
            self.game_running_flag = True
            
            self.playerconn1.send("attack") 
            self.playerconn2.send("wait")
            
            t1 = threading.Thread(target=self.attack, args=[self.playerconn1, 1]) 
            t2 = threading.Thread(target=self.attack, args=[self.playerconn2, 2])
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            
            print "FINISH!"
            
        except Exception as e:
            print e.message


# Server runs continuously to serve multi-game functionality.
try:
    port = 5250
except:
    print "Please enter valid port number."
    sys.exit()
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates a server which listens to port 5250
    sock.bind(('0.0.0.0', port))
    sock.listen(8)
    print "server started.."
    while True:
        g = Playground(sock)
except Exception as e:
    print "Server cannot be started, specified port may already in use."
    print e.message
finally:
    print "server stopped."