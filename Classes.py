import math
import os # Allows access to system statistics
import psutil # Allows access to virtual memor stats
from pyspectator.processor import Cpu # Python library for access resource stats (CPU)
from pyspectator.network import NetworkInterface # Library for access resource stats (NIC) 
from pythonping import ping # Library used for the simplified running of network commands
import re # Regex for detecting patterns in strings
import subprocess # Library for running terminal commands through Python
from time import sleep # Pauses code exection. Time passed to method in "seconds"
import tkinter as tk # Library used to create the GUI and its widgets
from tkinter import *


class TestClass:
    
    def __init__(self, word):
        self.word = word
        self.spill_the_beans(self.word)
        
    def spill_the_beans(self, word):
        print(f"Output: {word}")