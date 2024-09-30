import pygame
import os
import tkinter as tk
from tkinter import ttk, filedialog
import random
from mutagen.mp3 import MP3  # To get the length of the MP3 file

# Initialize pygame mixer
pygame.mixer.init()

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x450")
        self.root.configure(bg='#1e1e1e')

        # Music-related variables
        self.directory = ""
        self.track_list = []
        self.current_track_index = 0
        self.is_paused = False
        self.is_shuffled = False
        self.is_repeat = False
        self.track_length = 0  # Total length of current track
        self.update_time_bar = True  # To control time bar update
        self.track_loaded = False

        # Create the GUI components with styling
        self.track_label = tk.Label(root, text="No track playing", bg="#333", fg="#fff", width=50, anchor='center', font=("Helvetica", 14))
        self.track_label.pack(pady=20, padx=10)

        self.time_bar = tk.Scale(root, from_=0, to=100, orient='horizontal', showvalue=False, bg='#1e1e1e', fg='#fff', 
                                 highlightbackground='#1e1e1e', troughcolor='#444', sliderlength=15, length=300, command=self.seek)
        self.time_bar.pack(pady=10)

        self.time_display = tk.Label(root, text="00:00 / 00:00", bg="#333", fg="#fff", font=("Helvetica", 12))
        self.time_display.pack(pady=5)

        self.load_button = ttk.Button(root, text="Load Music Folder", command=self.load_music)
        self.load_button.pack(pady=10)

        control_frame = tk.Frame(root, bg='#1e1e1e')
        control_frame.pack(pady=10)

        self.prev_button = tk.Button(control_frame, text="⏮️", command=self.prev_track, width=4, bg='#333', fg='#fff', font=("Helvetica", 14))
        self.prev_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(control_frame, text="▶️", command=self.play_pause, width=4, bg='#333', fg='#fff', font=("Helvetica", 14))
        self.play_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(control_frame, text="⏹️", command=self.stop, width=4, bg='#333', fg='#fff', font=("Helvetica", 14))
        self.stop_button.grid(row=0, column=2, padx=10)

        self.next_button = tk.Button(control_frame, text="⏭️", command=self.next_track, width=4, bg='#333', fg='#fff', font=("Helvetica", 14))
        self.next_button.grid(row=0, column=3, padx=10)

        self.shuffle_button = tk.Button(root, text="🔀 Shuffle", command=self.toggle_shuffle, width=10, bg='#333', fg='#fff', font=("Helvetica", 12))
        self.shuffle_button.pack(pady=10)

        self.repeat_button = tk.Button(root, text="🔁 Repeat", command=self.toggle_repeat, width=10, bg='#333', fg='#fff', font=("Helvetica", 12))
        self.repeat_button.pack(pady=10)

        self.update_time()

    def load_music(self):
        """Allow the user to select a directory with music files."""
        self.directory = filedialog.askdirectory()
        if not self.directory:
            return
        
        self.track_list = [f for f in os.listdir(self.directory) if f.endswith(".mp3")]
        if self.track_list:
            self.current_track_index = 0
            self.update_track_label()

    def play_pause(self):
        """Play or pause the track."""
        if not self.track_list:
            return

        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="⏸️")
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()
            else:
                current_track = self.track_list[self.current_track_index]
                pygame.mixer.music.load(os.path.join(self.directory, current_track))
                pygame.mixer.music.play()
                self.get_track_length(os.path.join(self.directory, current_track))  # Get track length
                self.track_loaded = True
            self.is_paused = False
            self.play_button.config(text="▶️")
            self.update_track_label()

    def stop(self):
        """Stop the music."""
        pygame.mixer.music.stop()
        self.is_paused = False
        self.play_button.config(text="▶️")
        self.time_bar.set(0)
        self.track_loaded = False

    def next_track(self):
        """Play the next track."""
        if not self.track_list:
            return
        self.current_track_index += 1
        if self.current_track_index >= len(self.track_list):
            self.current_track_index = 0 if not self.is_repeat else len(self.track_list) - 1
        self.play_pause()

    def prev_track(self):
        """Play the previous track."""
        if not self.track_list:
            return
        self.current_track_index -= 1
        if self.current_track_index < 0:
            self.current_track_index = len(self.track_list) - 1
        self.play_pause()

    def toggle_shuffle(self):
        """Toggle shuffle mode."""
        self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            random.shuffle(self.track_list)
            self.shuffle_button.config(bg='#4caf50')  # Green for active
        else:
            self.track_list.sort()  # Return to original order
            self.shuffle_button.config(bg='#333')  # Default color

    def toggle_repeat(self):
        """Toggle repeat mode."""
        self.is_repeat = not self.is_repeat
        if self.is_repeat:
            self.repeat_button.config(bg='#4caf50')  # Green for active
        else:
            self.repeat_button.config(bg='#333')  # Default color

    def update_track_label(self):
        """Update the label to show the currently playing track."""
        current_track = self.track_list[self.current_track_index]
        self.track_label.config(text=f"Playing: {current_track}")

    def get_track_length(self, track_path):
        """Get the length of the track using mutagen."""
        audio = MP3(track_path)
        self.track_length = int(audio.info.length)
        self.time_bar.config(to=self.track_length)

    def update_time(self):
        """Update the time bar based on the current track position."""
        if pygame.mixer.music.get_busy() and self.track_loaded:
            current_time = pygame.mixer.music.get_pos() // 1000  # Convert milliseconds to seconds
            self.time_bar.set(current_time)
            elapsed_time = self.format_time(current_time)
            total_time = self.format_time(self.track_length)
            self.time_display.config(text=f"{elapsed_time} / {total_time}")

        if not self.is_paused:
            self.root.after(1000, self.update_time)

    def format_time(self, seconds):
        """Format time in MM:SS."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def seek(self, value):
        """Seek the song to the chosen time."""
        if self.track_loaded:
            pygame.mixer.music.play(start=int(value))
            self.is_paused = False

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
