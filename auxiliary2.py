import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os
import shutil

class kalculate:
    def __init__(self,root,newcanvas):
        self.root = root 
        self.newcanvas