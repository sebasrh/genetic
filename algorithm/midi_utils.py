import subprocess
from pydub import AudioSegment

def convert_midi_to_wav_mp3(file_midi, soundfont_path):
    # Build file paths
    file_wav = file_midi.replace(".mid", ".wav")
    file_mp3 = file_midi.replace(".mid", ".mp3")

    # Use FluidSynth to convert MIDI to WAV
    fluidsynth_command = f"fluidsynth -a alsa -g 1.0 -l -i '{soundfont_path}' '{file_midi}' -F '{file_wav}'"
    subprocess.run(fluidsynth_command, shell=True)

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

    return file_wav, file_mp3, final_duration