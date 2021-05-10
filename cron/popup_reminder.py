import tkinter
from tkinter import messagebox
import random
messages = [
        'Take the medicine!',
        'How about you take your tablet?',
        'Go ahead, take the medicine!',
        'Do take the medicine!'
        ]

window = tkinter.Tk()
window.wm_withdraw()
messagebox.showinfo(title="Reminder", message=random.choice(messages))

window.destroy()
