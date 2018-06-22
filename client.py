import socket

PORT = 8888

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self,add = '127.0.0.1',port = PORT):
        while True:
            try:
                self.socket.connect((add, port))
                print('Connected to {}:{}'.format(add, port))
                return True
            except:
                print("Connected filed")
                return False

    def send_message(self, message):
        try:
            message += '\0'
            data = message.encode('utf-8')
            self.socket.sendall(data)
        except:
            return False

    def receive_message(self, nodecoded_data=bytes()):  # zamiast funkcji recv
        messages = []
        while not messages:  # pobiera i dekoduje wiadomosci
            received_data = self.socket.recv(4096)
            print('receive',received_data)
            if not received_data:
                raise ConnectionError()  # jezeli nie ma odebranych danych to polaczenie zostalo przerwane
            nodecoded_data = nodecoded_data + received_data
            #(messages, other_data) = self.separate_data_received(nodecoded_data)
            parts_data = nodecoded_data.split(b'\0')
            messages = parts_data[:-1]
        messages = [message.decode('utf-8') for message in messages]  # dekoduje wiadomosci
        print('mes',messages)
        for msg in messages:
            print(msg)
        #print('ot',other_data)
        #return (messages, other_data)  # messages- dane zdekodowane , other_data- dane ktorych sie nie udalo zdekodowac
        return messages

    def separate_data_received(data):
        # Rozdziela wiadomosci po znaku \0
        parts_data = data.split(b'\0')
        message = parts_data[:-1]
        #next_message = parts_data[-1]
        #return (message, next_message)  # zwraca wiadomosc oraz czesc nastepnej
        return message

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            print('Polaczenie z serwerem zostalo zamkniete')
        except:
            print ("Blad przy zamykaniu")

