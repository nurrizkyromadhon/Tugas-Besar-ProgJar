import socket
import tqdm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

try:
    file_name = client.recv(1024).decode()
    file_size = client.recv(1024).decode()
except UnicodeDecodeError:
    file_name = client.recv(1024).decode('utf-16')
    file_size = client.recv(1024).decode('utf-16')

# file_name = client.recv(1024).decode("utf-8", "ignore")
print(file_name)
# file_size = client.recv(1024).decode("utf-8", "ignore")
print(file_size)

file = open(file_name, "wb")

file_bytes = b""

done = False

progress = tqdm.tqdm(unit="B", unit_scale=True,
                     unit_divisor=1000, total=int(file_size))

while not done:
    data = client.recv(1024)
    if file_bytes[-5:] == b"<END>":
        done = True
    else:
        file_bytes += data

    progress.update(1024)

file.write(file_bytes)

file.close()
server.close()
client.close()
