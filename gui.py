from Tkinter import Tk, Label, Button, StringVar

class GUI:
    LABEL_TEXT = [
        "Play some sounds"
    ]
    def __init__(self, master):
        self.master = master
        master.title("Concord")

        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master, textvariable=self.label_text)
        self.label.bind("<Button-1>", self.cycle_label_text)
        self.label.pack()

        self.sound_button = Button(master, text="Play Clint Eastwood", command=self.sound)
        self.sound_button.pack()


        self.sound_button1 = Button(master, text="Play npr", command=self.sound1)
        self.sound_button1.pack()

        self.sound_button2 = Button(master, text="Play Smash Mouth", command=self.sound2)
        self.sound_button2.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def sound(self):
        print("Greetings!")
    
    def sound1(self):
        print("Greetings!1")

    def sound2(self):
        print("Greetings!2")

    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT) # wrap around
        self.label_text.set(self.LABEL_TEXT[self.label_index])

root = Tk()
my_gui = GUI(root)
root.mainloop()