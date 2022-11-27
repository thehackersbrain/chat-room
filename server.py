#!/usr/bin/env python3

import socket
import threading

from rich import print

client_sockets = []
client_names = []


def chatServer(host, port, bytesize, encoder):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sckt.bind((host, port))
    sckt.listen()
    print("Server is listening for incoming connections...")
    connection(sckt, bytesize, encoder)


def broadcast(message):
    for i in client_sockets:
        i.send(message)


def receive(conn, bytesize, encoder):
    while True:
        try:
            sno = client_sockets.index(conn)
            name = client_names[sno]

            message = conn.recv(bytesize).decode(encoder)
            broadcast("{} [[bold green]{}[/]]".format(message, name).encode(encoder))
        except:
            sno = client_sockets.index(conn)
            name = client_names[sno]
            client_names.remove(name)
            client_sockets.remove(conn)

            message = "[i][red]{} has left the chat...[/][/]".format(name).encode(
                encoder
            )
            broadcast(message)

            conn.close()
            break


def connection(sckt, bytesize, encoder):
    while True:
        conn, addr = sckt.accept()
        name = conn.recv(bytesize).decode(encoder)
        print("[+] Name: {} Host: {} Port: {}".format(name, addr[0], addr[1]))
        broadcast(
            "[i][green]{} has joined the server[/][/]".format(name).encode(encoder)
        )

        client_sockets.append(conn)
        client_names.append(name)

        conn.send(
            "[u][cyan]Hey [bold][green]{}[/][/], Welcome to the Chat Room![/][/]".format(
                name.capitalize()
            ).encode(
                encoder
            )
        )
        receive_thread = threading.Thread(
            target=receive,
            args=(
                conn,
                bytesize,
                encoder,
            ),
        )
        receive_thread.start()


def main():
    host = socket.gethostbyname(socket.gethostname())
    port = 8000
    encoder = "utf-8"
    bytesize = 1024

    chatServer(host, port, bytesize, encoder)


if __name__ == "__main__":
    main()
