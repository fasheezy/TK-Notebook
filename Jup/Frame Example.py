import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Separate Grids Example")

# Create the frame for the Listbox
listbox_frame = tk.Frame(root)
listbox_frame.grid(row=0, column=0, sticky="nsew")

# Create a Listbox widget inside listbox_frame
listbox = tk.Listbox(listbox_frame, width=40, height=20)
listbox.pack(fill="both", expand=True)

# Add some items to the Listbox
for i in range(100):
    listbox.insert(tk.END, f"Item {i+1}")

# Create the frame for the buttons
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=0, column=1, sticky="nsew")

# Create a few buttons inside buttons_frame
button1 = tk.Button(buttons_frame, text="Button 1")
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = tk.Button(buttons_frame, text="Button 2")
button2.grid(row=1, column=0, padx=5, pady=5)

button3 = tk.Button(buttons_frame, text="Button 3")
button3.grid(row=2, column=0, padx=5, pady=5)

# Configure grid weights for resizing
root.grid_columnconfigure(0, weight=1)  # Listbox frame will expand
root.grid_columnconfigure(1, weight=0)  # Buttons frame will stay compact
root.grid_rowconfigure(0, weight=1)

# Run the Tkinter main loop
root.mainloop()
