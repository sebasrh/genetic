import  fluidsynth
from pydub import AudioSegment
import os

def convert_midi_to_wav_mp3(file_midi, soundfont_path):
    # Build file paths
    file_wav = file_midi.replace(".mid", ".wav")
    file_mp3 = file_midi.replace(".mid", ".mp3")

    fs = fluidsynth.Synth() # Create synthesizer instance (plays audio) 
    fs.start(driver="dsound") # Start audio driver (For windows, use driver="dsound")
    sfid = fs.sfload(soundfont_path) # Load SoundFont file 
    fs.program_select(0, sfid, 0, 0) # Select program for a channel 

    fs.midi_file_load(file_midi) # Load MIDI file 

    audio_data = fs.get_samples() # Get samples as NumPy array 

    with open(file_wav, "wb") as f: # Save as WAV file 
        f.write(bytes(audio_data)) 

    # Load the WAV file using pydub
    audio = AudioSegment.from_wav(file_wav)

    # Adjust the duration (remove the last 2 seconds)
    adjusted_audio = audio[:-2000]  # Assuming each second is 1000 milliseconds

    # Adjust the volume (add 10 dB)
    adjusted_audio = adjusted_audio + 10

    # Export to MP3
    adjusted_audio.export(file_mp3, format="mp3")

    # Calculate and store the final duration
    final_duration = len(adjusted_audio) / 1000.0  # Convert milliseconds to seconds

    os.remove(file_wav) # Delete the WAV file (not needed anymore) 

    fs.delete() # Delete synthesizer instance 

    return file_wav, file_mp3, final_duration