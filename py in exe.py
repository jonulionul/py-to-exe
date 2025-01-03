import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

# Function to check if PyInstaller is installed
def is_pyinstaller_installed():
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# Function to install PyInstaller if not installed
def install_pyinstaller():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        messagebox.showinfo("Success", "PyInstaller has been installed!")
        return True
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to install PyInstaller.")
        return False

# Function to select the .py file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

# Function to convert .py to .exe
def convert_to_exe():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a .py file!")
        return

    # Check if PyInstaller is installed
    if not is_pyinstaller_installed():
        user_response = messagebox.askyesno("PyInstaller Missing", "PyInstaller is not installed. Do you want to install it?")
        if user_response:
            if not install_pyinstaller():
                return
        else:
            messagebox.showinfo("Exit", "The program will now exit.")
            root.quit()
            return

    # Build the PyInstaller command
    command = ["pyinstaller", "--onefile"]
    if var_noconsole.get():
        command.append("--noconsole")
    command.append(file_path)

    # Run the command in the terminal
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "The EXE file has been created!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Conversion failed!")

# Function to open the dist folder
def open_dist_folder():
    dist_path = os.path.join(os.path.dirname(entry_file_path.get()), "dist")
    if os.path.exists(dist_path):
        os.startfile(dist_path)
    else:
        messagebox.showerror("Error", "The 'dist' folder was not found!")

# Create the main window
root = tk.Tk()
root.title("Py to EXE Converter")
root.geometry("400x250")
root.configure(bg="lightgray")

# Label and Entry for file selection
label_file = tk.Label(root, text="Select your .py file:", bg="lightgray")
label_file.pack(pady=10)
entry_file_path = tk.Entry(root, width=40, font=("Arial", 12))
entry_file_path.pack(pady=5)
button_browse = tk.Button(root, text="Browse", command=select_file)
button_browse.pack(pady=5)

# Checkbox for --noconsole
var_noconsole = tk.BooleanVar()
checkbox_noconsole = tk.Checkbutton(root, text="No Console (--noconsole)", variable=var_noconsole, bg="lightgray")
checkbox_noconsole.pack(pady=5)

# Button to convert to EXE
button_convert = tk.Button(root, text="Convert to EXE", command=convert_to_exe)
button_convert.pack(pady=10)

# Button to open the dist folder
button_open_dist = tk.Button(root, text="Open dist Folder", command=open_dist_folder)
button_open_dist.pack(pady=5)

# Start the Tkinter application
root.mainloop()
