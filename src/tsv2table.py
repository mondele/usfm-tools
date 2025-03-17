# Converts data from TSV file to a USFM table.

import io
import tsv

# globals
tsvpath = r'C:\DCS\Chin, Rawngtu\periphs\TSV files\periph_wts_meas.txt'
outputpath = r'C:\DCS\Chin, Rawngtu\periphs\wts-temp.usfm'

def clean(fieldvalue):
    value = fieldvalue.strip()
    value = value.replace("    ", " ")
    value = value.replace("   ", " ")
    value = value.replace("  ", " ")
    return value

def makeHeader(fields):
    line = f"\\tr \\th1 {clean(fields[0])}"
    for i in range(1, len(fields)):
        value = clean(fields[i])
        line += f" \\th{i+1} {value}"
    return line + '\n'

def makeRow(fields):
    line = f"\\tr \\tc1 {clean(fields[0])}"
    for i in range(1, len(fields)):
        value = clean(fields[i])
        line += f" \\tc{i+1} {value}"
    return line + '\n'

data = tsv.tsvRead(tsvpath)
output = io.open(outputpath, "tw", encoding='utf-8', newline='\n')
output.write(makeHeader(data[0]))
for i in range(1, len(data)):
    output.write(makeRow(data[i]))
output.close()
