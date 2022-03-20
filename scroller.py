#!/usr/bin/python3.8

# used to spin the mouse wheel in 'Minecraft' to help place random block.
# Spins the mouse wheel and so spins the toolbar in 'Minecraft' while you press the mouse button.

# prerequisites:
# pip install pynput
#
# sources:
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://stackoverflow.com/questions/57617018/how-to-stop-pynput-keyboard-thread-outside-of-class

import random
import time
from pynput import keyboard
from pynput.keyboard import Key, Listener
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


# =====
# main script starts here
# =====

# set a global var to keep track of if I should loop
continueLooping = False

print('This program is ment to be used with Minecraft Java on a Linux based computer \n'
      'It will allow you to place random blocks from your toolbar when right clicking the mouse.')
print()
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
    # shoe the value of continue looping, this can be removed if
    # you prefer a blank termial
    print(continueLooping)
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
        time.sleep(0.005)
