#! python3
# 
# Read in lines of text and determine where paragraph breaks should occur.

# Assumptions
# 1. Very first line of input will NOT end a paragraph
# 2. Paragraphs end w/ ".", "?", "!"
# 3. Paragraph last line is shorter than other paragraph lines
# So, find lines in para_lines that end w/ above punctuation and are shorter than average line 
# length

# Assign global variables
para_lines = []
new_para = []
x = 0
avgLen = 0


def processLine(newLine,counter):
    """Is the line passed in a line that ends a paragraph?

    Arguments: newLine: line to check
               counter: what line are we checking
    """
    global new_para
    global avgLen
    lenLine = len(newLine)
    endLine = False
    firstChar = newLine[0]
    lastChar = newLine[-1] if newLine[-1] != "\n" else newLine[-2]
    if lastChar in ".!?":
        endLine = True
    avgLen = ((avgLen + lenLine) / 2) if counter > 0 else lenLine
    new_para.append(newLine)
    if endLine and len(newLine) <= (avgLen * .90):
        new_para.append("\n")
    return


with open('paragraph_data_in.txt', mode='r') as para_data:
    para_lines = para_data.readlines()
numLines = len(para_lines)

while x < numLines:
    newLine = para_lines[x]
    processLine(newLine,x)
    x += 1

with open('paragraph_data_out.txt', mode='w') as para_data:
    para_data.writelines(new_para)


