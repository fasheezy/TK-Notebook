import tkinter as tk
import json
import os
from tkinter import filedialog, messagebox
from sympy import sympify, SympifyError, symbols

class EquationEditorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Main window configuration
        self.title("Dynamic Equation Editor")
        self.geometry("600x600")
        
        # Variables to track state
        self.current_file = None  # To track the current file
        self.save_directory = "saved_states"  # Directory to save states
        self.equation_boxes = []  # List to track equation boxes for saving/loading
        self.variables = {}  # Dictionary to track variable values

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

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Show the initial menu with saved states
        self.show_initial_menu()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_initial_menu(self):
        # Clear the grid and reset the row counter
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.row_counter = 0

        # List saved state files as buttons
        state_files = [f for f in os.listdir(self.save_directory) if f.endswith(".myappstate")]
        for state_file in state_files:
            button = tk.Button(self.scrollable_frame, text=state_file,
                               command=lambda sf=state_file: self.load_state(os.path.join(self.save_directory, sf)))
            button.grid(row=self.row_counter, column=0, pady=5, padx=5, sticky="ew")
            self.row_counter += 1

        # Button to create a new state
        create_new_button = tk.Button(self.scrollable_frame, text="Create New State", command=self.create_new_state)
        create_new_button.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
        self.row_counter += 1

        # Create the first equation box (modifiable dynamically based on equals sign)
        self.create_dynamic_equation_box()

    def create_new_state(self):
        # Prompt for a new state name
        new_state_name = filedialog.asksaveasfilename(
            initialdir=self.save_directory,
            defaultextension=".myappstate",
            filetypes=[("App State Files", "*.myappstate"), ("All Files", "*.*")],
            title="Create New State"
        )
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
        self.variables = {}  # Reset variables

        # Add buttons for adding more widgets, saving state, and going back to menu
        self.add_variable_btn = tk.Button(self.scrollable_frame, text="Add Variable", command=self.add_variable)
        self.save_btn = tk.Button(self.scrollable_frame, text="Save State", command=self.save_state)
        self.back_btn = tk.Button(self.scrollable_frame, text="Back to Menu", command=self.show_initial_menu)

        self.add_variable_btn.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
        self.row_counter += 1
        self.save_btn.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
        self.row_counter += 1
        self.back_btn.grid(row=self.row_counter, column=0, pady=10, padx=5, sticky="ew")
        self.row_counter += 1

        # Add the first dynamic equation box
        self.create_dynamic_equation_box()

    def create_dynamic_equation_box(self, initial_text=""):
        # Create an input box for the equation
        equation_input = tk.Text(self.scrollable_frame, height=2, font=('Arial', 14))
        equation_input.grid(row=self.row_counter, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        equation_input.insert(tk.END, initial_text)

        # Bind key release to dynamically handle the equation based on equals sign
        equation_input.bind("<KeyRelease>", lambda event, eq_input=equation_input: self.handle_dynamic_equation(eq_input))

        # Create a label to display the rendered equation and the result
        rendered_label = tk.Label(self.scrollable_frame, text="", font=('Arial', 14), anchor="w", justify="left")
        rendered_label.grid(row=self.row_counter + 1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.equation_boxes.append(equation_input)

        self.row_counter += 2

    def handle_dynamic_equation(self, equation_input):
        # Get the full input text
        equation_text = equation_input.get("1.0", tk.END).strip()

        # Check if the equation contains an equals sign
        if "=" in equation_text:
            lhs_text, rhs_text = equation_text.split("=", 1)
            self.render_and_calculate_double(lhs_text.strip(), rhs_text.strip(), equation_input)
        else:
            self.render_and_calculate(equation_input)

    def render_and_calculate(self, equation_input):
        # Get the input text (equation in simple notation)
        equation_text = equation_input.get("1.0", tk.END).strip()
        
        # Render the equation visually
        rendered_text = self.convert_to_markdown(equation_text)
        
        # Calculate the result, considering the variables
        result_text = self.calculate_equation(equation_text)
        
        # Display the rendered equation and the result
        final_output = f"{rendered_text} = {result_text}"
        rendered_label = equation_input.grid_info()["row"] + 1  # Row after the input box
        for widget in self.scrollable_frame.grid_slaves(row=rendered_label):
            if isinstance(widget, tk.Label):
                widget.config(text=final_output, anchor="w", justify="left")
                break

    def render_and_calculate_double(self, lhs_text, rhs_text, equation_input):
        # Render the equation visually
        lhs_rendered = self.convert_to_markdown(lhs_text)
        rhs_rendered = self.convert_to_markdown(rhs_text)

        # Calculate the LHS and RHS, considering the variables
        lhs_result = self.calculate_equation(lhs_text)
        rhs_result = self.calculate_equation(rhs_text)
        
        # Display the rendered LHS, RHS, and their results
        final_output = f"{lhs_rendered} = {lhs_result}    =    {rhs_rendered} = {rhs_result}"
        rendered_label = equation_input.grid_info()["row"] + 1  # Row after the input box
        for widget in self.scrollable_frame.grid_slaves(row=rendered_label):
            if isinstance(widget, tk.Label):
                widget.config(text=final_output, anchor="w", justify="left")
                break

    def add_variable(self, var_name=None, var_value=None):
        # Add a new variable input field
        var_name = var_name or f"var{len(self.variables) + 1}"
        var_label = tk.Label(self.scrollable_frame, text=f"{var_name} =")
        var_label.grid(row=self.row_counter, column=0, pady=5, padx=5, sticky="w")

        var_entry = tk.Entry(self.scrollable_frame)
        var_entry.grid(row=self.row_counter, column=1, pady=5, padx=5, sticky="ew")
        if var_value is not None:
            var_entry.insert(0, var_value)
        
        self.variables[var_name] = var_entry.get()

        var_entry.bind("<KeyRelease>", lambda event, name=var_name: self.update_variable(name, var_entry.get()))

        self.row_counter += 1

    def update_variable(self, var_name, var_value):
        # Update the variable dictionary
        self.variables[var_name] = var_value
        # Recalculate all equations
        for eq_box in self.equation_boxes:
            self.handle_dynamic_equation(eq_box)

    def convert_to_markdown(self, text):
        # Converts simple markdown-like text to a more visually represented string.
        # Supports Greek letters, basic and advanced mathematical symbols, etc.
        conversions = {
            '^': 'ⁿ',             # Superscript placeholder
            '_': 'ₙ',             # Subscript placeholder
            '**': '𝒃',            # Bold placeholder
            '*': '𝒊',             # Italic placeholder
            '~~': '̶',            # Strikethrough placeholder
            'sqrt': '√',          # Square root
            'pi': 'π',            # Pi
            'theta': 'θ',         # Theta
            'alpha': 'α',         # Alpha
            'beta': 'β',          # Beta
            'gamma': 'γ',         # Gamma
            'delta': 'δ',         # Delta
            'lambda': 'λ',        # Lambda
            'mu': 'μ',            # Mu
            'omega': 'ω',         # Omega
            'int': '∫',           # Integral
            'sum': '∑',           # Summation
            'prod': '∏',          # Product
            'infty': '∞',         # Infinity
            'approx': '≈',        # Approximation
            '!=': '≠',            # Not equal
            '>=': '≥',            # Greater than or equal
            '<=': '≤',            # Less than or equal
            '->': '→',            # Right arrow
            '<-': '←',            # Left arrow
            '=>': '⇒',            # Double right arrow
            '<=': '⇐',            # Double left arrow
            '...': '…',           # Ellipsis
            'sum_': '∑ₙ',         # Summation with subscript placeholder
            'sqrt(': '√(',        # Square root with parenthesis for expression
            'int_': '∫ₙ',         # Integral with subscript placeholder
            'lim': 'lim',         # Limit
            'lim_': 'limₙ',       # Limit with subscript placeholder
            'sin': 'sin',         # Sine function
            'cos': 'cos',         # Cosine function
            'tan': 'tan',         # Tangent function
            'log': 'log',         # Logarithm
            'ln': 'ln',           # Natural logarithm
            'exp': 'exp',         # Exponential function
            'frac': '⁄',          # Fraction
            'cdot': '⋅',          # Dot product
            'times': '×',         # Multiplication symbol
            'div': '÷',           # Division symbol
            'leq': '≤',           # Less than or equal
            'geq': '≥',           # Greater than or equal
            'neq': '≠',           # Not equal to
            'subset': '⊂',        # Subset
            'supset': '⊃',        # Superset
            'subseteq': '⊆',      # Subset or equal
            'supseteq': '⊇',      # Superset or equal
            'cup': '∪',           # Union
            'cap': '∩',           # Intersection
            'forall': '∀',        # For all
            'exists': '∃',        # There exists
            'nabla': '∇',         # Nabla (gradient)

            # Uppercase Greek Letters
            'Alpha': 'Α',           # Alpha
            'Beta': 'Β',            # Beta
            'Gamma': 'Γ',           # Gamma
            'Delta': 'Δ',           # Delta
            'Epsilon': 'Ε',         # Epsilon
            'Zeta': 'Ζ',            # Zeta
            'Eta': 'Η',             # Eta
            'Theta': 'Θ',           # Theta
            'Iota': 'Ι',            # Iota
            'Kappa': 'Κ',           # Kappa
            'Lambda': 'Λ',          # Lambda
            'Mu': 'Μ',              # Mu
            'Nu': 'Ν',              # Nu
            'Xi': 'Ξ',              # Xi
            'Omicron': 'Ο',         # Omicron
            'Pi': 'Π',              # Pi
            'Rho': 'Ρ',             # Rho
            'Sigma': 'Σ',           # Sigma
            'Tau': 'Τ',             # Tau
            'Upsilon': 'Υ',         # Upsilon
            'Phi': 'Φ',             # Phi
            'Chi': 'Χ',             # Chi
            'Psi': 'Ψ',             # Psi
            'Omega': 'Ω',           # Omega
        }
        
        for key, value in conversions.items():
            text = text.replace(key, value)
        
        return text

    def calculate_equation(self, text):
        try:
            # Use sympy to safely evaluate the equation with substituted variables
            expr = sympify(text)
            if self.variables:
                # Substitute variable values if provided
                expr = expr.subs(self.variables)
            return expr
        except SympifyError:
            return "Invalid equation"
    def on_closing(self):
        self.destroy()
        
if __name__ == "__main__":
    app = EquationEditorApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
