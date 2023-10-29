import socket
import threading
import time
import os
from ip_and_name_finder import ip_and_machine_name_finder
from Diffie_Hellman_Calculation import generate_random_32_digits, SecretNumber, pow_mod, check_32_digit_number
from DecrtypthEncrypth import decryption, encryption


class MexBroadcastClass:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    # This function broadcast the message that start the conversation: it stops when the same message arrives from someone else
    def mex_broadcast(self, UDP_PORT_RECEIVER):

        while self._running:
            print(f'Sending broadcast packets...')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((own_ip_address, 0))
            sock.sendto(msg_standard.encode(), ("255.255.255.255", UDP_PORT_RECEIVER))
            time.sleep(1)
        sock.close()


class MexReceiverClass:
    def __init__(self):
        self._running = True
        self.cipher = False

    def terminate(self):
        self._running = False

    def cypher(self):
        self.cipher = True

    # This function listen for the incoming messages
    def mex_receiver(self, BLOKING):

        UDP_IP_RECEIVER = ""
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

        print("binding the listener to the port " + str(Udp_Port_Listener))
        sock.bind((UDP_IP_RECEIVER, Udp_Port_Listener))
        sock.setblocking(BLOKING)

        while self._running:

            try:
                data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                data = data.decode()

                if addr[0] != own_ip_address:
                    if self.cipher:  # this block is true only after the key exchange, when the encryption is enstablished
                        data = decryption(data, Key)
                        print(data.decode())
                    messaggi.append((data, addr[0]))

            except Exception as e:
                print(e)
                pass
            time.sleep(0.1)

        # we use this to not bug when switching port
        sock.close()
        print("connection closed")


# This function sends the messages
def mex_sender(MESSAGE, UDP_IP_SENDER, UDP_PORT_SENDER):
    MESSAGE = str(MESSAGE).encode()
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP_SENDER, UDP_PORT_SENDER))


# --------------------------------------------------------------------------------------------------------------------------------------------
# Script Start

# Set the variables
messaggi = []
msg_standard = "IWTC"
Udp_Port_Listener = 5005
Udp_Port_Sender = 5006
hostname, own_ip_address = ip_and_machine_name_finder()

# printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {own_ip_address}")

# Starting the broadcast thread
Thread_Br = MexBroadcastClass()
mex_br_d = threading.Thread(target=Thread_Br.mex_broadcast, args=(Udp_Port_Listener,))
mex_br_d.daemon = True
mex_br_d.start()

# Starting the listener thread
Thread_Rcv = MexReceiverClass()
mex_rcv_d = threading.Thread(target=Thread_Rcv.mex_receiver, args=(True,))
mex_rcv_d.daemon = True
mex_rcv_d.start()


while mex_br_d.is_alive():
    time.sleep(0.1)

    # this while wait until a message arrives
    if len(messaggi) != 0:
        # we wait some time for our broadcast thread to send the message
        message_received, ip_address_of_the_other = messaggi[0]
        messaggi.pop(0)
        # if it is the message that want to start the conversation it stops the broadcasting
        if message_received == msg_standard:
            time.sleep(2)
            Thread_Br.terminate()
            mex_br_d.join(3)


# Now we want to do the diffie-hellman key exchange. keep in mind that this is vulnerable to the MITM
# (I could've smushed this code but i want to make the code the most clean possible)
#  if your own ip is the lower one you generate a random 32 digits number

g = 2

# We empty the queue
time.sleep(2)
messaggi.clear()  # FIX THIS
time.sleep(2)

if own_ip_address < ip_address_of_the_other:
    # h is always a big number in order to prevent brute-force attacks
    h = generate_random_32_digits()

    # We then share our result with the other person
    mex_sender(h, ip_address_of_the_other, Udp_Port_Listener)

else:
    # if we not share the number we wait for it and also check if is valid
    # We wait until a mex arrives
    while len(messaggi) == 0:
        time.sleep(1)

    if check_32_digit_number(messaggi[-1][-2]):
        h = messaggi[-1][-2]
    else:
        raise Exception("Error. Expected a different message")

# I choose a random number < h
a = SecretNumber(int(h))

# calculating the remainder
A = pow_mod(g, a, int(h))

print(f"\n\nIL NUMERO DECISO E':{h}\nIL NUMERO SEGRETO E':{a}\nIL CALCOLO E':{A}\n")

# NOW WE SEND THE RESULT OF THE OPERATION AND WE WAIT FOR THE RESPONSE
time.sleep(2)
mex_sender(A, ip_address_of_the_other, Udp_Port_Listener)
time.sleep(2)

# WE FIND THE NUMBER WE WILL USE TO COMUNICATE DOING THIS LAST POW
Key = str(pow_mod(int(messaggi[-1][-2]), a, int(h)))

# We add a padding in order to always have a 32 digit Key
Key = Key.ljust(32, "0")
print(f"THE KEY IS {Key}")
Thread_Rcv.cypher()

input("Press any button to start messaging with encryption END-TO-END with the other person\n")

# we clear the screen
os.system('cls' if os.name == 'nt' else 'clear')


# Now we can communicate with the conversation being encrypted
print("type 'quit' to exit the communication.")
while True:
    MESSAGE_TO_SEND = input("")

    if MESSAGE_TO_SEND == "quit":
        print("exiting...")
        exit(1)
    
    MESSAGE_TO_SEND = encryption(MESSAGE_TO_SEND, Key)
    mex_sender(MESSAGE_TO_SEND, ip_address_of_the_other, Udp_Port_Listener)
    print("message sended!")
