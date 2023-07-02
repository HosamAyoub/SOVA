from pygame import mixer, quit

def play_audio(audio_file):
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    quit()

# Example usage
audio_file = "InFront.wav"  # Replace with the actual path to your audio file
play_audio(audio_file)
exit(0)