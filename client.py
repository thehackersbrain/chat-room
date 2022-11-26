#!/usr/bin/env python3

import socket
import threading
from sys import argv, exit

from rich import print
from rich.console import Console

console = Console()


def chatClient(host, port, bytesize, encoder, name):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect((host, port))
    sckt.send(name.encode(encoder))
    receive_thread = threading.Thread(
        target=receive,
        args=(
            sckt,
            bytesize,
            encoder,
        ),
    )
    send_thread = threading.Thread(
        target=send_msg,
        args=(
            sckt,
            encoder,
        ),
    )
    receive_thread.start()
    send_thread.start()


def send_msg(cSckt, encoder):
    while True:
        # message = input("")
        message = console.input("")
        cSckt.send(message.encode(encoder))


def receive(cSckt, bytesize, encoder):
    while True:
        try:
            message = cSckt.recv(bytesize).decode(encoder)
            if "Welcome to the Chat Room!" in message:
                console.print("\n{}\n".format(message), justify="center")
            elif "has joined the server" in message:
                console.log(message)
            elif "has left the chat" in message:
                console.log(message)
            else:
                console.log(message, justify="right")
        except:
            print("An error occured...")
            cSckt.close()
            break


def main():
    if len(argv) == 4:
        host = argv[1]
        port = int(argv[2])
        name = argv[3]
        bytesize = 1024
        encoder = "utf-8"
        chatClient(host, port, bytesize, encoder, name)
    else:
        exit(1)


if __name__ == "__main__":
    main()
