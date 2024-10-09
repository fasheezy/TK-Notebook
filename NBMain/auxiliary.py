import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os
import shutil
def aroundtwice(input1):
    used = input1.split(".")[1]
    use = int(used) -1
    result = str(input1.split(".")[0])+"."+str(use)
    return result
class backend:
    def __init__(self,entry,counter):
        self.entry = entry 
        self.counter = counter
        self.enforce = iterfuncs()
    def boxcreate(self):
        self.entry.grid(row = self.counter,column=1,sticky="w")
        self.entry.bind("<FocusIn>",self.enforce.clear_placeholder)
        self.entry.bind("<FocusOut>",self.enforce.add_placeholder)
        self.entry.bind("<Return>",self.enforce.set_labellers)
    def entrymake(self):
        self.entry.grid(row=self.counter,column=1,pady=3,sticky="w")
        self.entry.bind("<KeyPress>",self.enforce.delete_char)
        self.entry.bind('<<Modified>>', self.enforce.check_for_special)
        self.entry.bind("<KeyRelease>",self.enforce.check_funcs)
    def imageshow(self):
        self.entry.grid(row=self.counter,column=1,pady=3,sticky="w")
        self.entry.drop_target_register(DND_FILES)
        self.entry.dnd_bind('<<Drop>>', self.enforce.drop_image)

class iterfuncs:
    conversions = {
        '/alpha': 'α', '/beta': 'β', '/gamma': 'γ', '/delta': 'δ',
        '/epsilon': 'ε', '/zeta': 'ζ', '/eta': 'η', '/theta': 'θ',
        '/iota': 'ι', '/kappa': 'κ', '/lambda': 'λ', '/mu': 'μ',
        '/nu': 'ν', '/xi': 'ξ', '/omicron': 'ο', '/pi': 'π',
        '/rho': 'ρ', '/sigma': 'σ', '/tau': 'τ', '/upsilon': 'υ',
        '/phi': 'φ', '/chi': 'χ', '/psi': 'ψ', '/omega': 'ω',
        '/Alpha': 'Α', '/Beta': 'Β', '/Gamma': 'Γ', '/Delta': 'Δ',
        '/Epsilon': 'Ε', '/Zeta': 'Ζ', '/Eta': 'Η', '/Theta': 'Θ',
        '/Iota': 'Ι', '/Kappa': 'Κ', '/Lambda': 'Λ', '/Mu': 'Μ',
        '/Nu': 'Ν', '/Xi': 'Ξ', '/Omicron': 'Ο', '/Pi': 'Π',
        '/Rho': 'Ρ', '/Sigma': 'Σ', '/Tau': 'Τ', '/Upsilon': 'Υ',
        '/Phi': 'Φ', '/Chi': 'Χ', '/Psi': 'Ψ', '/Omega': 'Ω',
        '/infty': '∞', '/sqrt': '√', '/sum': '∑', '/prod': '∏',
        '/int': '∫', '/partial': '∂', '/nabla': '∇', '/forall': '∀',
        '/exists': '∃', '/neg': '¬', '/rightarrow': '→', '/leftarrow': '←',
        '/leftrightarrow': '↔', '/uparrow': '↑', '/downarrow': '↓',
        '/pm': '±', '/times': '×', '/div': '÷', '/neq': '≠',
        '/approx': '≈', '/leq': '≤', '/geq': '≥', '/subset': '⊂',
        '/supset': '⊃', '/subseteq': '⊆', '/supseteq': '⊇', '/cup': '∪',
        '/cap': '∩', '/emptyset': '∅', '/In': '∈', '/notin': '∉',
        '/angle': '∠', '/perp': '⊥', '/cdot': '⋅', '/star': '★',
        '/propto': '∝', '/equiv': '≡', '/otimes': '⊗', '/oplus': '⊕',
        '/bullet': '•', '/dagger': '†', '/ddagger': '‡', '/aleph': 'ℵ',
        '/prime': '′', '/hbar': 'ℏ', '/ell': 'ℓ', '/Re': 'ℜ',
        '/Im': 'ℑ', '/wp': '℘', '/deg': '°', '/copyright': '©',
        '/registered': '®', '/paragraph': '¶', '/section': '§',
        '/therefore': '∴', '/because': '∵', '/angle': '∠', '/triangle': '△',
        '/lozenge': '◊', '/clubsuit': '♣', '/diamondsuit': '♦', '/heartsuit': '♥',
        '/spadesuit': '♠', '/male': '♂', '/female': '♀'}
    def __init__(self):
        self.notations = ["noscript","subscript","superscript"]
        self.tagnum = 0 
        self.newnum = 0
        self.used_tag = self.notations[self.tagnum]
        self.new_tag = self.notations[self.newnum]
        self.loc = []
    def clear_graph(self,event):
        if event.widget.get() == "Enter an Equation":
            event.widget.delete(0, tk.END)
    def add_graph(self,event):
        if event.widget.get() == "":
            event.widget.insert(0,"Enter an Equation")        
    def clear_placeholder(self, event):
        if event.widget.get()== "Create A Label":
            event.widget.delete(0, tk.END)
    def add_placeholder(self, event):
        if event.widget.get() == "":
            event.widget.insert(0,"Create A Label")
    def drop_image(self, event):
        file_path = event.data.strip('{}')
        try:
            imager = Image.open(file_path)
            image = imager.resize((600,500))
            self.image_tk = ImageTk.PhotoImage(image)
            event.widget.config(image=self.image_tk, text='')
            event.widget.config(width=self.image_tk.width(), height=self.image_tk.height())
        except Exception as e:
            print(f"Error opening image: {e}")
        ext = os.path.splitext(file_path)[1]
        new_filename = "photo_" +str(event.widget.grid_info()["row"]) + ext
        target_path = os.path.join("image_dump",new_filename) 
        try:
            shutil.copy(file_path, target_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move the image: {e}")
    def set_labellers(self,event):
        if event.widget.get() != "":
            self.new_stuff = event.widget.get()
            event.widget.delete(0, tk.END)
            self.focus_set()
            event.widget.insert(0,self.new_stuff)
            self.entry_info[event.widget] = self.new_stuff
    def check_for_special(self,event=None):
        event.widget.tag_configure("superscript", offset=8, font=("Times New Roman", 10))
        event.widget.tag_configure("subscript", offset=-4, font=("Times New Roman", 10))
        event.widget.tag_configure("noscript",offset=0,font=("Times New Roman", 13))
        if event.widget.edit_modified():
            event.widget.edit_modified(False)
            for word_to_replace,replacement_word in self.conversions.items():
                start_pos = '1.0'  
                replace_lambda = lambda start_pos: (event.widget.search(word_to_replace, start_pos, stopindex=tk.END))
                while True:
                    start_pos = replace_lambda(start_pos)
                    if not start_pos:
                        break  
                    end_pos = f"{start_pos}+{len(word_to_replace)}c"
                    event.widget.delete(start_pos, end_pos)
                    event.widget.insert(start_pos, replacement_word)
                    
                    start_pos = end_pos
        lp = event.widget.index(tk.INSERT) 
        event.widget.tag_remove(self.used_tag,f"{lp}-1c",f"{lp}")
        event.widget.tag_add(self.new_tag,f"{lp}-1c",f"{lp}")
    def replace_back(self,insert):
        entries = insert
        for unspecial,special in self.conversions.items():
            entries = entries.replace(special,unspecial)
        return entries
    def check_funcs(self,event):
        content = event.widget.get("1.0",tk.END)
        framer = fmframe(event.widget,content,event.widget.index(tk.INSERT))
        if "/frac" in content:
            framer.clear_fraction()
    def delete_char(self,event):
        
        if event.keysym in ("Left", "Right", "Up", "Down", "Home", "End", "BackSpace", "Delete","Return"):
            return None 

        if event.char=="`": 
            self.tagnum =self.newnum 
            self.newnum = 0
            self.used_tag = self.notations[self.tagnum]
            self.new_tag = self.notations[self.newnum]
            return "break"
        elif event.char=="_":
            self.tagnum =self.newnum 
            self.newnum = 1
            self.used_tag = self.notations[self.tagnum]
            self.new_tag = self.notations[self.newnum]
            return "break"
        elif event.char == "^":
            self.tagnum =self.newnum 
            self.newnum = 2
            self.used_tag = self.notations[self.tagnum]
            self.new_tag = self.notations[self.newnum]
            return "break"
        return None
    def set_tags(self,item):
        mainlist = {}
        templist = []
        all_tags = item.tag_names()
        if all_tags:
            for tag in all_tags:
                ranges = item.tag_ranges(tag)
                if ranges:
                    for i in range(0,len(ranges),2):
                        templist.append([f'{ranges[i]}',f'{ranges[i+1]}'])
                mainlist[tag] = templist
                templist = []
        return mainlist
    def re_tag(self,widget,dictionary):
        widget.tag_configure("superscript", offset=8, font=("Times New Roman", 10))
        widget.tag_configure("subscript", offset=-4, font=("Times New Roman", 10))
        widget.tag_configure("noscript",offset=0,font=("Times New Roman", 13))
        for key,value in dictionary.items():
            for rows in value:
                widget.tag_add(key, rows[0], rows[1])
class fmframe:
    def __init__(self,frame,content,position):
        self.scrolled = frame
        self.content=content
        self.position = position
    def clear_fraction(self):
        start_index = self.content.find("/frac")
        end_index = start_index + 5
        self.scrolled.delete(f'1.0 + {start_index} chars', f'1.0 + {end_index} chars')
        self.create_fraction()
    def create_fraction(self):
        mainframe = tk.Frame(self.scrolled,bg='white', relief='solid')
        mainframe.pack(fill=tk.X, padx=10, pady=(5, 0))

        numerator = tk.Entry(mainframe, justify='center', bd=0, relief='flat', font=("Times New Roman", 14))
        numerator.pack(fill=tk.X,padx=10,pady=(5, 0))

        separator = tk.Frame(mainframe, bg='black', height=1)
        separator.pack(fill=tk.X, padx=10, pady=2)

        denominator = tk.Entry(mainframe, justify='center', bd=0, relief='flat', font=("Times New Roman", 14))
        denominator.pack(fill=tk.X,padx=10,pady=(0,5))

        self.scrolled.window_create(self.position, window=mainframe)
    def create_matrix(self):
        print("")
class plotdow:
    def __init__(self, ax,canvas,fig):
        self.ax = ax 
        self.canvas = canvas 
        self.fig = fig 
        self.xlim = [-10, 10]
        self.ylim = [-2, 2]
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.equation = ""
    def plot_graph(self,event):
        equation = event.widget.get()
        x = np.linspace(-10, 10, 400)
        try:
            if not equation.startswith('y =') and not equation.startswith('y='):
                pass
            equation = equation.replace('y=', 'y =')
            equation = equation.replace('y =', '').strip()
            equation = equation.replace('^',"**")
            equation = equation.replace(" x", "x")
            equation = equation.replace("x", "*x")
            if equation.startswith("*x"):
                equation = equation.replace("*x", "x")
            equation = equation.replace("(*x","(x")
            allowed_functions = {"np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "x": x}
            y = eval(equation, {"__builtins__": None}, allowed_functions)
            if isinstance(y, (int, float)):
                y = np.full_like(x, y)
            self.ax.clear()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.grid(True)
            self.canvas.draw()
            self.equation = equation
        except Exception as e:
            self.ax.clear()
            self.ax.set_title('Invalid Equation')
            self.canvas.draw()
    def draw_axes(self):
        self.ax.axhline(0, color='black', linewidth=1)  
        self.ax.axvline(0, color='black', linewidth=1) 

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_in(event)
        elif event.delta < 0:
            self.zoom_out(event)

    def zoom_in(self,event):
        self.xlim = [self.xlim[0] * 0.9, self.xlim[1] * 0.9] 
        self.ylim = [self.ylim[0] * 0.9, self.ylim[1] * 0.9]  
        self.update_plot()

    def zoom_out(self,event):
        self.xlim = [self.xlim[0] * 1.1, self.xlim[1] * 1.1] 
        self.ylim = [self.ylim[0] * 1.1, self.ylim[1] * 1.1]  
        self.update_plot()

    def update_plot(self):
        self.ax.cla() 
        self.ax.grid(True) 
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.draw_axes()
        self.x = np.linspace(self.xlim[0], self.xlim[1], 1000)
        self.update_function()

    def update_function(self):
        try:
            equation = self.equation
            allowed_functions = {"np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "x": self.x}
            self.y = eval(equation, {"__builtins__": None}, allowed_functions)
            self.y = eval(equation, {"x": self.x, "np": np,"__builtins__": None},allowed_functions)
            self.ax.set_title(f'Graph of y = {equation}')
            self.plot, = self.ax.plot(self.x, self.y)
            self.ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            print(f"Error in equation: {e}")