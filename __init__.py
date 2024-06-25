from os import name

if (name == 'nt'):
    from tkinter import messagebox
else:
    from .messagebox import *
