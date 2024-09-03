import tkinter as tk
import json
import os
from tkinter import filedialog,messagebox,font, Tk,ttk,scrolledtext
from sympy import sympify,SympifyError
from IPython.display import clear_output as co
class Application(tk.Tk):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.title("No Save Loaded")
        self.geometry("600x400")
        self.current_file = None
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Times New Roman")


        self.entry_boxes = {}
        self.info_boxes = {}
        self.entry_info = {}
        self.infob_info = {}
        self.new_labels = {}
        self.other_frames = {}
        self.label_num = 1
        self.row_counter = 2


        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT,fill=tk.Y)
        self.current_file=None
        self.save_directory = "saved_states"
        self.listryoshka = "Image_files"
                # Ensure the save directory exists
        os.makedirs(self.save_directory, exist_ok=True)
        self.equation_boxes = []
        os.makedirs(self.save_directory, exist_ok=True)

        self.main_canvas = tk.Canvas(self)
        self.main_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.frame_1 = tk.Frame(self.main_canvas)

        self.main_canvas.create_window((4,4),window = self.frame_1,anchor="nw")
        self.frame_1.bind("<Configure>", self.on_configure)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.another_tbox = tk.Button(self.button_frame,text="Save State",command=self.create_new_state)
        self.another_tbox.pack(fill="x")
        self.button1 = tk.Button(self.button_frame,text="Create Text Boxes",command = self.make_new_entry)
        self.button2 = tk.Button(self.button_frame,text="Create Equation",command=self.make_new_equation)
        self.button3 = tk.Button(self.button_frame,text="Create Text Box",command=self.make_new_entry)
        self.button1.pack(fill="x")
        self.button2.pack(fill="x")
        self.button3.pack(fill="x")
        self.prefix_placeholder = "Create A Label"
    def on_configure(self,event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    def make_labels(self):
        self.label_num+=2
        self.entry_boxes["Entry"+str(self.label_num)] = tk.Entry(self.frame_1)
        self.entry_boxes["Entry"+str(self.label_num)].insert(0,self.prefix_placeholder)
        self.entry_boxes["Entry"+str(self.label_num)].grid(row=self.label_num,column=1,pady=3,sticky="w")
        self.entry_boxes["Entry"+str(self.label_num)].bind("<FocusIn>",self.clear_placeholder)
        self.entry_boxes["Entry"+str(self.label_num)].bind("<FocusOut>",self.add_placeholder)
        self.entry_boxes["Entry"+str(self.label_num)].bind("<Return>",self.set_labellers)

    def make_new_equation(self):
        self.make_labels()
        self.row_counter += 2
        self.info_boxes["Equation Box"+str(self.row_counter)] = tk.Text(self.frame_1,height = 2)
        self.info_boxes["Equation Box"+str(self.row_counter)].grid(row=self.row_counter,column=1,sticky="ew")
        self.info_boxes["Equation Box"+str(self.row_counter)].insert(tk.END,"")
        self.info_boxes["Equation Box"+str(self.row_counter)].bind("<KeyRelease>",self.process_equation)
        self.new_stuff = ""
        self.new_labels["Label"+str(self.row_counter+1)] = tk.Label(self.frame_1,height=2)
        self.new_labels["Label"+str(self.row_counter+1)].grid(row=self.row_counter+1,column=1,sticky="ew")
        self.row_counter+=2
        self.label_num+=2
    def make_new_entry(self):
       # self.label_num +=1
        self.make_labels()
        self.row_counter+=2
        self.info_boxes["infobox"+str(self.label_num)] = scrolledtext.ScrolledText(self.frame_1,wrap=tk.WORD,width=55,height=7)
        self.info_boxes["infobox"+str(self.label_num)].grid(row=self.row_counter,column=1,pady=3,sticky="w")
        self.info_boxes["infobox"+str(self.label_num)].bind("<FocusOut>",self.save_text_boxes)
    def process_equation(self,event):
        equation_text = event.widget.get("1.0",tk.END).strip()
        final = []
        entrance_set = equation_text.split("\n")
        print(entrance_set)
        co(wait=True)
        for enters in entrance_set:
            rendered_text=self.markdown_convert(enters)
            result_text=self.calculate_equation(rendered_text)
            if "=" in enters:
                final.append(rendered_text)
            else:
                final.append(f"{rendered_text} = {result_text}")
        final_output = ("\n").join(final)
        #final_output = f"{rendered_text} = {result_text}"
        rendered_label = event.widget.grid_info()["row"] + 1  # Row after the input box
        for widget in self.frame_1.grid_slaves(row=rendered_label):
            if isinstance(widget, tk.Label):
                widget.config(text=final_output, anchor="w", justify="left")
                break

    def markdown_convert(self,text):
        conversions = {
            '^': 'ⁿ', '_': 'ₙ','**': '𝒃','*': '𝒊','~~': '̶','sqrt': '√','pi': 'π',
            'theta': 'θ','alpha': 'α','beta': 'β','gamma': 'γ','delta': 'δ','lambda':'λ',
            'mu': 'μ','omega': 'ω', 'int': '∫','sum': '∑','prod': '∏','infty': '∞','approx': '≈',
            '!=': '≠','>=': '≥','<=': '≤','->': '→', '<-': '←','=>': '⇒','<=': '⇐','...': '…',
            'sum_': '∑ₙ','sqrt(': '√(','int_': '∫ₙ','lim': 'lim','lim_': 'limₙ','sin': 'sin',
            'cos': 'cos','tan': 'tan','log': 'log','ln': 'ln','exp': 'exp','frac': '⁄','cdot': '⋅',
            'times': '×','div': '÷', 'leq': '≤','geq': '≥','neq': '≠','subset': '⊂','supset': '⊃',
            'subseteq': '⊆', 'supseteq': '⊇','cup': '∪','cap': '∩','forall': '∀', 'exists': '∃',
            'nabla': '∇','Alpha': 'Α','Beta': 'Β','Gamma': 'Γ','Delta': 'Δ','Epsilon': 'Ε',
            'Zeta': 'Ζ','Eta': 'Η','Theta': 'Θ','Iota': 'Ι','Kappa': 'Κ','Lambda': 'Λ',
            'Mu': 'Μ','Nu': 'Ν','Xi': 'Ξ','Omicron': 'Ο','Pi': 'Π','Rho': 'Ρ',
            'Sigma': 'Σ','Tau': 'Τ','Upsilon': 'Υ','Phi': 'Φ','Chi': 'Χ','Psi': 'Ψ',
            'Omega': 'Ω'}
        for key, value in conversions.items():
            text = text.replace(key, value)
        print(text)
        print(type(text))
        co(wait=True)
        return text

    def calculate_equation(self,text):
        try:
            result = sympify(text)
            return result
        except SympifyError:
            return "Invalid Equation"
    def clear_placeholder(self, event):
        if event.widget.get()== "Create A Label":
            event.widget.delete(0, tk.END)

    def add_placeholder(self, event):
        if event.widget.get() == "":
            event.widget.insert(0,self.prefix_placeholder)
        elif event.widget.get() != "":
            self.entry_info[event.widget] = event.widget.get()
    def set_labellers(self,event):
        if event.widget.get() != "":
            self.new_stuff = event.widget.get()
            event.widget.delete(0, tk.END)
            self.focus_set()
            event.widget.insert(0,self.new_stuff)
            self.entry_info[event.widget] = self.new_stuff

    def save_text_boxes(self,event):
        self.infob_info[event.widget] = event.widget.get("1.0",tk.END)
   # def save_entry_boxes(self):

 #  def new_window(self):
    def create_new_state(self):
        print(self.info_boxes)
        print(self.infob_info)
        # Prompt for a new state name
        infom = {}
        entrym = {}
        meta = {}
        ticket = {}
        master = {}
        n = 0
        for i in self.info_boxes.values():
            infom["infobox"+str(n)] = str(i)
            n+=1
        n=0
        for i in self.entry_boxes.values():
            entrym["entry"+str(n)] = str(i)
            n+=1
        n=0
        for i in self.entry_info.values():
            ticket["labels"+str(n)] = str(i)
            n+=1
        n=0
        for i in self.infob_info.values():
            meta["text"+str(n)] = str(i)
            n+=1
        new_state_name = filedialog.asksaveasfilename(
            initialdir=self.save_directory,
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All Files", "*.*")],
            title="Create New State"
        )
        if new_state_name:
            master["Labels"] = infom
            master["Entry Boxes"] = entrym
            master["Label Text"] = ticket
            master["Box Text"] = meta
            # Initialize a new state
            leak = open(new_state_name,"w")
            json.dump(master,leak,indent=1)
            self.current_file = new_state_name
            self.reset_widgets()
    def reload_state(self):
        print("nothing yet")
    def reset_widgets(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.entry_boxes = {}
        self.info_boxes = {}
        self.entry_info = {}
        self.infob_info = {}


if __name__ == "__main__":
    app = Application()
    app.mainloop()
