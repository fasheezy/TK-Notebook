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
        self.current_file = None
        self.defaultFont = font.nametofont("TkDefaultFont") 
        self.defaultFont.configure(family="Times New Roman")
        
        self.entry_boxes = {}
        self.info_boxes = {}
        self.entry_info = {}
        self.infob_info = {}
        self.row_counter = 1
        self.label_num = 2 
        self.get_box = 3 
        self.get_text = 4 
        
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

        self.main_canvas.create_window((4,4),window = self.frame_1,anchor="nw")
       # self.main_canvas.create_window((600,0),window=self.frame_2,anchor = "NE")
        self.frame_1.bind("<Configure>", self.on_configure) 
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.another_tbox = tk.Button(self.frame_1,text="Create Text Box",command=self.make_new_entry)
        self.another_tbox.grid(row=1,column=0)

        self.another_tbox1 = tk.Button(self.frame_1,text="Save State",command=self.create_new_state)
        self.another_tbox1.grid(row=2,column=0)
        #self.new_lentry = tk.Entry(self.frame_1,bg="gainsboro",fg="grey",width=20,font=("Times New Roman",17))
        self.new_tbox = scrolledtext.ScrolledText(self.frame_1,wrap=tk.WORD,width=55,height=7)


    def on_configure(self,event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def make_new_entry(self):
        self.prefix_placeholder = "Create A Label"
        self.row_counter+=2
        self.label_num += 2 
        self.get_box += 2 
        self.get_text += 2
        self.new_stuff = ""
        self.entry_boxes["Entry"+str(self.row_counter)] = tk.Entry(self.frame_1)
        self.entry_boxes["Entry"+str(self.row_counter)].insert(0,self.prefix_placeholder)
        self.entry_boxes["Entry"+str(self.row_counter)].grid(row=self.row_counter,column=1,pady=3,sticky="w")
        self.entry_boxes["Entry"+str(self.row_counter)].bind("<FocusIn>",self.clear_placeholder)
        self.entry_boxes["Entry"+str(self.row_counter)].bind("<FocusOut>",self.add_placeholder) 
        self.entry_boxes["Entry"+str(self.row_counter)].bind("<Return>",self.set_labellers)

        self.info_boxes["infobox"+str(self.label_num)] = scrolledtext.ScrolledText(self.frame_1,wrap=tk.WORD,width=55,height=7)
        self.info_boxes["infobox"+str(self.label_num)].grid(row=self.row_counter+1,column=1,pady=3,sticky="w")
        self.info_boxes["infobox"+str(self.label_num)].bind("<FocusOut>",self.save_text_boxes)
        
    def clear_placeholder(self, event):
        if event.widget.get()== "Create A Label":
            event.widget.delete(0, tk.END)

    def add_placeholder(self, event):
        if event.widget.get() == "":
            event.widget.insert(0,self.prefix_placeholder)
            self.entry_info["st_label"+str(self.get_text)] = event.widget.get()
    def set_labellers(self,event):
        self.new_stuff = event.widget.get()
        event.widget.delete(0, tk.END)
        self.focus_set()
        event.widget.insert(0,self.new_stuff)
        self.entry_info["st_label"+str(self.get_text)] = self.new_stuff

    def save_text_boxes(self,event):
        self.infob_info["stored_data"+str(self.get_box)] = event.widget.get("1.0",tk.END)
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
    def reset_widgets(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.entry_boxes = {}
        self.info_boxes = {}
        self.entry_info = {}
        self.infob_info = {}
        self.another_tbox = tk.Button(self.frame_1,text="Create Text Box",command=self.make_new_entry)
        self.another_tbox.grid(row=1,column=0)

        self.another_tbox1 = tk.Button(self.frame_1,text="Save State",command=self.create_new_state)
        self.another_tbox1.grid(row=2,column=0)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
