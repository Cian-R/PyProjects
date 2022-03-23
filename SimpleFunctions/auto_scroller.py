import random
import time
from pynput import keyboard
from pynput.keyboard import Key
from pynput.mouse import Controller

mouse = Controller()


def key_check(key):
    # set var to global
    global continueLooping

    try:
        # start loop
        if key.char == 'y':
            continueLooping = True

        # ignore key press
        if key.char != 'y' and key != keyboard.Key.esc:
            mouse.scroll(dx=0, dy=0)
            print('key_check - else')

    except AttributeError:
        print('Key_check - finally')


def on_release(key):
    # set var to global
    global continueLooping
    print("key relase, running...")

    if key == Key.esc:
        continueLooping = False
        mouse.scroll(dx=0, dy=0)
        print('mouse = 0')


def scroll_wheel():
    random_spin = random.randrange(1, 10)
    mouse.scroll(dx=0, dy=random_spin)


# set a global var to keep track of if I should loop
continueLooping = False

print('Press the "y" to start the scrolling of the mouse wheel')
print('Press the "Esc" to stop the scrolling')

# set up listener in non blocking mode
listener = keyboard.Listener(
    on_press=key_check,
    on_release=on_release)
listener.start()

# create a infinite loop to listen to keyboard
print("waiting for key input...")
while True:
    time.sleep(1)
    # check global var if to continue looping
    while continueLooping:
        # show that you are in the loop, this can be removed if
        # you prefer a blank terminal
        print("loop")
        scroll_wheel()
        # interval between scrolls
        # lower if you want the scroll between items faster
        # this can be removed to scroll as fast as possible
        time.sleep(0.01)
