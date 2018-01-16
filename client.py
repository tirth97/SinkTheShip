import socket
import sys

def Main():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5002

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    while True:

        message = input("Write to server:- ")
        soc.sendall(message.encode("utf8"))
        if soc.recv(5120).decode("utf8") == "-":
            pass        # null operation

    soc.send(b'!q')

if __name__ == "__main__":
    Main()