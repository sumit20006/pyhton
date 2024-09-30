import tkinter as tk
from tkinter import messagebox
import os

# File to store notes
NOTES_FILE = "notes.txt"

# Function to write a new note
def save_note():
    note = note_text.get("1.0", tk.END).strip()
    if note:
        with open(NOTES_FILE, 'a') as file:
            file.write(note + "\n")
        messagebox.showinfo("Success", "Note saved!")
        note_text.delete("1.0", tk.END)
        view_notes()
    else:
        messagebox.showwarning("Warning", "Note is empty!")

# Function to view all saved notes
def view_notes():
    if os.path.exists(NOTES_FILE):
        notes_display.delete(1.0, tk.END)
        with open(NOTES_FILE, 'r') as file:
            notes = file.readlines()
            if notes:
                for i, note in enumerate(notes, start=1):
                    notes_display.insert(tk.END, f"{i}. {note}")
            else:
                notes_display.insert(tk.END, "No notes available.")
    else:
        notes_display.delete(1.0, tk.END)
        notes_display.insert(tk.END, "No notes available. Start by writing a note.")

# Function to delete all notes
def delete_notes():
    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)
        messagebox.showinfo("Deleted", "All notes deleted!")
        view_notes()
    else:
        messagebox.showinfo("No Notes", "There are no notes to delete.")

# Function to handle the clear text area button
def clear_note():
    note_text.delete("1.0", tk.END)

# Setting up the main window
app = tk.Tk()
app.title("Notes App")
app.geometry("500x400")

# Text area to write new notes
note_label = tk.Label(app, text="Write your note below:")
note_label.pack(pady=5)

note_text = tk.Text(app, height=5, width=50)
note_text.pack(pady=5)

# Save and clear buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=5)

save_button = tk.Button(button_frame, text="Save Note", command=save_note)
save_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="Clear Note", command=clear_note)
clear_button.grid(row=0, column=1, padx=10)

# Display area for saved notes
notes_label = tk.Label(app, text="Your saved notes:")
notes_label.pack(pady=5)

notes_display = tk.Text(app, height=10, width=50)
notes_display.pack(pady=5)
notes_display.config(state=tk.NORMAL)

# View and Delete buttons
action_frame = tk.Frame(app)
action_frame.pack(pady=10)

view_button = tk.Button(action_frame, text="View Notes", command=view_notes)
view_button.grid(row=0, column=0, padx=10)

delete_button = tk.Button(action_frame, text="Delete All Notes", command=delete_notes)
delete_button.grid(row=0, column=1, padx=10)

# Initialize the app by viewing notes
view_notes()

# Run the application
app.mainloop()
