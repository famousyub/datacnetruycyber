import tkinter as tk
from tkinter import messagebox
import subprocess

def ping_host():
    host = entry.get()
    if not host:
        messagebox.showerror("Error", "Please enter a host to ping.")
        return

    try:
        output = subprocess.check_output(['ping', '-t', host], stderr=subprocess.STDOUT, universal_newlines=True)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)
    except subprocess.CalledProcessError as e:
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, e.output)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Ping Application")

# Create and place the widgets
label = tk.Label(root, text="Enter host to ping:")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

ping_button = tk.Button(root, text="Ping", command=ping_host)
ping_button.pack(pady=5)

text_output = tk.Text(root, width=80, height=20)
text_output.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
