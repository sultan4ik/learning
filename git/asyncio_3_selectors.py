import socket
import selectors
# selectors
selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = 'Hello '.encode() + request
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    # событийный цикл
    while True:

        events = selector.select()  # (key, events)
        # SelectorKey(fileobj=<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM,
        # proto=0, laddr=('127.0.0.1', 5000)>, fd=4, events=1, data=<function accept_connection at 0x105c1c280>), 1)

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
