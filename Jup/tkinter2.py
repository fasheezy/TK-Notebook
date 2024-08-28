import tkinter as tk
import json
import os
from tkinter import filedialog,messagebox,font, Tk,ttk,scrolledtext 
from sympy import sympify,SympifyError
#from common_funcs import * 
class Application(tk.Tk):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.title("No Save Loaded")
        self.geometry("600x400")
        self.defaultFont = font.nametofont("TkDefaultFont") 
        self.defaultFont.configure(family="Times New Roman")
        
        self.entry_boxes = {}
        self.row_counter = 1
        self.label_num = 0 
        
        self.current_file=None
        self.save_directory = "saved_states"
        self.listryoshka = "Image_files"
                # Ensure the save directory exists
        os.makedirs(self.save_directory, exist_ok=True)
        self.equation_boxes = []
        os.makedirs(self.save_directory, exist_ok=True)
        
        self.main_canvas = tk.Canvas(self)
        self.main_canvas.pack(side= tk.LEFT,fill=tk.BOTH,expand=True)
        self.frame_1 = tk.Frame(self.main_canvas)
        
       # self.frame_2 = tk.Frame(self.main_canvas)
     #   self.frame_2.bind("<Configure>", self.on_configure)
        self.main_canvas.create_window((0,0),window = self.frame_1,anchor="nw")
       # self.main_canvas.create_window((600,0),window=self.frame_2,anchor = "NE")

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.another_state = tk.Button(self.frame_1,text="Create New State",command=self.make_new_entry)
        self.another_state.grid(row=0,column=0)
       # self.update_listbox()
        


    def make_new_entry(self):
        self.prefix_placeholder = "Create A Label"
        self.row_counter+=1 
       # self
        self.new_lentry = ttk.Entry(self.frame_1)
        
        self.new_lentry.insert(0,self.prefix_placeholder)
        self.new_lentry.grid(row=self.row_counter,column=1)
        self.new_lentry.bind("<FocusIn>",self.clear_placeholder)
        self.new_lentry.bind("<FocusOut>",self.add_placeholder) 
        self.new_lentry.bind("<Return>",self.set_labellers)
        #self.reset_label = ttk.Button(
        self.new_label = tk.Label(self.frame_1,text="Label Saved")
        self.row_counter+=1 
        self.new_tbox = scrolledtext.ScrolledText(self.frame_1,wrap=tk.WORD,width=25,height=7)
        self.new_tbox.grid(row=self.row_counter,column=1)
    def clear_placeholder(self, event):
        """Clear the placeholder text when the entry gains focus."""
        if self.new_lentry.get() == self.prefix_placeholder:
            self.new_lentry.delete(0, tk.END)
            self.new_lentry.config(foreground='black')

    def add_placeholder(self, event):
        """Add the placeholder text when the entry loses focus if it's empty."""
        if self.new_lentry.get() == "":
            self.new_lentry.insert(0, self.prefix_placeholder)
            self.new_lentry.config(foreground='grey')

    def set_labellers(self,event):
        if self.new_lentry.get()!= "":
            self.new_lentry.grid_forget()
 #  def new_window(self):
        

if __name__ == "__main__":
    app = Application()
    app.mainloop()
