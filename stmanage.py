import tkinter as tk 
import numpy as np 
class replace:
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
        '/spadesuit': '♠', '/male': '♂', '/female': '♀',
        '/Rightarrow': '⇒', '/Leftarrow': '⇐', '/Leftrightarrow': '⇔',
        '/Uparrow': '⇑', '/Downarrow': '⇓'}
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
    def replace_back(self,insert):
        entries = insert
        for unspecial,special in self.conversions.items():
            entries = entries.replace(special,unspecial)
        return entries
    
class newframe:
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
    def __init__(self,frame):
        self.scrolled = frame
       # self.content=content
       # self.position = position
        self.backspace = 1
        self.delete=1
        self.tuplelist = []
    def remove_frac(self,origin,other):
        start_pos = '1.0'  
        replace_lambda = lambda start_pos: (self.scrolled.search("/frac"+origin, start_pos, stopindex=tk.END))
        while True:
            start_pos = replace_lambda(start_pos)
            print(start_pos)
            if not start_pos:
                break  
            end_pos = f"{start_pos}+{len("/frac"+origin)}c"
            self.scrolled.delete(start_pos, end_pos)
            self.create_fraction(other,start_pos)
    def remove_matrix(self,placed):
        start_pos = '1.0'  
        replace_lambda = lambda start_pos: (self.scrolled.search(str(placed), start_pos, stopindex=tk.END))
        while True:
            start_pos = replace_lambda(start_pos)
            if not start_pos:
                break
            start_pos = replace_lambda(start_pos)
            end_pos = f"{start_pos}+{len(str(placed))}c"
            self.scrolled.delete(start_pos, end_pos)
            self.create_matrix_box(placed,start_pos)
    def create_fraction(self,other,pos):
        mainframe = tk.Frame(self.scrolled,bg='white', bd=0,relief='solid')
        mainframe.pack(fill=tk.X, padx=10, pady=(5, 0))
        numerator = tk.Entry(mainframe, justify='center',highlightthickness=0, bg="white",relief='flat', font=("Times New Roman", 14))
        numerator.pack(fill=tk.X,padx=10,pady=(5, 0))
        numerator.insert(0,other[0])
        separator = tk.Frame(mainframe, bg='black',relief="flat", height=1)
        separator.pack(fill=tk.X, padx=10, pady=2)
        denominator = tk.Entry(mainframe, justify='center',highlightthickness=0, relief='flat', bg="white",font=("Times New Roman", 14))
        denominator.pack(fill=tk.X,padx=10,pady=(0,5))
        denominator.insert(0,other[1])
        numerator.bind("<KeyRelease>",self.replacer)
        denominator.bind("<KeyRelease>",self.replacer)
        numerator.bind("<Left>",self.check_focus)
        denominator.bind("<Left>",self.check_focus)
        numerator.bind("<Right>",self.check_focus)
        denominator.bind("<Right>",self.check_focus)
        numerator.bind("<Down>",lambda event, i = denominator:self.moveup(i))
        denominator.bind("<Up>",lambda event, i = numerator:self.moveup(i))
        numerator.bind("<Key>",self.newidth1)
        denominator.bind("<Key>",self.newidth2)
        numerator.focus_set()
        self.scrolled.window_create(pos, window=mainframe)
    def create_matrix_box(self,nestlist,pos):
        cells = []
        frame = tk.Frame(self.scrolled, bg='white', relief='solid')
        frame.pack(pady=5, padx=10)
        matrix_frame = tk.Frame(frame,bg="white")
        matrix_frame.grid(row=0, column=1)
        rows = len(nestlist)
        cols = len(nestlist[0])
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
                cells[i][j].bind("<KeyRelease>",self.replacer)
                cells[i][j].insert(0,nestlist[i][j])
                self.initrep(cells[i][j])
        self.scrolled.window_create(pos, window=frame)
    def check_focus(self,event):
        if event.widget.index(tk.INSERT) == event.widget.index(tk.END) or event.widget.index(tk.INSERT) =="1.0":
            self.scrolled.focus_set()
    def moveup(self,otherframe):
        try:
            otherframe.focus_set()
        except: 
            self.scrolled.focus_set()
    def replacer(self,event=None):
        curtext = event.widget.get()
        for word_to_replace,replacement_word in self.conversions.items():
            curtext = curtext.replace( word_to_replace,replacement_word)
        event.widget.delete(0, tk.END)  # Clear the entry widget
        event.widget.insert(0, curtext) 
    def newidth1(self,event):
        disckeys = ["Right","Down","Left","Up"]
        if event.keysym not in disckeys:
            if event.keysym =="Delete" or event.keysym =="BackSpace":
                self.delete -=1
            else:
                self.delete+=1
            if self.backspace != self.delete and event.keysym not in disckeys:
                event.widget.config(width=self.delete)
        else:
            pass
    def newidth2(self,event):
        disckeys = ["Right","Down","Left","Up"]
        if event.keysym not in disckeys:
            if event.keysym =="Delete" or event.keysym =="BackSpace":
                self.backspace -=1
            else:
                self.backspace+=1
            if self.backspace != self.delete and event.keysym not in disckeys:
                event.widget.config(width=self.backspace)
        else:
            pass
    def initrep(self,ins):
        curtext = ins.get()
        for word_to_replace,replacement_word in self.conversions.items():
            curtext = curtext.replace( word_to_replace,replacement_word)
        ins.delete(0, tk.END)  # Clear the entry widget
        ins.insert(0, curtext)