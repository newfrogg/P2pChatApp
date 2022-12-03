from tkinter import *
import time
import socket

Temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostbyname(socket.gethostname()))

Window = Tk()
Window.geometry("700x700")
list_friend = ["Duc", "Vinh", "Triet"]
frames = {}

a = {"a":1, "b":2, "c":3}
for x in a:
    print(x)
my_menu = Menu(Window)
menuFriend = Menu(my_menu)
my_menu.add_cascade(label="Friends", menu=menuFriend)

frames["Duc"] = Frame(Window, width=400, height=400, bg="red")
frames["Vinh"] = Frame(Window, width=400, height=400, bg="blue")
frames["Triet"] = Frame(Window, width=400, height=400, bg="green")
 



Window.config(menu=my_menu)

for friend in list_friend:
    menuFriend.add_command(label=friend, command=lambda
                                    x=frames[friend]:layout(x))

text = Text(frames["Duc"], width=700, height=700, fg="#EAECEE",
                            bg="#17202A", padx=5, pady=5)
text.place(relheight=0.745, relwidth=0.8, relx=0.08, rely=0.08)




def layout(frame):
    hide_all_frame()
    frame.pack(fill="both", expand=1)

def hide_all_frame():
    for friend in list_friend:
        frames[friend].pack_forget()

#Window.mainloop()