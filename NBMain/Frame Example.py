import tkinter as tk
from tkinter import scrolledtext

class DynamicFrameApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the Tk class
        self.title("Dynamic Frame Creator")
        self.geometry("800x600")

        # ScrolledText widget to hold dynamically created frames and bind the key event
        self.scrolled_text = scrolledtext.ScrolledText(self, width=100, height=30, wrap=tk.WORD)
        self.scrolled_text.pack(fill=tk.BOTH, expand=True)
        self.scrolled_text.bind('<KeyRelease>', self.process_key_release)

    def process_key_release(self, event):
        # Get the full content of the ScrolledText widget
        content = self.scrolled_text.get('1.0', 'end-1c')

        # Check for the dollar sign to trigger fraction creation
        if '$' in content:
            self.clear_and_create_fraction(content)

        # Check for the tilde sign to trigger matrix input creation
        if '~' in content:
            self.clear_and_create_matrix_input(content)

    def clear_and_create_fraction(self, content):
        """Clears the dollar sign '$' and creates a fraction frame."""
        # Find and remove the dollar sign from the content
        start_index = content.find('$')
        end_index = start_index + len('$')

        # Use character positions to clear the dollar sign from the ScrolledText widget
        self.scrolled_text.delete(f'1.0 + {start_index} chars', f'1.0 + {end_index} chars')

        # Create the fraction frame
        self.create_fraction_frame()

    def clear_and_create_matrix_input(self, content):
        """Clears the tilde '~' and creates an input box for matrix dimensions."""
        # Find and remove the tilde sign from the content
        start_index = content.find('~')
        end_index = start_index + len('~')

        # Use character positions to clear the tilde sign from the ScrolledText widget
        self.scrolled_text.delete(f'1.0 + {start_index} chars', f'1.0 + {end_index} chars')

        # Create an entry box for matrix dimensions
        self.create_matrix_input_box()

    def create_fraction_frame(self):
        # Create a new frame inside the ScrolledText widget for the fraction layout
        frame = tk.Frame(self.scrolled_text, bg='white', relief='solid')
        frame.pack()

        # Create the numerator Entry widget without borders
        numerator_entry = tk.Entry(frame, justify='center', bd=0, relief='flat', font=('Arial', 14))
        numerator_entry.pack(fill=tk.X, padx=20, pady=(5, 0))

        # Create the horizontal line to separate numerator and denominator
        separator = tk.Frame(frame, bg='black', height=2)
        separator.pack(fill=tk.X, padx=10, pady=2)

        # Create the denominator Entry widget without borders
        denominator_entry = tk.Entry(frame, justify='center', bd=0, relief='flat', font=('Arial', 14))
        denominator_entry.pack(fill=tk.X, padx=20, pady=(0, 5))

        # Embed the frame into the ScrolledText widget
        self.scrolled_text.window_create('end-1c', window=frame)
        self.scrolled_text.insert('end-1c', '\n')  # Add a newline for spacing

    def create_matrix_input_box(self):
        """Creates a box for entering matrix dimensions (x, y)."""
        input_frame = tk.Frame(self.scrolled_text)
        input_frame.pack(pady=5, padx=10)

        # Label for instructions
        #tk.Label(input_frame, text="Enter rows and columns:", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        # Entry widgets for x and y dimensions without borders
        rows_entry = tk.Entry(input_frame, width=3, justify='center', bd=0, relief='flat')
        rows_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(input_frame, text="x", font=('Arial', 10)).pack(side=tk.LEFT)
        cols_entry = tk.Entry(input_frame, width=3, justify='center', bd=0, relief='flat')
        cols_entry.pack(side=tk.LEFT, padx=2)

        def on_dimensions_entered(event=None):
            try:
                rows = int(rows_entry.get())
                cols = int(cols_entry.get())
                if 1 <= rows <= 20 and 1 <= cols <= 20:
                    input_frame.destroy()
                    self.create_matrix_frame(rows, cols)
                else:
                    tk.messagebox.showwarning("Warning", "Values must be between 1 and 20.")
            except ValueError:
                tk.messagebox.showwarning("Warning", "Please enter valid integers.")

        # Bind the entry boxes to trigger matrix creation when dimensions are entered
        rows_entry.bind('<Return>', on_dimensions_entered)
        cols_entry.bind('<Return>', on_dimensions_entered)

        # Embed the input frame into the ScrolledText widget
        self.scrolled_text.window_create('end-1c', window=input_frame)
        self.scrolled_text.insert('end-1c', '\n')

    def create_matrix_frame(self, rows, cols):
        # Create a new frame inside the ScrolledText widget for the matrix layout
        frame = tk.Frame(self.scrolled_text, bg='white', relief='solid', bd=1)
        frame.pack(pady=5, padx=10)

        # Draw the square brackets for the matrix
        bracket_frame_left = tk.Frame(frame)
        bracket_frame_left.grid(row=0, column=0, rowspan=rows + 2)

        # Create the left bracket
        tk.Label(bracket_frame_left, text="[", font=("Helvetica", 24)).pack(side=tk.TOP)

        matrix_frame = tk.Frame(frame)
        matrix_frame.grid(row=0, column=1)

        # Create the grid cells inside the matrix frame without borders
        for r in range(rows):
            for c in range(cols):
                cell = tk.Entry(matrix_frame, width=5, justify='center', bd=0, relief='flat')
                cell.grid(row=r, column=c, padx=2, pady=2)

        # Create the right bracket
        bracket_frame_right = tk.Frame(frame)
        bracket_frame_right.grid(row=0, column=2, rowspan=rows + 2)
        tk.Label(bracket_frame_right, text="]", font=("Helvetica", 24)).pack(side=tk.TOP)

        # Embed the frame into the ScrolledText widget
        self.scrolled_text.window_create('end-1c', window=frame)
        self.scrolled_text.insert('end-1c', '\n')  # Add a newline for spacing

# Instantiate and run the application
if __name__ == "__main__":
    app = DynamicFrameApp()
    app.mainloop()
