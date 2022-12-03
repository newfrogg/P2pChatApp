import socket
from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

import os

host = socket.gethostbyname("localhost")
server_port = 2202

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:
	LOGIN = 0
	GETPEER = 1
	LOGOUT = 2
	
	# Initiation..
	def __init__(self, Window, serveraddr, serverport, serversocket):
		self.Window = Window
		self.Window.withdraw()
		self.isLogin = False
		self.Window.protocol("WM_DELETE_WINDOW", self.handlerExit)
		
		self.serversocket = serversocket
		self.serverAddr = serveraddr
		self.serverPort = int(serverport)
		self.mysocket = mysocket

		self.connect_To_Server()
		self.LoginGUI()
		self.friend_list = []
		self.connect_to_friend = {}
		self.connect_from_friend = []
		
	# LOGIN GUI FOR CLIENT	
	def LoginGUI(self):
		"""Build GUI."""

		self.login = Toplevel()
		self.login.title("Login")
		self.login.resizable(0,0)
		self.login.configure(width=300, height=200)
		# set the title
		
		# create a Label
		self.pls = Label(self.login,
						text="Login to continue",
						justify=CENTER,
						font="Helvetica 11")

		self.pls.place(relheight=0.15,
					relx=0.2,
					rely=0.07)

		# create a Label
		self.labelName = Label(self.login,
							text="Name: ",
							font="Helvetica 12")

		self.labelName.place(relheight=0.2,
							relx=0.1,
							rely=0.2)

		# create a entry box for
		# tyoing the message
		self.entryName = Entry(self.login,
							font="Helvetica 11")

		self.entryName.focus_set()

		self.entryName.place(relwidth=0.4,
							relheight=0.12,
							relx=0.35,
							rely=0.2)
		
		
		self.labelPass = Label(self.login,
							text="Password: ",
							font="Helvetica 11")

		self.labelPass.place(relheight=0.2,
							relx=0.1,
							rely=0.35)

		# create a entry box for
		# tyoing the message
		self.entryPass = Entry(self.login,
							font="Helvetica 14", show="*")

		self.entryPass.place(relwidth=0.4,
							relheight=0.12,
							relx=0.35,
							rely=0.35)

		self.go = Button(self.login,
						text="Login",
						font="Helvetica 14 bold",
						command=self.Login)

		self.go.place(relx=0.7,
					rely=0.55)

		# Register
		self.register = Button(self.login, text="Register",font="Helvetica 14 bold", command=self.Register)
		self.register.place(relx = 0.2, rely=0.55)

	def CHATGUI(self, username):
		self.status =""

		self.login.destroy()
		self.name = username
		self.frames = {}
		self.textCons = {}
		self.scrollbar = {}
		self.connectButton = {}

		self.menu = Menu(self.Window)
		self.Window.config(menu=self.menu)
		self.menuFriend = Menu(self.menu)
		self.menu.add_cascade(label="Friends", menu=self.menuFriend)

		def reset_tabstop(event):
			event.widget.configure(tabs=(event.width-8, "right"))
		#Create Frame for each friend
		for friend in self.friend_list:
			self.frames[friend] = Frame(self.Window, width=470, height=550, bg="#17202A")
			self.textCons[friend] = Text(self.frames[friend],
							width=20,
							height=2,
							bg="#17202A",
							fg="#EAECEE",
							font="Helvetica 14",
							padx=5,
							pady=7)

			self.textCons[friend].place(relheight=0.745,
							relwidth=1,
							rely=0.08)

			self.textCons[friend].config(cursor="arrow")

			self.textCons[friend].bind("<Configure>",reset_tabstop)
			# create a scroll bar
			self.scrollbar[friend] = Scrollbar(self.textCons[friend])

			# place the scroll bar
			# into the gui window
			self.scrollbar[friend].place(relheight=1,
						relx=0.974)

			self.scrollbar[friend].config(command=self.textCons[friend].yview)

			self.textCons[friend].config(state=DISABLED)


			# Add friend to menu
			self.menuFriend.add_command(label=friend,command=lambda x=friend :self.layout(x))
			self.menuFriend.add_separator()



		# to show chat window
		self.Window.deiconify()
		self.Window.geometry("470x550")
		self.Window.title("CHATROOM")
		self.Window.resizable(width=False,
							height=False)
		self.Window.configure(width=470,
							height=550,
							bg="#17202A")
		self.labelHead = Label(self.Window,
							bg="#17202A",
							fg="#EAECEE",
							text=f'\t\t\t\tYou: {self.name}',
							font="Helvetica 13 bold",
							pady=15)

		self.labelHead.place(relwidth=1)
		
		

		self.line = Label(self.Window,
						width=450,
						bg="#ABB2B9")

		self.line.place(relwidth=1,
						rely=0.08,
						relheight=0.012)

		self.labelBottom = Label(self.Window,
								bg="#ABB2B9",
								height=80)

		self.labelBottom.place(relwidth=1,
							rely=0.825)

		self.entryMsg = Entry(self.labelBottom,
							bg="#2C3E50",
							fg="#EAECEE",
							font="Helvetica 13")

		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth=0.50,
							relheight=0.06,
							rely=0.008,
							relx=0.011)

		self.entryMsg.focus()

		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text="Send",
								font="Helvetica 10 bold",
								width=10,
								bg="#ABB2B9",
								command=lambda :self.sendMsg(self.status))

		self.buttonMsg.place(relx=0.77,
							rely=0.008,
							relheight=0.06,
							relwidth=0.22)


		# Choose File


		self.chooseFile = Button(self.labelBottom,
								text="ChooseFile",
								font="Helvetica 10 bold",
								width=10,
								bg="#ABB2B9",
								command = lambda: self.sendFile(self.status))

		self.chooseFile.place(relx=0.55,
							 rely=0.008,
							 relheight=0.06,
							 relwidth=0.22)

	def sendFile(self, friend):
		file = filedialog.askopenfilename(title="Choose a file",initialdir= os.path.dirname(__file__))
		filename = str(file.split('/')[-1])

		with open(file, 'r') as f:
			file_content = str(f.read())
			f.close()
		try: 
			content = filename
			msg = f"{self.name}\n{filename}\n{file_content}"
			print(file_content)
			self.connect_to_friend[friend].send(msg.encode())
			self.textCons[friend].config(state = NORMAL)
			self.textCons[friend].insert(END, f' \t[[ NOTIFICATION ]] You has shared {filename} file.   \n\n')
			self.textCons[friend].config(state = DISABLED)
			self.entryMsg.delete(0, END)
		except:
			if friend in self.connect_to_friend:
				self.connect_to_friend.pop(friend)
			self.getPeer(friend)
			if friend in self.connect_to_friend:
				self.sendFile(friend)



	def layout(self, friend):
		self.hide_all_frame()
		self.frames[friend].pack(fill="both", expand=1)
		self.labelHead.config(text=f"{friend}\t\t\t\tYou: {self.name}")
		self.status = friend
	
	def hide_all_frame(self):
		for friend in self.friend_list:
			self.frames[friend].pack_forget()
		
	def connect_To_Server(self):
		"""Connect to the Server."""
		try:
			self.serversocket.connect((self.serverAddr, self.serverPort))
			self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			host = socket.gethostbyname(socket.gethostname())
			self.mysocket.bind((host, 0))
			self.mysocket.listen(100)
		except:
			pass

	def sendRequest(self, requestCode, data):
		"""Send request to the server."""
		if requestCode == self.LOGIN:
			request = "LOGIN" + "\n" + data
			self.serversocket.send(request.encode())
		elif requestCode == self.GETPEER:
			request = "GETPEER" + "\n" + data
			self.serversocket.send(request.encode())
		elif requestCode == self.LOGOUT:
			request = "LOGOUT" + "\n" + data
			self.serversocket.send(request.encode())

	def recvReply(self):
		"""Receive RTSP reply from the server."""
		response = self.serversocket.recv(1024).decode()
		return response.split("\n")
	
	def Login(self):
		username = self.entryName.get()
		password = self.entryPass.get()
		self.sendRequest(self.LOGIN, f'{username}-{password}-{self.mysocket.getsockname()}')
		response = self.recvReply()
		if response[0] == "USER_PASS_INVALID":
			messagebox.showerror(title="Warning", message="Username or Password invalid")
		else:
			print("Login success")
			self.friend_list = response[1].split(" ")
			self.isLogin = True
			self.CHATGUI(username)
			Thread(target=self.accept_connect_from_friend).start()
	
	def Register(self):
		messagebox.showwarning(title='Warning', message="Oops, this feature hasn't been released :))")

	def getPeer(self, username):
		self.sendRequest(self.GETPEER, f'{username}')
		response = self.recvReply()
		if response[0] == "NOT_ONLINE":
			messagebox.showerror(title="Message", message="Friend is not online")
		else:
			print("Get peer success")
			address = response[1][2:len(response[1]) - 1].split("', ")
			HOST = address[0]
			PORT = int(address[1])
			self.connect_to_friend[username] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connect_to_friend[username].connect((HOST, PORT))

	def sendMsg(self, friend):
		try:
			content = self.entryMsg.get()
			msg = f"{self.name}\n{content}"
			self.connect_to_friend[friend].send(msg.encode())
			self.textCons[friend].config(state = NORMAL)
			self.textCons[friend].insert(END, f' \t<You> : {content}    \n\n')
			self.textCons[friend].config(state = DISABLED)
			self.entryMsg.delete(0, END)
		except:
			if friend in self.connect_to_friend:
				self.connect_to_friend.pop(friend)
			self.getPeer(friend)
			if friend in self.connect_to_friend:
				self.sendMsg(friend)

	def accept_connect_from_friend(self):
		while self.isLogin == True:
			try:
				friend = self.mysocket.accept()
				print("Successfull")
				self.connect_from_friend.append(friend)
				Thread(target=self.RecvMsg, args=(friend, )).start()
			except:
				print("Close listen socket")

	def RecvMsg(self, friend):
		connSocket = friend[0]
		while self.isLogin == True:
			try:
				data = connSocket.recv(1024).decode("utf-8")
				if data and data != '~disconnect~':
					data = data.split("\n")
					name = data[0]
					msg = data[1]
					if len(data) > 2:
						filecontent = data[2]
						dst_dir = r'File/Download/' + msg
						with open(dst_dir, 'x') as f:
							f.write(filecontent)
							f.close()

					#display msg in textCons
					if msg:
						self.textCons[name].config(state = NORMAL)
						self.textCons[name].insert(END, f'<{name}> : {msg}\n\n')
						self.textCons[name].config(state = DISABLED)

				elif data and data == '~disconnect~':
					#remove friend has disconnected
					friend[0].shutdown(socket.SHUT_RD)
					friend[0].close()
					self.connect_from_friend.remove(friend)
			except:
				print("Error Receive")
				break

	def handlerExit(self):
		"""Handler closing the GUI window."""
		ans = messagebox.askyesno(title="Exit", message="Do you want to exit ?")
		if ans:
			self.sendRequest(self.LOGOUT, "")
			response = self.recvReply()
			if response[0] == "OK":
				self.isLogin = False
				self.serversocket.close()
				for friend in self.connect_to_friend:
					try:
						self.connect_to_friend[friend].send("~disconnect~".encode())
					except:
						pass
				for accept_socket in self.connect_from_friend:
					#accept_socket[0].shutdown(socket.SHUT_RD)
					accept_socket[0].close()
				#self.mysocket.shutdown(socket.SHUT_RD)
				self.mysocket.close()
				self.Window.destroy()


def main():
	Window = Tk()
	App = Client(Window, host, server_port, serversocket)
	Window.mainloop()
	Window.destroy()

if __name__ == "__main__":
    main()
