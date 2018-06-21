# Server.py
import queue
import socket
import threading

PORT = 8888
MESSAGE_SIZER = 12
clients = {}
object_lock = threading.Lock()


def send_message(socket, question):
    # dodaje znak konca wiadomosci i koduje ja w formacie UTF8
    question += '\0'
    data = question.encode('utf-8') #pierwsza wersja kodowanie w utf8, jak starczy czasu to zamienimy na szyfrowanie
    socket.sendall(data)

def receive_message(socket, data=bytes()):
    #Odbiera wiadomosc
    messages = []
    while not messages:
        received = socket.recv(MESSAGE_SIZER).strip()
        if not received:
            raise ConnectionError()
            data = data + received
    data.decode('utf-8')
    #messages = [message.decode('utf-8') for message in messages]
    return data

        #data = data + received
        #(messages, rest) = data#= parse_data(data)
   # messages = [message.decode('utf-8') for message in messages] #zdekodowanie wiadomosci
    #return (messages, data)


# WATKI OBSLUGI KLIENTA
def client_receive(socket, addr):
    """ Jej zadaniem jest obsluga odbierania wiadomosci od klienta"""
    data = bytes()
    while True:  # funkcja dziala w petli nieskaczonej bo nie wiadomo ile wiadomosci bedzie przesylal klient
        try:
            #(messages, data) = receive_message(socket, data)
            messages = receive_message(socket, data)
            """oczekiwanie na wiadomosc, pobranie i zdekodowanie
            do funkcji receive_message przekazujemy gniazdo klienta oraz zmienna data, poczatkowo pusta"""
        except (EOFError, ConnectionError):  # komunikacja moze sie zakonczyc wyjatkiem
            client_disconnect(socket, addr)
            break

        for message in messages:  # kazda wiadomosc wyswietlana jest na konsoli serwera
            print('{}: {}'.format(addr, message)) #wyswietla wartosc odebranych wiadomosci

            # Obsluzenie pierwszej wiadomosci. Dodanie ID.
            with object_lock:
                clientId = clients[socket.fileno()]['id']
                if clientId is None:  # sprawdzamy pierwsza wiadomosc od klienta porownujac jego nazwe z wartoscia none. Jesli name jest None to oznacza ze jeszcze zadna wiadomosc nie zostala przeslana
                    clients[socket.fileno()]['id'] = message  # wartosci pierwszej wiadomosci zapisujemy w polu name w slowniku skojarzonym z klientem
                else:
                    # jestli wartosc client name nie jest none to znaczy ze wczesniej wyslano wiadomosc powitalna ustawiajaca id klienta
                    # i kolejna wiadomosc powinna rozpoaczac 'gre'
                    clients[socket.fileno()]['queue'].put(message)

                    """ Add message to each connected client’s send queue 
                    message = '{}: {}'.format(clientId, message)  # dodawana jest nazwa nadawcy do wiadomosci
                    # ponizej przygotowana wiadomosc mozna rozeslac czyli dodac do kolejki wiad skojarzonej z kazdym z klientow zapisanych we wspoldzielonej zmiennej client
                    for i in clients:
                        clients[i]['queue'].put(message)
                    """

def client_send(socket, que, addr):
    """Monitoruje zawartosc kolejki klienta i gdy pojawi sie w niej nowa wiadomosc to odpowiada mu"""
    while True:  # ta funkcja rowniez dziala w petli nieskonczonej
        message = que.get()  # wywolanie metody get na obiekcie kolejki klienta
        if message == None:
            break
        try:
            question = "Kim jest jelen?"
            #message odebrane opcje if - moze dac odwolanie do funkcji?
            send_message(socket, question)
        except (ConnectionError, BrokenPipeError):
            client_disconnect(socket, addr)
            break

def client_disconnect(socket, addr):
    """ Konczy polaczenie z klientem i usuwa go ze zmiennej clients abysmy nie probowali wysylac wiadomosci do kogos kogo juz nie ma.
    """
    fd = socket.fileno()
    with object_lock:
        que = clients.get(fd, None)['queue']
        if que:
            que.put(None)
            del clients[fd]
        addr = socket.getpeername()
        print('Klient {} zostal rozlaczony'.format(addr))
        socket.close()



if __name__ == "__main__":

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # serwer tworzy gniazdo tcp i nasluchuje na polaczenie
    socket.bind(("127.0.0.1", PORT))
    socket.listen(5)

    adres = socket.getsockname()
    print('Trwa nasluchiwanie na: {}'.format(adres))

    while True:
        client, addr = socket.accept()  # odbiera i akceptuje polaczenie
        print('Polaczono z: {}'.format(addr))  # wyswietlenei info o polaczeniu

        que = queue.Queue()  # tworzy obiekt kolejki FIFO i zapisuje w zmiennej q. Kolejka ta jest 'thread safe'
        # Zapisany w zmiennej que obiekt Queue bedzie sluzyl jako bufor otrzymywanych wiadomosci od klientow.
        with object_lock:  # w zmiennej clients zapisywany jest slownik opisujacy nowego klienta.
            clients[socket.fileno()] = {
                'id': None,
                'queue': que
            }
            """ object_lock to wspoldzielona zmienna w ktorej jest obiekt object_lock z modulu threading. Słuzy do tego co kolejka Queue
            W sekcji tej modyfikujemy zmienna clients, ktora jest slownikiem a slownik nie jest 'thread safe'
            dlatego korzystamy z niezaleznego obiektu Lock. Jego dzialanie polega ze jezeli watek wejdzie do sekcji object_lock:
            co oznacza, że zablokuje zmienna object_lock, przez co zaden inny watek do niej nie wejdzie."""

        # nastepnie tworzone sa watki
        receive_msg_thread = threading.Thread(target=client_receive, args=[client, addr], daemon=True)  # args - lista parametrow przekazanych do funkcji z target. Deamon - oznacza ze program moze zakonczyc dzialanie gdy watek dziala w tle
        send_msg_thread = threading.Thread(target=client_send, args=[client, que, addr], daemon=True)

        # uruchomienie obu watkow
        receive_msg_thread.start()
        send_msg_thread.start()

    socket.close()