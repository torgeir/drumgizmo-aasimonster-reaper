#!/usr/bin/python

# import library for working with midi files
import midi
import math
import sys


if len(sys.argv) > 5 or len(sys.argv) < 2:
    print("Usage: midi2hydro_pattern.py infile (outfile) (genre) (name)")
    quit()

filename = sys.argv[1]

if len(sys.argv) > 2:
    outfilename = sys.argv[2]
else:
    outfilename = filename+".h2pattern"
if len(sys.argv) > 3:
    category = sys.argv[3]
else:
    category = "Uncategorized"
if len(sys.argv) > 4:
    pattern_name = sys.argv[4]
else:
    pattern_name = filename.split(".mid")[0]
    



# load file
pattern = midi.read_midifile(filename)

# list for new note items
new_notes = []

# magic number for resolution of hydrogen files
res = 48

# number of beats per quarter note in midi file
resolution = pattern.resolution


note = midi.NoteOnEvent()
noteoff = midi.NoteOffEvent()
timeSig = midi.TimeSignatureEvent()
tempo = midi.SetTempoEvent()

# number of beats per quarter in midi file / number of beats per quater in hydrogen
ratio = resolution / res

# get length from total number of ticks
total_ticks = 0
for track in pattern:
    this_track_ticks = 0
    for line in track:
        if type(line) == type(timeSig):
            timeSig = line
        elif type(line) == type(tempo):
            tempo = line
        elif type(line) == type(note): 
            this_track_ticks += line.tick
            new_notes.append([round(this_track_ticks/ratio),line.data])
        elif type(line) == type(noteoff):
            this_track_ticks += line.tick
    if this_track_ticks>total_ticks:
        total_ticks = this_track_ticks
            
num_of_quarter_notes = math.ceil(total_ticks/resolution)
length= num_of_quarter_notes*res


# open file for writing
outfile = open(outfilename,"w")
outfile.write("<drumkit_pattern>\n")
outfile.write("    <pattern_for_drumkit>GMkit</pattern_for_drumkit>\n")
outfile.write("    <pattern>\n")
outfile.write("        <pattern_name>" + pattern_name + "</pattern_name>\n")
outfile.write("        <category>"+category+"</category>\n")
outfile.write("        <size>" + str(length) + "</size>\n")
outfile.write("        <noteList>\n")
for note in new_notes:
    outfile.write("            <note>\n")
    outfile.write("            <position>" + str(note[0]) + "</position>\n")
    outfile.write("            <leadlag>0</leadlag>\n")
    outfile.write("            <velocity>" + str((note[1][1]/127)) + "</velocity>\n")
    outfile.write("            <pan_L>0.5</pan_L>\n")
    outfile.write("            <pan_R>0.5</pan_R>\n")
    outfile.write("            <pitch>0</pitch>\n")
    outfile.write("            <key>C0</key>\n")
    outfile.write("            <length>-1</length>\n")
    outfile.write("            <instrument>" + str(note[1][0]-36) + "</instrument>\n")
    outfile.write("            </note>\n")
outfile.write("        </noteList>\n")
outfile.write("    </pattern>\n")
outfile.write("</drumkit_pattern>\n")
outfile.close

    

    

