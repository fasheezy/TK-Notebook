import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from multiprocessing import Process, Pool, Queue
import zipfile
import time

class DirectoryColumn:
    """Represents a column in the UI displaying a directory and its files."""

    def __init__(self, master, title, directory_path, show_files_var, update_callback, drop_callback):
        self.master = master
        self.directory_path = directory_path
        self.show_files_var = show_files_var
        self.update_callback = update_callback
        self.drop_callback = drop_callback

        # Root frame for the column
        self.frame = ttk.Frame(master, width=300)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=10)

        # Title label
        self.label = ttk.Label(self.frame, text=title)
        self.label.pack(pady=5)

        # Root directory label
        self.root_label = ttk.Label(self.frame, text="Root Directory: None")
        self.root_label.pack(pady=5)

        # File count label
        self.file_count_label = ttk.Label(self.frame, text="Files: 0")
        self.file_count_label.pack(pady=5)

        # Show/Hide files button
        self.toggle_button = ttk.Checkbutton(self.frame, text="Show/Hide Files", variable=self.show_files_var, command=self.toggle_files)
        self.toggle_button.pack(pady=5)

        # Frame to hold the listbox
        self.listbox_frame = ttk.Frame(self.frame, height=150)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox to display files
        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Invisible placeholder frame
        self.placeholder = ttk.Frame(self.listbox_frame, height=150)

        # Additional buttons
        self.additional_buttons = []

        # Clear button
        self.clear_button = ttk.Button(self.frame, text=f"Clear {title}", command=self.clear_directory)
        self.clear_button.pack(pady=5)

        # Drag and drop functionality
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_callback)

    def add_additional_button(self, text, command):
        """Add additional button specific to a column (like Rename or Zip)."""
        button = ttk.Button(self.frame, text=text, command=command)
        self.additional_buttons.append(button)
        button.pack(pady=5)

    def toggle_files(self):
        """Toggle the visibility of the file list."""
        if self.show_files_var.get():
            self.placeholder.pack_forget()
            self.listbox.pack(fill=tk.BOTH, expand=True)
        else:
            self.listbox.pack_forget()
            self.placeholder.pack(fill=tk.BOTH, expand=True)

    def update_listbox(self, files):
        """Update the listbox with the given list of files."""
        self.listbox.delete(0, tk.END)
        if files:  # Check if the list is not empty
            for file in files:
                self.listbox.insert(tk.END, file)
        self.update_file_count(len(files))

    def set_root_directory(self, root_dir):
        """Set the root directory label."""
        self.root_label.config(text=f"Root Directory: {root_dir}")

    def clear_directory(self):
        """Clear the directory and update the listbox."""
        self.update_callback(self.directory_path)
        self.root_label.config(text="Root Directory: None")
        self.update_listbox([])

    def update_file_count(self, count):
        """Update the file count label."""
        self.file_count_label.config(text=f"Files: {count}")

class FileMonitorProcess(Process):
    """A process that monitors a directory and sends file updates to a queue."""

    def __init__(self, directory, queue):
        super().__init__()
        self.directory = directory
        self.queue = queue

    def run(self):
        """Continuously monitor the directory and send updates to the queue."""
        previous_files = []
        while True:
            if os.path.exists(self.directory):
                current_files = self.list_files(self.directory)
                if current_files != previous_files:
                    self.queue.put((self.directory, current_files))
                    previous_files = current_files
            time.sleep(1)  # Adjust the sleep time as needed

    def list_files(self, directory):
        """List files in the specified directory."""
        return [os.path.relpath(os.path.join(root, file), directory)
                for root, dirs, files in os.walk(directory)
                for file in files]

class RenameSettingsFrame(ttk.Frame):
    """Settings frame for renaming output files."""

    def __init__(self, master, back_callback, update_prefix_callback, names):
        super().__init__(master)
        self.back_callback = back_callback
        self.update_prefix_callback = update_prefix_callback
        self.names = names
        self.current_index = 0
        self.file_counts = {name: 0 for name in names}
        self.special_chars_visible = False
        self.prefix_placeholder = "Enter prefix"
        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the rename settings frame."""
        label = ttk.Label(self, text="Rename Settings", font=("Helvetica", 16))
        label.pack(pady=10)

        # Prefix entry customization
        self.prefix_label = ttk.Label(self, text="File Name Prefix:")
        self.prefix_label.pack(pady=5)

        self.prefix_entry = ttk.Entry(self, foreground='grey')
        self.prefix_entry.insert(0, self.prefix_placeholder)
        self.prefix_entry.pack(pady=5)

        # Bind events to handle placeholder behavior
        self.prefix_entry.bind("<FocusIn>", self.clear_placeholder)
        self.prefix_entry.bind("<FocusOut>", self.add_placeholder)
        self.prefix_entry.bind("<Return>", self.save_prefix)

        # Label for displaying "Text entered" message
        self.message_label = ttk.Label(self, text="", font=("Helvetica", 12))
        self.message_label.pack(pady=5)

        # Special characters button
        self.special_char_button = ttk.Button(self, text="Special Characters", command=self.toggle_special_chars)
        self.special_char_button.pack(pady=10)

        # Special characters frame
        self.special_chars_frame = ttk.Frame(self)
        self.special_chars_buttons = []
        special_chars = ['@', '#', '$', '%', '&', '_', '-', '+', '=']
        for char in special_chars:
            btn = ttk.Button(self.special_chars_frame, text=char, command=lambda c=char: self.insert_special_char(c))
            self.special_chars_buttons.append(btn)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Hide the special characters initially
        self.special_chars_frame.pack_forget()

        # Navigation and count adjustment section
        self.name_label = ttk.Label(self, text=self.names[self.current_index], font=("Helvetica", 16))
        self.name_label.pack(pady=10)

        self.file_count_label = ttk.Label(self, text=f"Files: {self.file_counts[self.names[self.current_index]]}", font=("Helvetica", 14))
        self.file_count_label.pack(pady=10)

        self.previous_button = ttk.Button(self, text="Previous", command=self.show_previous_name)
        self.previous_button.pack(side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(self, text="Next", command=self.show_next_name)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.decrease_button = ttk.Button(self, text="-", command=self.decrease_file_count)
        self.decrease_button.pack(side=tk.LEFT, padx=10)

        self.increase_button = ttk.Button(self, text="+", command=self.increase_file_count)
        self.increase_button.pack(side=tk.LEFT, padx=10)

        back_button = ttk.Button(self, text="Back", command=self.back_callback)
        back_button.pack(pady=20)

7

    def save_prefix(self, event=None):
        """Save the prefix customization when the Return key is pressed."""
        prefix = self.prefix_entry.get()
        if prefix != self.prefix_placeholder:  # Ensure it's not the placeholder text
            self.update_prefix_callback(prefix)
            self.prefix_entry.delete(0, tk.END)  # Clear the entry box
            self.message_label.config(text="Text entered")
            self.after(2000, self.clear_message)  # Clear the message after 2 seconds

    def clear_message(self):
        """Clear the 'Text entered' message."""
        self.message_label.config(text="")

    def toggle_special_chars(self):
        """Toggle the visibility of special character buttons."""
        if self.special_chars_visible:
            self.special_chars_frame.pack_forget()
        else:
            self.special_chars_frame.pack(pady=10)
        self.special_chars_visible = not self.special_chars_visible

    def insert_special_char(self, char):
        """Insert a special character into the prefix entry."""
        current_text = self.prefix_entry.get()
        if current_text == self.prefix_placeholder:
            self.prefix_entry.delete(0, tk.END)
            self.prefix_entry.config(foreground='black')
            current_text = ''
        self.prefix_entry.insert(tk.END, current_text + char)

    def show_previous_name(self):
        """Navigate to the previous name in the list."""
        self.current_index = (self.current_index - 1) % len(self.names)
        self.update_displayed_name()

    def show_next_name(self):
        """Navigate to the next name in the list."""
        self.current_index = (self.current_index + 1) % len(self.names)
        self.update_displayed_name()

    def increase_file_count(self):
        """Increase the file count for the current name."""
        self.file_counts[self.names[self.current_index]] += 1
        self.update_file_count_label()

    def decrease_file_count(self):
        """Decrease the file count for the current name."""
        if self.file_counts[self.names[self.current_index]] > 0:
            self.file_counts[self.names[self.current_index]] -= 1
            self.update_file_count_label()

    def update_displayed_name(self):
        """Update the name label and file count label."""
        self.name_label.config(text=self.names[self.current_index])
        self.update_file_count_label()

    def update_file_count_label(self):
        """Update the file count label."""
        self.file_count_label.config(text=f"Files: {self.file_counts[self.names[self.current_index]]}")

class ZipSettingsFrame(ttk.Frame):
    """Settings frame for zip output files."""

    def __init__(self, master, back_callback, update_cluster_callback):
        super().__init__(master)
        self.back_callback = back_callback
        self.update_cluster_callback = update_cluster_callback
        self.extra_settings_visible = False  # State to track visibility of extra settings
        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the zip settings frame."""
        label = ttk.Label(self, text="Zip Settings", font=("Helvetica", 16))
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Cluster size customization
        self.cluster_label = ttk.Label(self, text="Files per Cluster:")
        self.cluster_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.cluster_entry = ttk.Entry(self)
        self.cluster_entry.grid(row=1, column=1, padx=10, pady=5)
        self.cluster_button = ttk.Button(self, text="Save Cluster Size", command=self.save_cluster_size)
        self.cluster_button.grid(row=1, column=2, padx=10, pady=5)

        # Extra settings button
        self.extra_settings_button = ttk.Button(self, text="Extra Settings", command=self.toggle_extra_settings)
        self.extra_settings_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Extra settings frame (initially hidden)
        self.extra_settings_frame = ttk.Frame(self)
        self.extra_settings_frame.grid(row=0, column=3, rowspan=10, padx=10, pady=10, sticky="ns")

        # Add detailed extra settings
        self.nesting_label = ttk.Label(self.extra_settings_frame, text="Select Nesting Type:")
        self.nesting_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nesting_var = tk.StringVar(value="Flat")
        flat_option = ttk.Radiobutton(self.extra_settings_frame, text="Flat", variable=self.nesting_var, value="Flat")
        nested_option = ttk.Radiobutton(self.extra_settings_frame, text="Nested", variable=self.nesting_var, value="Nested")
        flat_option.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        nested_option.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.compression_label = ttk.Label(self.extra_settings_frame, text="Compression Level:")
        self.compression_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.compression_var = tk.StringVar(value="Normal")
        normal_option = ttk.Radiobutton(self.extra_settings_frame, text="Normal", variable=self.compression_var, value="Normal")
        high_option = ttk.Radiobutton(self.extra_settings_frame, text="High", variable=self.compression_var, value="High")
        low_option = ttk.Radiobutton(self.extra_settings_frame, text="Low", variable=self.compression_var, value="Low")
        normal_option.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        high_option.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        low_option.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.save_nesting_button = ttk.Button(self.extra_settings_frame, text="Save Settings", command=self.save_extra_settings)
        self.save_nesting_button.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        # Hide the extra settings initially
        self.extra_settings_frame.grid_remove()

        back_button = ttk.Button(self, text="Back", command=self.back_callback)
        back_button.grid(row=8, column=0, padx=10, pady=20, sticky="w")

    def save_cluster_size(self):
        """Save the cluster size customization."""
        try:
            cluster_size = int(self.cluster_entry.get())
            self.update_cluster_callback(cluster_size)
        except ValueError:
            print("Invalid cluster size. Please enter an integer.")

    def toggle_extra_settings(self):
        """Toggle the visibility of the extra settings frame."""
        if self.extra_settings_visible:
            self.extra_settings_frame.grid_remove()
        else:
            self.extra_settings_frame.grid()
        self.extra_settings_visible = not self.extra_settings_visible

    def save_extra_settings(self):
        """Save the selected extra settings."""
        nesting_type = self.nesting_var.get()
        compression_level = self.compression_var.get()
        print(f"Nesting type: {nesting_type}, Compression level: {compression_level}")  # Placeholder for actual functionality

def rename_file(old_path, new_path):
    """Renames a single file."""
    os.rename(old_path, new_path)

def prepare_rename_arguments(directory, prefix):
    """Prepare the list of tuples for renaming files."""
    arguments = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            old_path = os.path.join(root, file)
            new_name = f"{prefix}_{file}"
            new_path = os.path.join(root, new_name)
            arguments.append((old_path, new_path))
    return arguments

def rename_files_in_parallel(directory, prefix):
    """Renames files in the directory in parallel using starmap."""
    arguments = prepare_rename_arguments(directory, prefix)
    
    with Pool() as pool:
        pool.starmap(rename_file, arguments)

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Three Column Example")
        self.geometry("1200x500")

        # Queue for inter-process communication
        self.queue = Queue()

        # Main container for columns
        self.main_container = ttk.Frame(self)
        self.main_container.grid(row=0, column=1, padx=20, pady=10)

        # Empty columns for spacing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Directories (define, and ensure they start empty)
        self.input_directory = "input_files"
        self.renamed_directory = "renamed_files"
        self.zipped_directory = "zipped_files"

        # Create directories if they don't exist
        os.makedirs(self.input_directory, exist_ok=True)
        os.makedirs(self.renamed_directory, exist_ok=True)
        os.makedirs(self.zipped_directory, exist_ok=True)

        # Clear directories to start with an empty slate
        self.clear_directory(self.input_directory)
        self.clear_directory(self.renamed_directory)
        self.clear_directory(self.zipped_directory)

        # Settings variables
        self.rename_prefix = "renamed_"
        self.zip_cluster_size = 5
        self.nesting_type = "Flat"

        # Show/Hide file state variables
        self.show_input_files = tk.BooleanVar(value=True)
        self.show_renamed_files = tk.BooleanVar(value=True)
        self.show_zipped_files = tk.BooleanVar(value=True)

        # Create DirectoryColumn instances
        self.input_column = DirectoryColumn(
            self.main_container, "Input Files", self.input_directory, self.show_input_files, self.load_input_files, self.on_drop_input
        )
        self.renamed_column = DirectoryColumn(
            self.main_container, "Renamed Files", self.renamed_directory, self.show_renamed_files, self.load_renamed_files, self.on_drop_renamed
        )
        self.zipped_column = DirectoryColumn(
            self.main_container, "Zipped Files", self.zipped_directory, self.show_zipped_files, self.load_zipped_files, self.on_drop_zipped
        )

        # Start file monitoring processes
        self.input_monitor = FileMonitorProcess(self.input_directory, self.queue)
        self.renamed_monitor = FileMonitorProcess(self.renamed_directory, self.queue)
        self.zipped_monitor = FileMonitorProcess(self.zipped_directory, self.queue)

        self.input_monitor.start()
        self.renamed_monitor.start()
        self.zipped_monitor.start()

        # Reference to track if the app is closing
        self.is_closing = False

        # Timer attributes
        self.timer_running = False
        self.start_time = None
        self.timer_label = ttk.Label(self, text="Elapsed Time: 00:00:00", font=("Helvetica", 14))
        self.timer_label.grid(row=2, column=1, pady=10)

        # Add buttons to trigger multiprocessing tasks
        self.renamed_column.add_additional_button("Rename Files", self.start_rename_files)
        self.zipped_column.add_additional_button("Collate Files", self.start_collate_files)

        # Add download buttons
        self.renamed_column.add_additional_button("Download Renamed", self.download_renamed)
        self.zipped_column.add_additional_button("Download Zipped", self.download_zipped)

        # Settings buttons
        self.rename_settings_button = ttk.Button(self, text="Rename Settings", command=self.show_rename_settings)
        self.rename_settings_button.grid(row=1, column=0, sticky="n", pady=10)

        self.zip_settings_button = ttk.Button(self, text="Zip Settings", command=self.show_zip_settings)
        self.zip_settings_button.grid(row=1, column=2, sticky="n", pady=10)

        # Create Settings Frames
        names_list = ["Alice", "Bob", "Charlie", "Diana"]  # Example names
        self.rename_settings_frame = RenameSettingsFrame(self, self.show_main_frame, self.update_rename_prefix, names_list)
        self.zip_settings_frame = ZipSettingsFrame(self, self.show_main_frame, self.update_zip_cluster_size)
        self.zip_settings_frame.grid(row=0, column=1, padx=20, pady=10)

        # Hide the settings frame initially
        self.zip_settings_frame.grid_remove()

        # Periodically check the queue for updates
        self.after_id = None
        self.check_queue()

    def check_queue(self):
        """Check the queue for file updates and update the GUI."""
        if self.is_closing:
            return  # Stop checking the queue if the application is closing

        while not self.queue.empty():
            directory, files = self.queue.get()
            if files:  # Ensure files are not empty before proceeding
                if directory == self.input_directory:
                    self.input_column.update_listbox(files)
                elif directory == self.renamed_directory:
                    self.renamed_column.update_listbox(files)
                elif directory == self.zipped_directory:
                    self.zipped_column.update_listbox(files)

        # Schedule the next queue check
        self.after_id = self.after(100, self.check_queue)  # Check every 100ms, adjust as needed

    def start_rename_files(self):
        """Start the rename files process using starmap."""
        self.start_timer()
        process = Process(target=rename_files_in_parallel, args=(self.input_directory, self.rename_prefix))
        process.start()
        process.join()
        self.load_renamed_files(self.renamed_directory)
        self.stop_timer()

    def start_collate_files(self):
        """Start the collate files process."""
        self.start_timer()
        process = Process(target=self.collate_files, args=(self.input_directory, self.zipped_directory))
        process.start()
        process.join()
        self.load_zipped_files(self.zipped_directory)
        self.stop_timer()

    def start_timer(self):
        """Start the timer when a function begins."""
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.config(text=f"Elapsed Time: {hours:02}:{minutes:02}:{seconds:02}")
            self.after(1000, self.update_timer)  # Update every second

    def stop_timer(self):
        """Stop the timer."""
        self.timer_running = False

    def collate_files(self, input_dir, output_dir):
        """Multiprocessing method to collate files from the input directory to the output directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                shutil.copy(os.path.join(root, file), os.path.join(output_dir, file))

    def download_renamed(self, event=None):
        """Handle download for renamed files."""
        self.create_download_zip(self.renamed_directory, "renamed_files.zip")
        self.download_complete_message(self.renamed_column.additional_buttons[-1])

    def download_zipped(self, event=None):
        """Handle download for zipped files."""
        self.create_download_zip(self.zipped_directory, "zipped_files.zip")
        self.download_complete_message(self.zipped_column.additional_buttons[-1])

    def create_download_zip(self, directory, default_zip_name):
        """Create and save a zip file for the specified directory."""
        zip_filename = filedialog.asksaveasfilename(defaultextension=".zip", initialfile=default_zip_name, filetypes=[("Zip files", "*.zip"), ("All files", "*.*")])
        if zip_filename:
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, directory)
                        zipf.write(full_path, arcname=arcname)

    def download_complete_message(self, button):
        """Show download complete message on the button."""
        original_text = button.cget("text")
        button.config(text="Download Complete")
        self.after(2000, lambda: button.config(text=original_text))  # Reset after 2 seconds

    def show_rename_settings(self):
        """Show the rename settings frame."""
        self.hide_main_interface()
        self.rename_settings_frame.grid(row=0, column=1, padx=20, pady=10)

    def show_zip_settings(self):
        """Show the zip settings frame."""
        self.hide_main_interface()
        self.zip_settings_frame.grid(row=0, column=1, padx=20, pady=10)

    def hide_main_interface(self):
        """Hide the main interface elements."""
        self.main_container.grid_remove()
        self.rename_settings_button.grid_remove()
        self.zip_settings_button.grid_remove()

    def show_main_frame(self):
        """Show the main frame with columns."""
        self.rename_settings_frame.grid_forget()
        self.zip_settings_frame.grid_forget()
        self.main_container.grid()
        self.rename_settings_button.grid()
        self.zip_settings_button.grid()

    def update_rename_prefix(self, prefix):
        """Update the prefix for renaming files."""
        self.rename_prefix = prefix or "renamed_"

    def update_zip_cluster_size(self, cluster_size):
        """Update the number of files per cluster in zipping."""
        self.zip_cluster_size = cluster_size if cluster_size > 0 else 5

    def load_input_files(self, directory):
        """Load files from the input directory and update the input column."""
        files = self.list_files(directory)
        self.input_column.update_listbox(files)

    def load_renamed_files(self, directory):
        """Load files from the renamed directory and update the renamed column."""
        files = self.list_files(directory)
        self.renamed_column.update_listbox(files)

    def load_zipped_files(self, directory):
        """Load files from the zipped directory and update the zipped column."""
        files = self.list_files(directory)
        self.zipped_column.update_listbox(files)

    def on_drop_input(self, event):
        """Handle file drop in the input column."""
        file_paths = self.tk.splitlist(event.data)
        for file_path in file_paths:
            if os.path.isdir(file_path):
                self.input_column.set_root_directory(os.path.basename(file_path))
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        relative_path = os.path.relpath(full_path, file_path)
                        dest_path = os.path.join(self.input_directory, relative_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy(full_path, dest_path)
            else:
                print(f"Ignored non-directory item: {file_path}")

        self.load_input_files(self.input_directory)

    def on_drop_renamed(self, event):
        """Handle file drop in the renamed column."""
        pass  # Placeholder for handling drop events in the renamed column

    def on_drop_zipped(self, event):
        """Handle file drop in the zipped column."""
        pass  # Placeholder for handling drop events in the zipped column

    def clear_directory(self, directory):
        """Clear the specified directory."""
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    def list_files(self, directory):
        """List files in the specified directory."""
        return [os.path.relpath(os.path.join(root, file), directory) for root, dirs, files in os.walk(directory) for file in files]

    def on_closing(self):
        """Handle the application closing."""
        self.is_closing = True  # Set the closing flag
        if self.after_id is not None:
            self.after_cancel(self.after_id)  # Cancel any scheduled after calls
        self.input_monitor.terminate()
        self.renamed_monitor.terminate()
        self.zipped_monitor.terminate()
        self.input_monitor.join()
        self.renamed_monitor.join()
        self.zipped_monitor.join()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
