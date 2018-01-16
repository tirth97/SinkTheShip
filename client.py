import socket


def Main():
    host = "127.0.0.1"
    port = 5002

    mySocket = socket.socket()
    mySocket.connect((host, port))

    print("Connected with:- " + str(host))

    message = input(" -> ")

    while True:

        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print('Received from server: ' + data)

        message = input(" -> ")

    mySocket.close()


if __name__ == '__main__':
    Main()