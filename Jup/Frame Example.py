import tkinter as tk
from tkinter import ttk

def on_button_click():
    print("Button clicked!")

root = tk.Tk()
root.title("Scrollable Frame with Fixed Buttons")

# Create a frame for the always-visible buttons on the left
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add buttons to the button frame, aligned vertically
button1 = tk.Button(button_frame, text="Button 1", command=on_button_click)
button1.pack(padx=5, pady=5, anchor='w')

button2 = tk.Button(button_frame, text="Button 2", command=on_button_click)
button2.pack(padx=5, pady=5, anchor='w')

button3 = tk.Button(button_frame, text="Button 3", command=on_button_click)
button3.pack(padx=5, pady=5, anchor='w')

# Create a canvas for the scrollable content
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the scrollable content
scrollable_frame = tk.Frame(canvas)

# Create a window in the canvas to hold the scrollable frame
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Ensure the scrollable frame expands with the window size
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Add content to the scrollable frame
for i in range(20):
    tk.Label(scrollable_frame, text=f"Label {i+1}").pack(pady=5, padx=5)

# Start the Tkinter event loop
root.mainloop()
