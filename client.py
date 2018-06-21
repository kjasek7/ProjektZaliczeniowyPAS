import socket


def fill_msg_left(n, width, pad="0"):
    return ((pad * width) + str(n))[-width:]

def prepare_message(msg):
    """Przygotowanie wiadomosci(napis) przed wysylka"""
    data2 = msg.rjust(12, '0')
    data = fill_msg_left(msg,12)
    return data

def separate_data_received(data):
    # Rozdziela wiadomosci po znaku \0
    parts_data = data.split(b'\0')
    message = parts_data[:-1]
    next_message = parts_data[-1]
    return (message, next_message) #zwraca wiadomosc oraz czesc nastepnej

def receive_message(socket, nodecoded_data=bytes()): #zamiast funkcji recv
    messages = []
    while not messages: #pobiera i dekoduje wiadomosci
        received_data = socket.recv(4096)
        if not received_data:
            raise ConnectionError() #jezeli nie ma odebranych danych to polaczenie zostalo przerwane
        nodecoded_data = nodecoded_data + received_data
        (messages, other_data) = separate_data_received(nodecoded_data)
    messages = [message.decode('utf-8') for message in messages] #dekoduje wiadomosci
    return (messages, other_data) #messages- dane zdekodowane , other_data- dane ktorych sie nie udalo zdekodowac

def send_message(socket, message):
    data = prepare_message(message)# dodaje znak konca wiadomosci i koduje ja w formacie UTF8
    data = data.encode('utf-8')
    print(data)
    socket.sendall(data)

def handle_input(socket):
    """ Prompt user for message and send it to server """
    while True:
        message = 'HELO'
        if message == 'QUIT':
            socket.shutdown(socket.SHUT_RDWR)
            socket.close()
            break
        try:
            send_message(socket, message)  # Blocks until

        except (BrokenPipeError, ConnectionError):
            break


PORT = 8888


if __name__ == "__main__":

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(('127.0.0.1', PORT))
    print('Connected to {}:{}'.format('127.0.0.1', PORT))

    #handle_input(socket)
    rest = bytes()
    while True:
        message = "HELO"
        message2 = 'OK'
        if message == "QUIT":
            socket.shutdown(socket.SHUT_RDWR)
            socket.close()
        try:
            send_message(socket, message)
            print('wyslano')
            send_message(socket, message2)
            print('wyslano2')
            (messages, rest) = receive_message(socket, rest)
            print('odbieranie')
            for mess in messages:
                print(mess)
        except ConnectionError:
            print('Polaczenie z serwerem zostalo zamkniete')
            socket.close()

    """"
    while True:
        message = "HELO"
        if message == "QUIT":
            socket.shutdown(socket.SHUT_RDWR)
            socket.close()
            break
        try:
            send_message(socket, message)
            (messages, rest) = receive_message(socket, rest)
            for mess in messages:
                print(mess)
        except ConnectionError:
            print('Polaczenie z serwerem zostalo zamkniete')
            socket.close()
            break
    """
    socket.close()