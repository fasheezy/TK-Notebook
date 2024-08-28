import tkinter as tk
import json
import os
from tkinter import filedialog, messagebox,font,Tk
from sympy import sympify, SympifyError

class EquationEditorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Main window configuration
        self.title("Equation Box Creator with Auto-Calculation")
        self.geometry("600x400")
        self.defaultFont = font.nametofont("TkDefaultFont") 
        self.defaultFont.configure(family="Times New Roman") 
        # Variables to track state
        self.current_file = None  # To track the current file
        self.save_directory = "saved_states"  # Directory to save states
        self.equation_boxes = []  # List to track equation boxes for saving/loading
        # Ensure the save directory exists
        os.makedirs(self.save_directory, exist_ok=True)

        # Setup the scrollable frame
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", self.on_configure)
        self.second_frame = tk.Frame(self.canvas) 
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Show the initial menu with saved states
        self.show_initial_menu()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_initial_menu(self):
 
        # Clear the grid and reset the row counter
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.row_counter = 2

        # List saved state files as buttons
     #   state_files = [f for f in os.listdir(self.save_directory) if f.endswith(".json")]
        #for state_file in state_files:
         #   button = tk.Button(self.scrollable_frame, text=state_file,
                              # command=lambda sf=state_file: self.load_state(os.path.join(self.save_directory, sf)))
          #  button.grid(row=self.row_counter, column=0, pady=5, padx=5, sticky="ew")
           # self.row_counter += 1

        # Button to create a new state
        self.create_new_button = tk.Button(self.scrollable_frame, text="Create New State", command=self.create_new_state)
        
       # self.row_counter += 1

        # Button to create a customizable equation box
       # self.create_equation_button = tk.Button(self.scrollable_frame, text="Create Equation Box", command=self.create_equation_box)
       # self.create_equation_button.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
       # self.row_counter += 1
        self.clear_and_setup_widgets()
        self.uber_label = tk.Label(self.scrollable_frame,text="Select list of States")
        self.uber_label.grid(row=0,column=0)
        self.show_states = tk.Listbox(self.scrollable_frame)
        self.show_states.delete(0,tk.END)
        for i in os.listdir("saved_states"):
            self.show_states.insert(tk.END,i)
        self.show_states.grid(row=1,column=0)
        self.create_new_button.grid(row=3, column=0, pady=10, padx=5, sticky="ew")
    def show_previous_states(self):
        self.place_frame
        self.create_new_button.grid_forget()
        self.create_equation_button.grid_forget()
        self.show_states = tk.Listbox(self.scrollable_frame)
        self.show_states.delete(0,tk.END)
        for i in os.listdir("saved_states"):
            self.show_states.insert(tk.END,i)
        self.show_states.grid(row=0,column=3)
        self.back
    def show_main_menu(self):
        self.create_equation_button = tk.Button(self.scrollable_frame, text="Create Equation Box", command=self.create_equation_box)
        self.create_equation_button.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
        self.row_counter += 1

        self.create_new_button = tk.Button(self.scrollable_frame, text="Create New State", command=self.create_new_state)
        self.create_new_button.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
    def create_new_state(self):
        # Prompt for a new state name
        new_state_name = filedialog.asksaveasfilename(initialdir=self.save_directory,defaultextension=".json",filetypes=[("json", "*.json"), ("All Files", "*.*")],title="Create New State")
        if new_state_name:
            # Initialize a new state
            self.current_file = new_state_name
            self.clear_and_setup_widgets()

    def clear_and_setup_widgets(self):
        # Clear the grid and reset the row counter
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.row_counter = 0
        self.equation_boxes = []  # Reset equation boxes

        # Add buttons for adding more widgets, saving state, and going back to menu
        self.add_button_btn = tk.Button(self.scrollable_frame, text="Add Button", command=self.add_button)
        self.add_entry_btn = tk.Button(self.scrollable_frame, text="Add Entry Box", command=self.add_entry)
        self.save_btn = tk.Button(self.scrollable_frame, text="Save State", command=self.save_state)
        self.back_btn = tk.Button(self.scrollable_frame, text="Back to Menu", command=self.show_initial_menu)

        self.add_button_btn.grid(row=self.row_counter, column=1, pady=10, padx=5, sticky="ew")
        self.row_counter += 1
        self.add_entry_btn.grid(row=self.row_counter, column=1, pady=10, padx=5, sticky="ew")
        self.row_counter += 1
        self.save_btn.grid(row=3, column=0, pady=10, padx=5, sticky="ew")
        self.row_counter += 1
        self.back_btn.grid(row=self.row_counter, column=1, pady=10, padx=5, sticky="ew")
        self.row_counter += 1

    def save_state(self):
        if self.current_file:
            state = {
                "equation_boxes": [eq_box.get("1.0", tk.END).strip() for eq_box in self.equation_boxes]
            }
            with open(self.current_file, "w") as file:
                json.dump(state, file)
            messagebox.showinfo("Success", f"State saved to {self.current_file}")

    def load_state(self, filename):
        try:
            with open(filename, "r") as file:
                state = json.load(file)
                self.current_file = filename
                self.clear_and_setup_widgets()

                # Load equation boxes
                for equation in state.get("equation_boxes", []):
                    self.create_equation_box(equation)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def on_closing(self):
        if self.current_file:
            self.save_state()
        self.destroy()

    def add_button(self):
        # Dynamically add a new button
        new_button = tk.Button(self.scrollable_frame, text="New Button")
        new_button.grid(row=self.row_counter, column=1, pady=5, padx=5, sticky="ew")
        self.row_counter += 1

    def add_entry(self):
        # Dynamically add a new Entry box
        new_entry = tk.Entry(self.scrollable_frame)
        new_entry.grid(row=self.row_counter, column=1, pady=5, padx=5, sticky="ew")
        self.row_counter += 1

    def create_equation_box(self, initial_text=""):
        # Create an input box for the equation
        equation_input = tk.Text(self.scrollable_frame, height=2, font=('Arial', 14))
        equation_input.grid(row=self.row_counter, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        equation_input.insert(tk.END, initial_text)

        # Bind key release to render and calculate the equation as the user types
        equation_input.bind("<KeyRelease>", lambda event, eq_input=equation_input: self.render_and_calculate(eq_input))

        # Create a label to display the rendered equation and the result
        rendered_label = tk.Label(self.scrollable_frame, text="", font=('Arial', 14), anchor="w", justify="left")
        rendered_label.grid(row=self.row_counter + 1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.equation_boxes.append(equation_input)

        self.row_counter += 2

        # Add a button to go back to the menu
        back_button = tk.Button(self.scrollable_frame, text="Back to Menu", command=self.show_initial_menu)
        back_button.grid(row=self.row_counter, column=0, columnspan=3, pady=10, padx=5, sticky="ew")
        self.row_counter += 1

        # Initial render
        self.render_and_calculate(equation_input)

    def render_and_calculate(self, equation_input):
        # Get the input text (equation in simple notation)
        equation_text = equation_input.get("1.0", tk.END).strip()
        
        # Render the equation visually
        rendered_text = self.convert_to_markdown(equation_text)
        
        # Calculate the result
        result_text = self.calculate_equation(equation_text)
        
        # Display the rendered equation and the result
        final_output = f"{rendered_text} = {result_text}"
        rendered_label = equation_input.grid_info()["row"] + 1  # Row after the input box
        for widget in self.scrollable_frame.grid_slaves(row=rendered_label):
            if isinstance(widget, tk.Label):
                widget.config(text=final_output, anchor="w", justify="left")
                break

    def convert_to_markdown(self, text):
        # Basic conversion of text to simulate markdown rendering, e.g., superscripts and subscripts
        text = text.replace("^", "ⁿ")  # Simple superscript, e.g., e^x -> eⁿx (basic, non-comprehensive)
        text = text.replace("_", "ₙ")  # Simple subscript, e.g., x_2 -> xₙ (basic, non-comprehensive)
        return text

    def calculate_equation(self, text):
        try:
            # Using sympy to safely evaluate the equation
            result = sympify(text)
            return result
        except SympifyError:
            return "Invalid equation"

if __name__ == "__main__":
    app = EquationEditorApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
