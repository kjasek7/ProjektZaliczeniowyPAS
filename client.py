import socket

PORT = 8888

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self,add,port):
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
            data = self.__prepare_message(message)  # dodaje znak konca wiadomosci i koduje ja w formacie UTF8
            data = data.encode('utf-8')
            print(data)
            self.socket.sendall(data)
        except:
            return False

    def __prepare_message(self, msg):
        """Przygotowanie wiadomosci(napis) przed wysylka"""
        #data2 = msg.rjust(12, '0')
        data = self.__fill_msg_left(msg, 12)
        return data

    def __fill_msg_left(self, n, width, pad="0"):
        return ((pad * width) + str(n))[-width:]

    def receive_message(self, nodecoded_data=bytes()):  # zamiast funkcji recv
        try:
            messages = []
            while not messages:  # pobiera i dekoduje wiadomosci
                received_data = self.socket.recv(4096)
                if not received_data:
                    raise ConnectionError()  # jezeli nie ma odebranych danych to polaczenie zostalo przerwane
                nodecoded_data = nodecoded_data + received_data
                (messages, other_data) = self.__separate_data_received(nodecoded_data)
            messages = [message.decode('utf-8') for message in messages]  # dekoduje wiadomosci
            return (messages, other_data)  # messages- dane zdekodowane , other_data- dane ktorych sie nie udalo zdekodowac
        except:
            return False

    def __separate_data_received(data):
        # Rozdziela wiadomosci po znaku \0
        parts_data = data.split(b'\0')
        message = parts_data[:-1]
        next_message = parts_data[-1]
        return (message, next_message)  # zwraca wiadomosc oraz czesc nastepnej

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            print('Polaczenie z serwerem zostalo zamkniete')
        except:
            print ("Blad przy zamykaniu")



# if __name__ == "__main__":
#
#     client = Client()
#     client.connect('127.0.0.1',PORT)
#     #client.send_message("Hej")
#     #client.close()

