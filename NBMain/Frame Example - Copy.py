import tkinter as tk
from tkinter import scrolledtext

class FractionText(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create the ScrolledText widget
        self.scrolled_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, undo=True)
        self.scrolled_text.pack(fill=tk.BOTH, expand=True)

        # Create a frame to hold buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        # Create a button to print the last inserted fraction in the desired format
        self.print_fraction_button = tk.Button(button_frame, text="Print Last Fraction", command=self.print_last_fraction)
        self.print_fraction_button.pack(side=tk.LEFT, padx=5)

        # Create a button to print the entire ScrolledText content
        self.print_all_button = tk.Button(button_frame, text="Print All Content", command=self.print_all_content)
        self.print_all_button.pack(side=tk.LEFT, padx=5)

        # Store a reference to the last inserted fraction's numerator and denominator entries
        self.fractions = []

        # Bind the Enter key to check for the "/frac" command
        self.scrolled_text.bind("<Return>", self.check_for_fraction_command)

    def check_for_fraction_command(self, event):
        # Get the current position in the text widget
        current_position = self.scrolled_text.index(tk.INSERT)
        
        # Get the text before the current position to check for "/frac"
        text_before_cursor = self.scrolled_text.get("1.0", current_position).strip()

        # If the last word typed is "/frac", create the fraction frame
        if text_before_cursor.endswith("/frac"):
            # Remove the "/frac" text from the widget
            self.scrolled_text.delete(f"{current_position} linestart", current_position)

            # Create the fraction frame at the current position
            self.insert_fraction_frame()

            # Stop the Enter key from creating a new line
            return "break"

    def insert_fraction_frame(self):
        # Create a frame to hold the fraction parts
        fraction_frame = tk.Frame(self.scrolled_text)
        
        # Create the numerator entry
        numerator_entry = tk.Entry(fraction_frame, width=5, justify='center')
        numerator_entry.grid(row=0, column=0)

        # Create the separator (a label with a line or a slash)
        separator_label = tk.Label(fraction_frame, text="—")  # Use "/" if preferred
        separator_label.grid(row=1, column=0)

        # Create the denominator entry
        denominator_entry = tk.Entry(fraction_frame, width=5, justify='center')
        denominator_entry.grid(row=2, column=0)

        # Insert the fraction frame into the ScrolledText widget
        self.scrolled_text.window_create(tk.INSERT, window=fraction_frame)

        # Set focus to the numerator entry initially
        numerator_entry.focus_set()

        # Store the reference to the fraction entries for later use
        self.fractions.append((fraction_frame, numerator_entry, denominator_entry))

        # Bindings to shift focus between numerator and denominator using Up and Down keys
        numerator_entry.bind("<Down>", lambda event: denominator_entry.focus_set())
        denominator_entry.bind("<Up>", lambda event: numerator_entry.focus_set())

        # Binding to move to the next line in ScrolledText if Down key is pressed in denominator entry
        denominator_entry.bind("<Down>", self.move_to_next_line)

    def move_to_next_line(self, event):
        # Move the focus to the end of the current text in the ScrolledText widget
        self.scrolled_text.focus_set()
        self.scrolled_text.insert(tk.END, '\n')
        return "break"

    def print_last_fraction(self):
        # Print the last inserted fraction
        if self.fractions:
            _, numerator_entry, denominator_entry = self.fractions[-1]
            numerator = numerator_entry.get()
            denominator = denominator_entry.get()
            print(f"/frac{{{numerator}}}{{{denominator}}}")

    def print_all_content(self):
        # Initialize a variable to store the complete text content
        content = ""

        # Iterate through each character in the ScrolledText widget
        current_index = self.scrolled_text.index("1.0")
        end_index = self.scrolled_text.index(tk.END)

        while current_index != end_index:
            try:
                # Check if the character at the current index is associated with a window (widget)
                widget = self.scrolled_text.window_cget(current_index, "window")
            except tk.TclError:
                # If there is no widget at the current index, treat it as regular text
                widget = None

            if widget:
                # If the widget is a fraction frame, extract its numerator and denominator
                for fraction_frame, numerator_entry, denominator_entry in self.fractions:
                    if widget == str(fraction_frame):
                        numerator = numerator_entry.get()
                        denominator = denominator_entry.get()
                        content += f"/frac{{{numerator}}}{{{denominator}}} "
                        break
            else:
                # If it's regular text, add it to the content
                content += self.scrolled_text.get(current_index, f"{current_index} +1c")

            # Move to the next character in the ScrolledText widget
            current_index = self.scrolled_text.index(f"{current_index} +1c")

        print(content)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fraction Text Editor")

    fraction_text = FractionText(root)
    fraction_text.pack(fill=tk.BOTH, expand=True)

    root.geometry("600x400")
    root.mainloop()
