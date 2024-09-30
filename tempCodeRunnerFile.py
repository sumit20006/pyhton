import pygame
import time
import os

# Initialize pygame mixer
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, directory):
        self.directory = directory
        self.track_list = self.load_tracks()
        self.current_track_index = 0

    def load_tracks(self):
        """Load all music files from the given directory"""
        return [track for track in os.listdir(self.directory) if track.endswith(".mp3")]

    def play(self):
        """Play the current track"""
        if not self.track_list:
            print("No tracks found!")
            return
        
        current_track = self.track_list[self.current_track_index]
        pygame.mixer.music.load(os.path.join(self.directory, current_track))
        pygame.mixer.music.play()
        print(f"Playing: {current_track}")
    
    def pause(self):
        """Pause the currently playing track"""
        pygame.mixer.music.pause()
        print("Music paused")
    
    def unpause(self):
        """Unpause the currently paused track"""
        pygame.mixer.music.unpause()
        print("Music unpaused")

    def stop(self):
        """Stop the music"""
        pygame.mixer.music.stop()
        print("Music stopped")

    def next_track(self):
        """Move to the next track"""
        if not self.track_list:
            return
        self.current_track_index = (self.current_track_index + 1) % len(self.track_list)
        self.play()

    def prev_track(self):
        """Move to the previous track"""
        if not self.track_list:
            return
        self.current_track_index = (self.current_track_index - 1) % len(self.track_list)
        self.play()

    def show_track_list(self):
        """Show the list of available tracks"""
        print("Track List:")
        for i, track in enumerate(self.track_list):
            print(f"{i + 1}. {track}")

# Example usage
if __name__ == "__main__":
    music_dir = "path_to_your_music_directory"  # Replace with your directory path
    player = MusicPlayer(music_dir)

    # Show track list
    player.show_track_list()

    # Example controls
    player.play()      # Play first track
    time.sleep(10)     # Play for 10 seconds
    player.pause()     # Pause the music
    time.sleep(5)      # Wait for 5 seconds
    player.unpause()   # Unpause the music
    time.sleep(5)      # Play for another 5 seconds
    player.next_track()# Move to next track
    time.sleep(10)     # Play for 10 seconds
    player.stop()      # Stop the music
