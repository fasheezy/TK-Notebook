import tkinter as tk
import json
import os
from tkinter import filedialog,messagebox,font, Tk,ttk,scrolledtext
#from sympy import sympify,SympifyError
from tkinterdnd2 import TkinterDnD, DND_FILES
from auxiliary import * 
from stmanage import *
from auxiliary2 import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import shutil 
import time
import re
import ast
class Application(TkinterDnD.Tk):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.title("No Save Loaded")
        self.geometry("600x400")
        self.current_file = None
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Times New Roman")
        self.restarted = True
        self.entry_boxes = {}
        self.info_boxes = {}
        self.pic_boxes={}
        self.master_boxes = {}
        self.label_num = -1
        self.row_counter = 0 

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT,fill=tk.Y)
        self.frame_1.bind("<Configure>", self.on_configure)
        self.frame_1 = tk.Frame(self.main_canvas)
        self.frame_2 = 
        self.current_file=None
        os.makedirs("saved_states", exist_ok=True)
        os.makedirs("image_files", exist_ok=True)
        os.makedirs("image_dump",exist_ok=True)

        self.main_canvas = tk.Canvas(self)
        self.main_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        

        self.main_canvas.create_window((4,4),window = self.frame_1,anchor="nw")
        
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.button0 = tk.Button(self.button_frame,text="Reload Old Save",command=self.reload_state)
        self.button1 = tk.Button(self.button_frame,text="Create Text Boxes",command = self.make_new_entry)
        self.button2 = tk.Button(self.button_frame,text="Create Graph",command=self.create_graphs) 
        self.button3 = tk.Button(self.button_frame,text="Create Image Box",command=self.image_placer)
        self.button4 = tk.Button(self.button_frame,text="Create New Save",command=self.create_new_state)
        self.button5 = tk.Button(self.button_frame,text="Settings",command=self.set_settings)
        self.button0.pack(pady=5,fill="x")
        self.button1.pack(pady=5,fill="x")
        #self.button2.pack(pady=5,fill="x") Uncomment if you want graphs and have windows
        self.button3.pack(pady=5,fill="x")
        self.button4.pack(pady=5,fill="x")
        self.button5.pack(pady=5,fill="x")
    def on_configure(self,event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    def make_labels(self):
        self.label_num+=2
        self.entry_boxes["Entry"+str(self.label_num)] = tk.Entry(self.frame_1,fg='gray1',font=("Times New Roman", 12))
        if self.restarted==True:
            self.entry_boxes["Entry"+str(self.label_num)].insert(0,"Create A Label")
        backdoor = backend(self.entry_boxes["Entry"+str(self.label_num)],self.label_num)
        button = tk.Button(self.frame_1,text ="Delete Entry",command = lambda: self.remove_widget(button))
        button.grid(row=self.label_num,column=1,sticky="e")
        backdoor.boxcreate()

    def make_new_entry(self):
        if self.restarted==True:
            self.make_labels()
        self.row_counter+=2
        self.info_boxes["infobox"+str(self.row_counter)] = scrolledtext.ScrolledText(self.frame_1,wrap=tk.WORD,width=75,height=10)
        boxes = backend(self.info_boxes["infobox"+str(self.row_counter)],self.row_counter)
        boxes.entrymake()
    def image_placer(self):
        if self.restarted==True:
            self.make_labels()
        self.row_counter+=2
        self.pic_boxes["picbox"+str(self.row_counter)] = tk.Label(self.frame_1, text="Drag and drop an image here", bg="gray", width=40, height=20)
        boxes = backend(self.pic_boxes["picbox"+str(self.row_counter)],self.row_counter)
        boxes.imageshow()
    def reimage(self,image):
        self.row_counter +=2 
        placeholder = ImageTk.PhotoImage(image)
        self.pic_boxes["picbox"+str(self.row_counter)] = tk.Label(self.frame_1, image=placeholder, bg="gray", width=placeholder.width(), height=placeholder.height())
        func = backend(self.pic_boxes["picbox"+str(self.row_counter)],self.row_counter)
        func.imageshow()
        self.pic_boxes["picbox"+str(self.row_counter)].config(image=placeholder, text='')
        self.pic_boxes["picbox"+str(self.row_counter)].config(width=placeholder.width(), height=placeholder.height())
    def remove_widget(self,loc):
        extract = loc.grid_info()["row"]
        for widget in self.frame_1.grid_slaves(row=extract, column=1):
            widget.destroy()  
        for widget in self.frame_1.grid_slaves(row=extract+1,column=1):
            widget.destroy()  
            if isinstance(widget,tk.Label):
                for photo in os.listdir("image_dump"):
                    if extract+1 == int(photo.split("_")[1][0]):
                        os.remove("image_dump/"+photo)
    def set_settings(self):
        for wick in self.button_frame.winfo_children():
            wick.destroy()
        for lick in self.frame_1.winfo_children():
            lick.destroy()
    def create_graphs(self):
        helper = iterfuncs()
        self.row_counter +=2
        self.label_num +=2 
        button = tk.Button(self.frame_1,text ="Delete Entry",command = lambda: self.remove_widget(button))
        button.grid(row=self.label_num,column=1,sticky="e")
        fig, ax = plt.subplots(figsize=(4, 2))
        canvas = FigureCanvasTkAgg(fig, master=self.frame_1) 
        self.entry_boxes["Entry"+str(self.label_num)] = tk.Entry(self.frame_1,fg='gray2')
        graphix = plotdow(ax,canvas,fig)
        canvas.get_tk_widget().grid(row=self.row_counter,column=1)
        self.entry_boxes["Entry"+str(self.label_num)].bind("<KeyRelease>",graphix.plot_graph)
        self.entry_boxes["Entry"+str(self.label_num)].bind("<FocusIn>", helper.clear_graph)
        self.entry_boxes["Entry"+str(self.label_num)].bind("<FocusOut>",helper.add_graph)
        canvas.get_tk_widget().bind("<Button-4>", graphix.zoom_in)  
        canvas.get_tk_widget().bind("<Button-5>", graphix.zoom_out)  
        canvas.get_tk_widget().bind("<MouseWheel>", graphix.zoom) 
        if self.restarted==True:
            self.entry_boxes["Entry"+str(self.label_num)].insert(0,"Enter an Equation")
        self.entry_boxes["Entry"+str(self.label_num)].grid(sticky="w",row=self.label_num,column=1)
    def master_maker(self):
        club,row = "",""
        photo_list,textlocs,fracs = [],[],[]
        photo_num=0
        for images in os.listdir("image_dump"):
            photo_list.append(images)
        func=iterfuncs()
        for widget in self.frame_1.winfo_children():
            club = widget.grid_info()
            row = club["row"]
            if isinstance(widget,tk.Entry): 
                color = widget.cget("foreground")  
                self.master_boxes["Entry"+color+"_"+str(row)] = widget.get()
            elif isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child,tk.Text): 
                        tick =  replace.graball(child)
                        extratags = replace.set_tags(child)
                        text = func.replace_back(tick)
                        textlocs.append(text)
                        del extratags["sel"]
                        textlocs.append(extratags)
                        self.master_boxes["Text_"+str(row)] = textlocs
                    elif isinstance(child,tk.Frame):
                        for grandkid in child.winfo_children():
                            if isinstance(grandkid,tk.Entry):
                                fracs.append(grandkid.get())
                    fracs = []            
                    textlocs = []
                    
            elif isinstance(widget,tk.Label):
                self.master_boxes["Photo_"+str(row)] = "image_dump/photo_"+photo_list[photo_num]   
                photo_num+=1
    def create_new_state(self):
        photo_list = []
        self.master_boxes ={}
        
        new_state_name = filedialog.asksaveasfilename(
            initialdir="saved_states",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All Files", "*.*")],
            title="Create New State")
        if new_state_name:
            file_name = new_state_name.split("/")[-1]
            try:
                os.mkdir("image_files/"+file_name[:-5]) 
            except: 
                pass
        self
       
        self.master_boxes["Title"] = new_state_name.split("/")[-1][:-5]
        self.master_maker()
        for images in os.listdir("image_dump"):
            photo_list.append(images)
            try:
                shutil.move("image_dump/"+images,"image_files/"+file_name[:-5])
            except:
                pass
        for keys,values in self.master_boxes.items():
            if keys:
                pass
        leak = open(new_state_name,"w")
        json.dump(self.master_boxes,leak,indent=1)
        self.current_file = new_state_name
        self.reset_widgets()
        
       
    def reload_state(self):
        self.reset_widgets()
        self.restarted= False
        self.row_counter = 0
        self.label_num = -1
        old_state_name = filedialog.askopenfile(mode='r', filetypes=[("JSON files", "*.json")])
        dictims = json.load(old_state_name)
        n = 0
        for key,value in dictims.items():
            n+=1
            if "Title" in key:
                self.title(value)
                n -=1
            if "Entrygray1" in key:
                self.make_labels()
                self.entry_boxes["Entry"+str(n)].insert(0,value)
                self.entry_boxes["Entry"+str(n)].get()
            elif "Text" in key:
                self.make_new_entry()
                self.info_boxes["infobox"+str(n)].insert('1.0',value[0])
                replace.re_tag(self.info_boxes["infobox"+str(n)],value[1])
                list_strs = re.findall(r"\[\[.*?\]\]", self.info_boxes["infobox"+str(n)].get("1.0",tk.END))
                fr_strs = re.findall(r"/frac(\{.*?\}\{.*?\})", self.info_boxes["infobox"+str(n)].get("1.0",tk.END))
                check = newframe(self.info_boxes["infobox"+str(n)])
                for listr in list_strs:
                    neslist = ast.literal_eval(listr)
                    check.remove_matrix(neslist)
                for look in fr_strs:
                    ed1 = look.strip("}{")
                    ed2 = ed1.split("}{")
                    check.remove_frac(look,ed2)
            elif "Photo" in key:
                shutil.copy(value,"image_dump")
                try:
                    imager = Image.open(value)
                    image = imager.resize((600,500))
                    self.row_counter +=2 
                    placeholder = ImageTk.PhotoImage(image)
                    self.pic_boxes["picbox"+str(self.row_counter)] = tk.Label(self.frame_1, image=placeholder, bg="gray", width=placeholder.width(), height=placeholder.height())
                    self.pic_boxes["picbox"+str(self.row_counter)].image = placeholder
                    func = backend(self.pic_boxes["picbox"+str(self.row_counter)],self.row_counter)
                    func.imageshow()
                except Exception as e:
                    print(f"Error opening image: {e}")
            elif "Entrygray2" in key:
                self.create_graphs()
                self.entry_boxes["Entry"+str(n)].insert(0,value)
                n+=1
        
        self.restarted=True
    def reset_widgets(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.entry_boxes = {}
        self.infob_info = {}
        self.pic_boxes={}
    def on_closing(self):
        try:
            self.create_new_state()
        except:
            pass
        for file in os.listdir("image_dump"):
            os.remove("image_dump/"+file)
        self.is_closing = True  
        self.quit()
if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()