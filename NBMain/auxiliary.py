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
        self.entry.bind("<Left>",self.enforce.refocus_left)
        self.entry.bind("<Right>",self.enforce.refocus_right)
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
        '/int': '∫', '/partial': '∂', "/domain":'ℝ','/nabla': '∇', '/forall': '∀',
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
            print(self.image_tk)
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
        elif "/mat" in content:
            framer.clear_matrix()
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
    def refocus_left(self,event):
        try:
            widgets = event.widget.window_cget(f"{event.widget.index(tk.INSERT)}-1c","window")
        except tk.TclError:
            widgets = None
        if widgets:
            embed_frame = event.widget.nametowidget(widgets)
            if isinstance(embed_frame.winfo_children()[0],tk.Entry):
                numerator = embed_frame.winfo_children()[0]
                numerator.focus_set()
            else:
                for box in embed_frame.winfo_children():
                    if len(box.winfo_children())>=1:
                        if isinstance(box.winfo_children()[0],tk.Entry):
                            box.winfo_children()[0].focus_set()
                            break
    def refocus_right(self,event):
        try:
            widgets = event.widget.window_cget(event.widget.index(tk.INSERT),"window")
        except tk.TclError:
            widgets = None
        if widgets:
            embed_frame = event.widget.nametowidget(widgets)
            if isinstance(embed_frame.winfo_children()[0],tk.Entry):
                numerator = embed_frame.winfo_children()[0]
                numerator.focus_set()
            else:
                for box in embed_frame.winfo_children():
                    if len(box.winfo_children())>=1:
                        if isinstance(box.winfo_children()[0],tk.Entry):
                            box.winfo_children()[1].focus_set()
                            break



class replace:
    def re_tag(widget,dictionary):
        widget.tag_configure("superscript", offset=8, font=("Times New Roman", 10))
        widget.tag_configure("subscript", offset=-4, font=("Times New Roman", 10))
        widget.tag_configure("noscript",offset=0,font=("Times New Roman", 13))
        for key,value in dictionary.items():
            for rows in value:
                widget.tag_add(key, rows[0], rows[1])
    def graball(egg):
        content = ""
        current_index = egg.index("1.0")
        end_index = egg.index(tk.END)
        matridex1 = []
        while current_index != end_index:
            try:
                widget = egg.window_cget(current_index, "window")
            except tk.TclError:
                widget = None
            if widget:
                fraction_frame = egg.nametowidget(widget)
                try:
                    numerator_entry = fraction_frame.winfo_children()[0]
                    denominator_entry = fraction_frame.winfo_children()[2]
                    numerator = numerator_entry.get()
                    denominator = denominator_entry.get()
                    content += f"/frac{{{numerator}}}{{{denominator}}} "
                except:
                    pass
                try:
                    for something in fraction_frame.winfo_children():
                        if len(something.winfo_children()) >=1: 
                            for inform in something.winfo_children():
                                if isinstance(inform,tk.Entry):
                                    matridex1.append(inform.get())
                    cleanmat = np.array(matridex1)
                    cleanlist = cleanmat.reshape(round(fraction_frame.winfo_height()/21),round(fraction_frame.winfo_width()/38))
                    content += str(cleanlist.tolist())
                    matridex1 = []
                except:
                    pass
            else:
                content += str(egg.get(current_index, f"{current_index} +1c"))

            current_index = egg.index(f"{current_index} +1c")
        return content
    def set_tags(item):
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
    
class fmframe:
    def __init__(self,frame,content,position):
        self.scrolled = frame
        self.content=content
        self.position = position
        self.tuplelist = []
    def clear_fraction(self):
        start_pos = '1.0'  
        replace_lambda = lambda start_pos: (self.scrolled.search("/frac", start_pos, stopindex=tk.END))
        while True:
            start_pos = replace_lambda(start_pos)
            if not start_pos:
                break  
            end_pos = f"{start_pos}+{len("/frac")}c"
            self.scrolled.delete(start_pos, end_pos)
        self.create_fraction()
    def clear_matrix(self):
        start_pos = '1.0'  
        replace_lambda = lambda start_pos: (self.scrolled.search("/mat", start_pos, stopindex=tk.END))
        while True:
            start_pos = replace_lambda(start_pos)
            if not start_pos:
                break  
            end_pos = f"{start_pos}+{len("/mat")}c"
            self.scrolled.delete(start_pos, end_pos)
        self.create_matrix()
    def create_fraction(self):
        mainframe = tk.Frame(self.scrolled,bg='white', bd=0,relief='solid')
        mainframe.pack(fill=tk.X, padx=10, pady=(5, 0))

        numerator = tk.Entry(mainframe, justify='center',highlightthickness=0, bg="white",relief='flat', font=("Times New Roman", 14))
        numerator.pack(fill=tk.X,padx=10,pady=(5, 0))

        separator = tk.Frame(mainframe, bg='black',relief="flat", height=1)
        separator.pack(fill=tk.X, padx=10, pady=2)

        denominator = tk.Entry(mainframe, justify='center',highlightthickness=0, relief='flat', bg="white",font=("Times New Roman", 14))
        denominator.pack(fill=tk.X,padx=10,pady=(0,5))

        mainframe.bind("<<Modified>>",self.replacer)
        denominator.bind("<<Modified>>",self.replacer)
        numerator.bind("<<Modified>>",self.replacer)
        numerator.bind("<Left>",self.check_focus)
        denominator.bind("<Left>",self.check_focus)
        numerator.bind("<Right>",self.check_focus)
        denominator.bind("<Right>",self.check_focus)
        numerator.bind("<Down>",lambda event, i = denominator:self.moveup(i))
        denominator.bind("<Up>",lambda event, i = numerator:self.moveup(i))
        numerator.focus_set()
        self.scrolled.window_create(self.position, window=mainframe)
    def create_matrix(self):
        input_frame = tk.Frame(self.scrolled)
        input_frame.pack(pady=5, padx=10)
        rows_entry = tk.Entry(input_frame, width=3, justify='center', bd=0, relief='solid')
        rows_entry.pack(side=tk.LEFT, padx=2)
        cols_entry = tk.Entry(input_frame, width=3, justify='center', bd=0, relief='solid')
        cols_entry.pack(side=tk.LEFT, padx=2)
        rows_entry.focus_set()
        def dimension_entered(event=None):
            try:
                rows = int(rows_entry.get())
                cols = int(cols_entry.get())
                if 1 <= rows <= 20 and 1 <= cols <= 20:
                    input_frame.destroy()
                    self.create_matrix_box(rows, cols)
                else:
                    pass
            except ValueError:
                pass

        rows_entry.bind("<FocusOut>", dimension_entered)
        cols_entry.bind("<FocusOut>", dimension_entered)
        rows_entry.bind("<Right>",lambda event, i = cols_entry:self.moveup(i))
        cols_entry.bind("<Right>",self.check_focus)

        self.scrolled.window_create(self.position, window=input_frame)
    def create_matrix_box(self,rows,cols):
        cells = []
        frame = tk.Frame(self.scrolled, bg='white', relief='solid')
        frame.pack(pady=5, padx=10)
       # bracket_frame_left = tk.Frame(frame)
        #bracket_frame_left.grid(row=0, column=0, rowspan=rows + 2)
        matrix_frame = tk.Frame(frame,bg="white")
        matrix_frame.grid(row=0, column=1)
        for r in range(rows):
            rowes = []
            for c in range(cols):
                cell = tk.Entry(matrix_frame, width=5, justify='center', bd=1, relief='solid')
                cell.grid(row=r, column=c, padx=2, pady=2)
                rowes.append(cell)
            cells.append(rowes)
        def navigate(event, row, col):
            if event.keysym == "Up":
                new_row = (row - 1) 
                if new_row == -1:
                    self.scrolled.focus_set()
                else:
                    cells[new_row][col].focus_set()
            elif event.keysym == "Down":
                new_row = (row + 1) 
                try:
                    cells[new_row][col].focus_set()
                except:
                    self.scrolled.focus_set()    
            elif event.keysym == "Left":
                new_col = (col - 1) 
                if new_col == -1:
                    self.scrolled.focus_set()
                else:
                    cells[row][new_col].focus_set()
            elif event.keysym == "Right":
                new_col = (col + 1) 
                try:
                    cells[row][new_col].focus_set()
                except:
                    self.scrolled.focus_set()

        for i in range(rows):
            for j in range(cols):
                cells[i][j].bind("<Key>", lambda e, row=i, col=j: navigate(e, row, col))
        self.scrolled.window_create(self.position, window=frame)
    def check_focus(self,event):
        if event.widget.index(tk.INSERT) == event.widget.index(tk.END) or event.widget.index(tk.INSERT) =="1.0":
            self.scrolled.focus_set()
    def moveup(self,otherframe):
        try:
            otherframe.focus_set()
        except: 
            self.scrolled.focus_set()
    
        

    def replacer(self,event=None):
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
         '/perp': '⊥', '/cdot': '⋅', '/star': '★',
        '/propto': '∝', '/equiv': '≡', '/otimes': '⊗', '/oplus': '⊕',
        '/bullet': '•', '/dagger': '†', '/ddagger': '‡', '/aleph': 'ℵ',
        '/prime': '′', '/hbar': 'ℏ', '/ell': 'ℓ', '/Re': 'ℜ',
        '/Im': 'ℑ', '/wp': '℘', '/deg': '°', '/copyright': '©',
        '/registered': '®', '/paragraph': '¶', '/section': '§',
        '/therefore': '∴', '/because': '∵', '/angle': '∠', '/triangle': '△',
        '/lozenge': '◊', '/clubsuit': '♣', '/diamondsuit': '♦', '/heartsuit': '♥',
        '/spadesuit': '♠', '/male': '♂', '/female': '♀'}
        if event.widget.edit_modified():
            event.widget.edit_modified(False)
            for word_to_replace,replacement_word in conversions.items():
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
