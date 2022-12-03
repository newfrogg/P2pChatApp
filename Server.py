import sys, socket
from threading import Thread
import json

HOST = "localhost"
SERVER_PORT = 2202


active_clients = {}
db = {}

with open("db.json", "r") as file:
    db = json.load(file)


class Server:	
	
	LOGIN = "LOGIN"
	GETPEER = "GETPEER"
	LOGOUT = "LOGOUT"

	LOGIN_SUCCESS = 0
	USER_PASS_INVALID = 1
	NOT_ONLINE = 2
	GPEER_SUCCESS = 3
	OK = 4

	def __init__(self, active_clients, db):
		self.active_clients = active_clients
		self.db = db

	def main(self):
		Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		Server_Socket.bind((HOST, SERVER_PORT))
		Server_Socket.listen(5)        

		# Receive client info (address,port) through RTSP/TCP session
		while True:
			client = {}
			client['Socket'] = Server_Socket.accept()
			#print(f"connect from {client['Socket'][1]}")
			Thread(target=self.recvRequest, args=(client, )).start()
			

	def recvRequest(self, client):
		"""Receive RTSP request from the client."""
		connSocket = client['Socket'][0]
		while True:            
			try:
				data = connSocket.recv(256)
				if data:
					print("Data received:\n" + data.decode("utf-8"))
					self.processRequest(data.decode("utf-8"), client)
			except:
				print(f"{client['username']} has logged out")
				break

	def processRequest(self, data, client):
		"""Process RTSP request sent from the client."""
		# Get the request type
		request = data.split('\n')
		requestType = request[0]
		
		# Process LOGIN request
		if requestType == self.LOGIN:
			info = request[1].split("-")
			username = info[0]
			password = info[1]
			if (self.validate_login(username, password) == 1):
				client['username'] = username
				
				#get client_listen_port
				client['listen_socket'] = info[2]
				
				#get client_friend from database
				client["friend"] = self.db[username]['friends']
				self.replyRequest(self.LOGIN_SUCCESS, client)
				self.active_clients[username] = client
			else:
				self.replyRequest(self.USER_PASS_INVALID, client)
		# Process GETPEER request
		elif requestType == self.GETPEER:
			username = request[1]
			try:
				peer = active_clients[username]['listen_socket']
				client['peer'] = peer
				self.replyRequest(self.GPEER_SUCCESS, client)
			except:
				self.replyRequest(self.NOT_ONLINE, client)
		# Process LOGOUT request
		elif requestType == self.LOGOUT:
			self.active_clients.pop(client['username'])
			self.replyRequest(self.OK, client)
			client['Socket'][0].close()
			

	def replyRequest(self, code, client):
		"""Send reply to the client."""
		if code == self.LOGIN_SUCCESS:
			friend = " ".join(client['friend'])
			reply = f'LOGIN_SUCCESS\n{friend}'  
			connSocket = client['Socket'][0]
			connSocket.send(reply.encode())
		
		elif code == self.USER_PASS_INVALID:
			reply = f'USER_PASS_INVALID\n'
			connSocket = client['Socket'][0]
			connSocket.send(reply.encode())

		elif code == self.NOT_ONLINE:
			reply = f'NOT_ONLINE\n'
			connSocket = client['Socket'][0]
			connSocket.send(reply.encode())
		
		elif code == self.GPEER_SUCCESS:
			peer = client["peer"]
			reply = f'GPEER_SUCCESS\n{peer}'
			connSocket = client['Socket'][0]
			connSocket.send(reply.encode())
		
		elif code == self.OK :
			reply = f"OK\n"
			connSocket = client['Socket'][0]
			connSocket.send(reply.encode())
		
	
	def validate_login(self, username, password):
		try:
			if self.db[username]['password'] == password:
				return 1
			else: 
				return -1
		except:
			return -1

if __name__ == "__main__":
	(Server(active_clients, db)).main()


