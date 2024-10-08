import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None


choice = input("Do you want to (1)Host or (2)Connect: ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind (("192.168.7.11", 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect (("192.168.7.11", 9999))
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
else:
    exit()

def sending_messages(c):
    while True:
        message = input("")
        # c.send(message.encode())
        c.send(rsa.encrypt(message.encode(), public_partner))
        print ("You: " + message)

def receiving_messages(c):
    while True:
        # print("Partner: " + c.recv(1024).decode())
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()

        