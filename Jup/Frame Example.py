import tkinter as tk
from tkinter import filedialog,messagebox,font, Tk,ttk,scrolledtext 
def aroundtwice(input1):
    used = input1.split(".")[1]
    use = int(used) -1
    result = str(input1.split(".")[0])+"."+str(use)
    return result
#print(aroundtwice("915.132"))
class Apps(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.notation = 0
        self.lastlen = 0 

        #self.title("No Save Loaded")
        self.geometry("600x400")
        #self.current_file = None
        self.main_canvas = tk.Canvas(self)
        self.main_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        
        self.frames = tk.Frame(self.main_canvas)
        self.main_canvas.create_window((4,4),window = self.frames,anchor="nw")
        self.textboxo = tk.Text(self.frames,height=2,font=("Helvetica",16))
        self.textboxo.grid(row=0,column=0)
        self.textboxo.bind("<Key>",self.delete_char)
        self.textboxo.bind("<KeyRelease>",self.change_font)
        self.textboxo.bind('<<Modified>>', self.check_for_special)
    def delete_char(self,event):
        content = event.widget.get("1.0", tk.END)
        if "^" in content: 
            self.notation=1
            #print(tk.INSERT)
            lp = event.widget.index(INSERT)
            print(event.char)
            event.widget.delete(aroundtwice(lp),lp)
        if "_" in content:
            self.notation -= 1
            event.widget.delete(f"{tk.END}-2c")

    def check_for_special(self,event=None):
        conversions = {
            '/sqrt': '√','/pi': 'π',
            '/theta': 'θ','/alpha': 'α','/beta': 'β','/gamma': 'γ','/delta': 'δ','/lambda':'λ',
            '/mu': 'μ','/omega': 'ω', '/int': '∫','/sum': '∑','/prod': '∏','/infty': '∞','/approx': '≈', 
            '/neq': '≠','/geq': '≥','/leq': '≤','/raw': '→', '/law': '←','/draw': '⇒','/dlaw': '⇐','/...': '…',
            '/sum_': '∑ₙ','/frac': '⁄','/cdot': '⋅','/times': '×','/div': '÷','/subset': '⊂','/supset': '⊃', 
            '/subseteq': '⊆', '/supseteq': '⊇','/cup': '∪','/cap': '∩','/forall': '∀', '/exists': '∃',      
            '/nabla': '∇','/Alpha': 'Α','/Beta': 'Β','/Gamma': 'Γ','/Delta': 'Δ','/Epsilon': 'Ε',
            '/Zeta': 'Ζ','/Eta': 'Η','/Theta': 'Θ','/Iota': 'Ι','/Kappa': 'Κ','/Lambda': 'Λ',          
            '/Mu': 'Μ','/Xi': 'Ξ','/Omicron': 'Ο','/Pi': 'Π','/Rho': 'Ρ',             
            '/Sigma': 'Σ','/Tau': 'Τ','/Upsilon': 'Υ','/Phi': 'Φ','/Chi': 'Χ','/Psi': 'Ψ',             
            '/Omega': 'Ω'}
        if event.widget.edit_modified():
            event.widget.edit_modified(False)
            for word_to_replace,replacement_word in conversions.items():
                start_pos = '1.0'  # Start searching from the beginning for each word
                replace_lambda = lambda start_pos: (event.widget.search(word_to_replace, start_pos, stopindex=tk.END))
            
                while True:
                # Use the lambda to search for the word
                    start_pos = replace_lambda(start_pos)
                
                    if not start_pos:
                        break  # Exit if no more words are found
                
                    end_pos = f"{start_pos}+{len(word_to_replace)}c"
                
                # Delete the found word
                    event.widget.delete(start_pos, end_pos)
                    event.widget.insert(start_pos, replacement_word)
                    start_pos = end_pos
        
    def change_font(self,event):
        content = event.widget.get("1.0", tk.END)

        if self.notation ==1:                
            event.widget.tag_configure("superscript", offset=8, font=("Helvetica", 10))
            event.widget.tag_add("superscript", f"{tk.END}-2c")
        if self.notation == -1:
            event.widget.tag_configure("subscript", offset=-4, font=("Helvetica", 10))
            event.widget.tag_add("subscript", f"{tk.END}-2c")


if __name__ == "__main__":
    apps = Apps()
    apps.mainloop()