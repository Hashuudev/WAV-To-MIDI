import librosa
from mido import MidiFile, MidiTrack, Message
import numpy as np


def convert_wav_to_midi(input_filename, output_filename, bpm):
    # Load the WAV file with the original sampling rate
    print("1")
    y, sr = librosa.load(input_filename, sr=None)

    # Estimate pitches using the Constant-Q chromagram
    chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Find the most dominant pitch in each frame
    dominant_pitches = np.argmax(chromagram, axis=0)
    # Shift pitches to MIDI note numbers (A0 is MIDI note 21)
    midi_notes = dominant_pitches + 21

    # Create MIDI messages with note-on and note-off events
    midi_messages = []
    time = 0
    for note in midi_notes:
        note_on = Message('note_on', note=note, velocity=64, time=int(time))
        midi_messages.append(note_on)

        note_off_time = time + int(bpm * 60 / bpm)  # Assuming a constant tempo
        note_off = Message('note_off', note=note,
                           velocity=0, time=note_off_time)
        midi_messages.append(note_off)

        time += int(bpm * 60 / bpm)  # Increment time based on the tempo

    # Create and save the MIDI file
    output_midi = MidiFile()
    track = MidiTrack()
    output_midi.tracks.append(track)
    for msg in midi_messages:
        track.append(msg)
    output_midi.save(output_filename)


if __name__ == "__main__":
    input_filename = './1.wav'
    output_filename = 'output.mid'
    bpm = 120
    convert_wav_to_midi(input_filename, output_filename, bpm)
