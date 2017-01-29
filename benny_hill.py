import time
import math
import re
import numbers
import decimal

from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file
from ewmh import EWMH
from tkinter import Tk, Label, Button, StringVar

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

        self.sound_button = Button(master, text="Clint Eastwood", command=self.sound)
        self.sound_button.pack()


        self.sound_button1 = Button(master, text="This American Life", command=self.sound1)
        self.sound_button1.pack()

        self.sound_button2 = Button(master, text="Smash Mouth", command=self.sound2)
        self.sound_button2.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def sound(self):
        data = load_wav_file("test.wav")
        source.queue(data)

        sink.play(source)

        while True:
            source.position = get_window_3d_coords(current_window).return_tup()
            sink.update()

            print("playing at %s" % str(source.position))

            time.sleep(0.1)
    
    def sound1(self):
        data = load_wav_file("thisAmericanLife.wav")
        source.queue(data)

        sink.play(source)

        while True:
            source.position = get_window_3d_coords(current_window).return_tup()
            sink.update()

            print("playing at %s" % str(source.position))

            time.sleep(0.1)

    def sound2(self):
        data = load_wav_file("AllStar.wav")
        source.queue(data)

        sink.play(source)

        while True:
            source.position = get_window_3d_coords(current_window).return_tup()
            sink.update()

            print("playing at %s" % str(source.position))

            time.sleep(0.1)

    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT) # wrap around
        self.label_text.set(self.LABEL_TEXT[self.label_index])

class vector():
    """ A 2D point class with basic transformation functions. """

    def __init__(self, tup): self.elements = tuple(tup)

    def __len__(self): return len(self.elements)

    def __add__(self, a):
        if not isinstance(a, vector):
            raise ValueError("Cannot add non vector object to vector.")

        if (len(self) != len(a)):
            raise ValueError("Vectors do not have the same dimension.")

        return vector(tuple(x + y for (x,y) in zip(self.elements, a.elements)))

    def __sub__(self, a):
        if not isinstance(a, vector):
            raise ValueError("Cannot add non vector object to vector.")

        if (len(self) != len(a)):
            raise ValueError("Vectors do not have the same dimension.")

        return vector(tuple(x - y for (x,y) in zip(self.elements, a.elements)))

    def __truediv__(self, scalar):
        if not isinstance(scalar, numbers.Number):
            raise ValueError("Cannot divide vector by non-scalar.")

        if scalar == 0: raise ValueError("Cannot divide by zero.")

        return vector(tuple(x/scalar for x in self.elements))

    def __str__(self): return str(self.elements)

    def __getitem__(self, i):
        """ Obtains the i'th element of the vector """

        if not isinstance(i, int): raise ValueError("Index must be an integer.")

        return self.elements[i]

    def norm(self):
        """ Computes the l2 norm of the vector
            (the square root of the sum of squares) """

        return math.sqrt(sum(x*x for x in self.elements))

    def normalize(self):
        """ Returns the vector scaled so it lies on the unit sphere. """

        return self/self.norm()

    def reflect_y(self):
        """ Reflects a two dimensional vector in the y-axis. """

        if (len(self) != 2): raise ValueError("Vector must be two dimensional.")

        return vector((self.elements[0], -self.elements[1]))

    def cross_prod(self):
        """ In two dimensions, calculates the vector obtained by rotating
            a vector 90 degree anticlockwise, so the vector 'points right'
            with respect to the orientation of the vector against its
            orthogonal plane.

            Proof that this vector points right:
                If H is the half plane defined by {w: <v,w> <= 0}, then H
                is an oriented manifold with boundary. Then H is oriented,
                such that x points right if {x,v} is correctly oriented,
                which means that x1v2 - x2v1 > 0. If x = (v2, -v1), then
                x1v2 - x2v1 = v2^2 + v1^2 > 0, so that x points right.
        """

        if (len(self) != 2): raise ValueError("Vector must be two dimensional.")

        return vector((self.elements[1], -self.elements[0]))

    def return_tup(self): return self.elements






def get_frame(client):
    """ I have no idea what's going on here, but it works? """

    frame = client

    while (frame.query_tree().parent != ewmh.root): frame = frame.query_tree().parent

    return frame

def filter_dict(txt):
    """ Finds the string in txt representing a dictionary,
        where txt is formatted in some weird way so we had
        to hack together a solution.
    """

    regexp = re.compile(".*?(\\{.*?\\})", re.IGNORECASE|re.DOTALL)
    outcome = regexp.search(txt).group(1)
    dictionary_str = (outcome.replace("\"", "").replace("'", "\"")
                             .replace("<", "\"").replace(">", "\"")
                             .replace("\"\"", "\"").replace("\"X", "")
                             .replace("w\"",""))

    return(eval(dictionary_str))

def parse_window_info(window):
    """ Computes the top left and bottom right coordinates of
        a window in pixels, as well as the width and height of
        the window. """

    info_dict = filter_dict(str(get_frame(window).get_geometry()))

    window_topleft = vector((info_dict["x"], info_dict["y"]))
    window_dimensions = vector((info_dict["width"], info_dict["height"]))
    window_botright = window_topleft + window_dimensions

    return (window_topleft, window_dimensions, window_botright)





def convert_monitor_to_environment(monitor_coords,
                                   monitor_orientation,
                                   screen_coords):
    """ Computes the relative position of a pixel on the
        monitor, givings its position and outward pointing
        unit vector in space, as well as the coordinates of
        the item on the screen of the monitor. """

    #print(monitor_coords, monitor_orientation, screen_coords)

    # Rotate screen_coords to fit on screen in real life.
    perpendicular = monitor_orientation.cross_prod().normalize()

    print(screen_coords)

    return vector((
            monitor_coords[0] - perpendicular[0]*screen_coords[0],
            monitor_coords[1] - perpendicular[1]*screen_coords[0],
            screen_coords[1]
    ))

def get_window_3d_coords(window):
    (window_topleft, window_dimensions, window_botright) = parse_window_info(window)
    print(window_topleft)
    window_centre = (window_topleft + window_botright)/2

    # Now project our position onto real life.
    monitor = 2 if (window_topleft[0] > 1366) else 1

    if (monitor == 1):
        monitor_topleft = vector((0,0))
        monitor_botright = vector((1366, 918))
    elif (monitor == 2):
        monitor_topleft = vector((1366,0))
        monitor_botright = vector((3633, 918))
    else:
        raise ValueError("BADD!")

    monitor_dimensions = monitor_botright - monitor_topleft
    monitor_centre = (monitor_botright + monitor_topleft)/2

    screen_coords = ((window_centre - monitor_centre)/100).reflect_y()

    print(monitor)
    return convert_monitor_to_environment(
            get_monitor_positions()[monitor],
            get_monitor_orientations()[monitor],
            screen_coords
    )

def get_monitor_positions(): return { 1: vector((-1,0)),  2: vector((1,0)) }

def get_monitor_orientations(): return { 1: vector((1,0)), 2: vector((-1,0)) }

if __name__ == "__main__":
    ewmh = EWMH()

    monitor_positions = get_monitor_positions()

    current_window = ewmh.getActiveWindow()

    sink = SoundSink()
    sink.activate()

    source = SoundSource(position=[0,0,0,0,1,0])
    source.looping = True

    root = Tk()
    my_gui = GUI(root)
    root.mainloop()
