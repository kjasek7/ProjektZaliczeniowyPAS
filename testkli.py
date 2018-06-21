import socket


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
    message += '\0'
    data = message.encode('utf-8')
    socket.sendall(data)


PORT = 8888

if __name__ == "__main__":

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(('127.0.0.1', PORT))
    print('Connected to {}:{}'.format('127.0.0.1', PORT))

    #handle_input(socket)
    rest = bytes()
    message = 'HELO'
    message2 = 'OK'
    if message == "QUIT":
        socket.shutdown(socket.SHUT_RDWR)
        socket.close()
    try:
        send_message(socket, message)
        send_message(socket, message2)
        (messages, rest) = receive_message(socket, rest)
        for mess in messages:
            print(mess)
    except ConnectionError:
        print('Polaczenie z serwerem zostalo zamkniete')
        socket.close()
