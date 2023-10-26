# By Faiyaz Chowdhury
from tkinter import Tk, Canvas
from math import sin, cos, atan2, sqrt, pi, log, floor
import musicalbeeps
import copy

player = musicalbeeps.Player(volume = 0.3,
                            mute_output = False)


########### USER CONSTANTS ############
N = 7 

SEVEN_THIRDHARMONICS = range(0,N*6+1,N)
SEVEN_OCTAVED_FIFTHS = [index % 12 for index in SEVEN_THIRDHARMONICS]
SEVEN_OCTAVED_FIFTHS_AUGMENTED = copy.copy(SEVEN_OCTAVED_FIFTHS)
SEVEN_OCTAVED_FIFTHS_AUGMENTED[1] = SEVEN_OCTAVED_FIFTHS_AUGMENTED[1]+1
SEVEN_OCTAVED_FIFTHS_DOUBLE_AUGMENTED = copy.copy(SEVEN_OCTAVED_FIFTHS_AUGMENTED)
SEVEN_OCTAVED_FIFTHS_DOUBLE_AUGMENTED[2] = SEVEN_OCTAVED_FIFTHS_DOUBLE_AUGMENTED[2]+1

CHOSEN_KERNEL = SEVEN_OCTAVED_FIFTHS # Picking the scale root
SCALE_SHIFT = 1 # Rotation of 12 note circle, flattening last fifths.
KEY_SHIFT = 0 # Picking out what will be the root note or the key.
OCTAVE_OFFSET = 5 # Picking base octave offset
MODE_SHIFT = 0  # Rotation of circle of N notes. Temporary change of mode of music.

HARMONIC_RANGE_0 = [0]
HARMONIC_RANGE_1 = [0, 2]
HARMONIC_RANGE_2 = [0, 2, 4, 6]
HARMONIC_RANGE_3 = [0, 1, 2, 3, 4, 6]

HARMONIC_RANGES = [HARMONIC_RANGE_1, HARMONIC_RANGE_2, [0]]
HARMONIC_RANGES = [HARMONIC_RANGE_2, HARMONIC_RANGE_2, HARMONIC_RANGE_3, [0]]

# GRAPHICS USER CONSTANTS
GROWTH = 0.5
DELTA = 800


############# END USER CONSTANTS #####################
WINDOW_SIZE = 1000
MIDDLE_SIZE = WINDOW_SIZE/2
RADIUS = WINDOW_SIZE/4
# NOTE GUI Buttons also have global values

RGB_YELLOW = (255, 255,   0)
RGB_GREEN  = ( 36, 255,   0)
RGB_BLUE   = (  0, 123, 255)
RGB_INDIGO = ( 40,   0, 255)
RGB_PURPLE = ( 97,   0,  97)
RGB_RED    = (255,   0,   0)
RGB_ORANGE = (255, 141,   0)
RGB_MID    = (128, 128, 128)

PALLET_SEVEN = (RGB_YELLOW, RGB_GREEN, RGB_BLUE, RGB_INDIGO, RGB_PURPLE, RGB_RED, RGB_ORANGE)
PALLET_TWELVE = 12*[RGB_MID]
TONES_TWELVE_KERNEL = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


SEVEN_SCALE = copy.copy(CHOSEN_KERNEL)
for lastFifth in range(1,SCALE_SHIFT+1):
    SEVEN_SCALE[-lastFifth] = SEVEN_SCALE[-lastFifth]-1
SEVEN_SCALE.sort()
TONES_KERNEL = [TONES_TWELVE_KERNEL[(index+KEY_SHIFT)%12] for index in SEVEN_SCALE]

index_shift = ((MODE_SHIFT) * 4)%N
keyRGBColors = PALLET_SEVEN[index_shift:] + PALLET_SEVEN[:index_shift]
TONES_SEVEN = TONES_KERNEL[index_shift:] + TONES_KERNEL[:index_shift]

if N == 12:
    TONES = TONES_TWELVE_KERNEL
    keyRGBColors = PALLET_TWELVE
else:
    TONES = TONES_SEVEN

print(TONES)

# Get Color from RGB
def RGBtoColor(rgb):
    """
    Changes RGB values to Hexadecimal String Color
    Arguments:
        rgb: RGB Values are tuple of 3 integers
    Returns:
        Color as Hexadecimal String
    """
    return "#%02x%02x%02x"%rgb

# Drawing A Single Trapezoid
def drawTrap(r1, theta, note, N, harmonic):
    """
    Calculates the centroid of the triangle face. Used to sort farthest triangle for Painter's algorithm implementation
    Arguments:
        face: vector of 3 vertices of the triangle face
    Returns:
        Centroid coordinate
    """
    v1 = [r1*cos(theta+r1/DELTA), r1*sin(theta+r1/DELTA)]
    theta = theta + 2*pi/N
    v2 = [r1*cos(theta-r1/DELTA), r1*sin(theta-r1/DELTA)]
    canvas.create_polygon([v1[0]+MIDDLE_SIZE,v1[1]+MIDDLE_SIZE,v2[0]+MIDDLE_SIZE,v2[1]+MIDDLE_SIZE,MIDDLE_SIZE,MIDDLE_SIZE], outline='black', fill=keyColors[(note+harmonic)%N], width=2)
    r1 = r1 * (GROWTH ** (1/N))
    return r1, theta

# Drawing N Trapezoids
def drawTrapezoids(r1, theta, N, harmonic):
    """
    Calculates the centroid of the triangle face. Used to sort farthest triangle for Painter's algorithm implementation
    Arguments:
        face: vector of 3 vertices of the triangle face
    Returns:
        Centroid coordinate
    """
    for note in range(N):
        r1, theta = drawTrap(r1, theta, note, N, harmonic)

def drawImage(N, keyColors):
    """
    Draws the image in canvas, after performing several operations
    Arguments:
        N: The number of sides the pine has
        keyColors: The Colors of each key
    """
    theta = (pi/2) - (pi/N)
    r = RADIUS
    for harmonicRange in HARMONIC_RANGES:
        harmonic_index = 0
        for harmonic in harmonicRange:
            rh = r * (GROWTH ** (harmonic_index/len(harmonicRange)))
            drawTrapezoids(rh, theta, N, harmonic)
            harmonic_index += 1

        for i in range(1000):
            thetaS = 2*pi*i/1000 + theta
            rs = r*GROWTH**(i/1000)
            x1, y1 = [rs*cos(thetaS) + MIDDLE_SIZE, rs*sin(thetaS) + MIDDLE_SIZE]
            x2, y2 = [x1, y1]
            color = RGBtoColor(wave2rgb(500))
            canvas.create_oval(x1,y1,x2,y2,fill=color, width=1)

        r = r * GROWTH

def wave2rgb(wave):
    # This is a port of javascript code from  http://stackoverflow.com/a/14917481
    gamma = 0.8
    intensity_max = 1
 
    if wave < 380:
        red, green, blue = 0, 0, 0
    elif wave < 440:
        red = -(wave - 440) / (440 - 380)
        green, blue = 0, 1
    elif wave < 490:
        red = 0
        green = (wave - 440) / (490 - 440)
        blue = 1
    elif wave < 510:
        red, green = 0, 1
        blue = -(wave - 510) / (510 - 490)
    elif wave < 580:
        red = (wave - 510) / (580 - 510)
        green, blue = 1, 0
    elif wave < 645:
        red = 1
        green = -(wave - 645) / (645 - 580)
        blue = 0
    elif wave <= 780:
        red, green, blue = 1, 0, 0
    else:
        red, green, blue = 0, 0, 0
 
    # let the intensity fall of near the vision limits
    if wave < 380:
        factor = 0
    elif wave < 420:
        factor = 0.3 + 0.7 * (wave - 380) / (420 - 380)
    elif wave < 700:
        factor = 1
    elif wave <= 780:
        factor = 0.3 + 0.7 * (780 - wave) / (780 - 700)
    else:
        factor = 0
 
    def f(c):
        if c == 0:
            return 0
        else:
            return intensity_max * pow (c * factor, gamma)
 
    return (floor(f(red)), floor(f(green)), floor(f(blue)))


#---------GUI Buttons-------------
def pressButton(event):
    """
    Sets the mouse coordinates upon clicking
    Arguments:
        event: Canvas.bind event
    """
    global press_x
    global press_y
    press_x = event.x
    press_y = event.y
    x = press_x - MIDDLE_SIZE
    y = press_y - MIDDLE_SIZE
    theta = atan2(y, x)
    theta = theta - ((pi/2) - (pi/N))
    if theta < 0:
        theta = theta + 2*pi
    r = sqrt(x**2 + y**2)

    index = floor(theta*N/2/pi)
    rad_sector = RADIUS*0.5**(index/N)
    rawOctave = floor(log(r/rad_sector)/log(GROWTH))
    if rawOctave >= len(HARMONIC_RANGES):
        octave = len(HARMONIC_RANGES)-1
    else:
        octave = rawOctave
    harmonicRange = HARMONIC_RANGES[octave]
    sector_root = rad_sector*0.5**(octave)
    if rawOctave >= len(HARMONIC_RANGES):
        harmonic_index = 0
    else:
        harmonic_index = floor(len(harmonicRange)*log(sector_root/r)/log(2))
    harmonic = harmonicRange[harmonic_index]
    octaveShifted = octave + OCTAVE_OFFSET + floor((index+harmonic)/N)
    letter = TONES_SEVEN[(index+harmonic)%N]
    if len(letter) >1:
        key = letter[0]+ str(octaveShifted) + letter[1]
    else:
        key = letter[0]+ str(octaveShifted)
    duration = 0.3 #2/(octave+1)/2/(index_shift+1)

    # To play an A on default octave n°4 for 0.2 seconds
    player.play_note(key, duration)


if __name__ == '__main__':
    keyColors = [RGBtoColor(rgbColor) for rgbColor in keyRGBColors]

    # Drawing Setup
    window = Tk()
    window.title("3D Shaded Object Part 2")
    canvas = Canvas(window, height=WINDOW_SIZE, width=WINDOW_SIZE)

    # Initial Drawing
    drawImage(N, keyColors)
    canvas.bind('<Button-1>', pressButton)

    canvas.pack()
    window.mainloop()