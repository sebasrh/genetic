import fluidsynth
from pydub import AudioSegment

def convert_midi_to_wav_mp3(file_midi, soundfont_path):

    # Build file paths
    file_wav = file_midi.replace(".mid", ".wav")
    file_mp3 = file_midi.replace(".mid", ".mp3")

    # Create a FluidSynth instance
    fs = fluidsynth.Synth()

    # Load the SoundFont
    sfid = fs.sfload(soundfont_path)

    # Initialize FluidSynth
    fs.start(driver="alsa")

    # Load the SoundFont instrument
    fs.program_select(0, sfid, 0, 0)

    # Load the MIDI file
    fs.midi_file_load(file_midi)

    # Render the MIDI file to WAV
    fs.midi_to_wav(file_midi, file_wav)

    # Stop and close FluidSynth
    fs.delete()

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