from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")

# Define a function to show the entered password
def show():

   ttk.Label(win, text="Your Password is: " + str(p)).pack()

password = StringVar()

# Add an Entry widget for accepting User Password
entry = Entry(win, width=25, textvariable=password, show="*")
entry.pack(pady=10)

# Add a Button to reveal the password
ttk.Button(win, text="Show Password", command=show).pack()

win.mainloop()