import queue
import socket
import threading
import random
import pickle


clients = {}
object_lock = threading.Lock()
losujPytanie = []
def pytania():
    pytanie = []
    with open("Pytania.txt", "r") as file:
        for line in file:
            pytanie.append(line.split(":"))
    losujPytanie = pytanie[random.randint(0,len(pytanie)-1)]
    return losujPytanie

def parser(data):
    parts = data.split(b'\0')
    msgs = parts[:-1]
    return (msgs)


def receive_message(socket):
    messages = []
    data = bytes()
    while not messages:
        received = socket.recv(2048)
        if not received:
            raise ConnectionError()
        data = data + received
        (messages) = parser(data)
    messages = [message.decode('utf-8') for message in messages]
    return (messages)


def send_message(socket, question):
    # dodaje znak konca wiadomosci i koduje ja w formacie UTF8
    question += '\0'
    data = question.encode('utf-8')
    print('wysylam', data)
    socket.sendall(data)

    """
    data = question #pierwsza wersja kodowanie w utf8, jak starczy czasu to zamienimy na szyfrowanie
    if type(data)==type(str()):
        data = question.encode('utf-8')
        socket.sendall(data)
    else:
        dana = pickle.dumps(data)
        socket.sendall(dana)
    """
def client_receive(socket, addr):

    while True:
        try:
            (messages) = receive_message(socket)
        except (EOFError, ConnectionError):
            client_disconnect(socket, addr)
            break
        for message in messages:
            print('{}: {}'.format(addr, message))

            with object_lock:
                client_name = clients[socket.fileno()]['id']
                if client_name is None:
                    clients[socket.fileno()]['id'] = message
                else:
                    for i in clients:
                        clients[i]['queue'].put(message)
                        print('m',message)


def client_send(socket, client_queue, addr):
    while True:
        message = client_queue.get()
        if message == None: break
        try:
            if (message == 'PYTANIE'):
                losujPytanie = pytania()
                print("all", losujPytanie)
                msg1 = losujPytanie[0]
                msg2 = losujPytanie[1]
                msg3 = losujPytanie[2]
                msg4 = losujPytanie[3]
                msg5 = losujPytanie[4]
                msg6 = losujPytanie[5]
                print("pytanie", msg1)
                print("a", msg2)
                print("b", msg3)
                print("c", msg4)
                print("d", msg5)
                print("odp", msg6)
                send_message(socket, msg1) #pytanie
                send_message(socket, msg2) #a
                send_message(socket, msg3) #b
                send_message(socket, msg4) #c
                send_message(socket, msg5) #d
                send_message(socket, msg6) #poprawna odp
                print('wyslano')
                break
            #message = "wal sie"
            #send_message(socket, message)
        except (ConnectionError, BrokenPipeError):
            client_disconnect(socket, addr)
            break


def client_disconnect(socket, addr):
    fd = socket.fileno()
    with object_lock:
        q = clients.get(fd, None)['queue']
        if q:
            q.put(None)
            del clients[fd]

        addr = socket.getpeername()
        print('Klient {} zostal rozlaczony'.format(addr))
        socket.close()


if __name__ == '__main__':

    port = 8888

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(("127.0.0.1", port))
    socket.listen(5)

    adres = socket.getsockname()
    print('Trwa nasluchiwanie na: {}'.format(adres))

    while True:
        client, addr = socket.accept()
        print('Polaczono z: {}'.format(addr))
        que = queue.Queue()
        with object_lock:
            clients[client.fileno()] = {
                'id': None,
                'queue': que
            }

        # nastepnie tworzone sa watki
        receive_msg_thread = threading.Thread(target=client_receive, args=[client, addr], daemon=True)  # args - lista parametrow przekazanych do funkcji z target. Deamon - oznacza ze program moze zakonczyc dzialanie gdy watek dziala w tle
        send_msg_thread = threading.Thread(target=client_send, args=[client, que, addr], daemon=True)

        # uruchomienie obu watkow
        receive_msg_thread.start()
        send_msg_thread.start()

    socket.close()

