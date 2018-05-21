from pathlib import Path

def standardize(text):
    text = text.upper()
    text = text.strip()
    return text
# Standardize input END

class SimplifiedHanChar:

    PhraseConstraint = {}
    def __init__(self, char):
        self.char = char
    
    def ord(self):
        return ord(self.char)

    def setTraditionalCharacters(self, chars):
        self.traditionalCharacters = chars

    def addPhraseConstraint(self, string, output):
        self.PhraseConstraint[string] = output

# SimplifiedHanChar Char Class END

dictionary = {}

completeHanTableFile = "HanTable.txt"
SimplifiedToHanTableFile = "SimplifiedToHanTable.txt"
dictionaryFile = "Dictionary"

def createSimplifiedToHanTable():
    if Path(completeHanTableFile).exists():
        savedLines = []
        with open(completeHanTableFile, "r") as file:
            lines = file.readlines()
            savedLines = [line for line in lines if "kTraditionalVariant" in line]

        for i, line in enumerate(savedLines):
            codepoints = line.split()
            codepoints.pop(1)
            for j, codepoint in enumerate(codepoints):
                codepoints[j] = "\\U" + "0" * (10 - len(codepoint)) + codepoint[2:]
            savedLines[i] = " ".join(codepoints) + "\n"

        with open(SimplifiedToHanTableFile, "w") as file:
            file.writelines(savedLines)
# Create Simplified To Han Table END

def createDatabase():
    if Path(SimplifiedToHanTableFile).exists():
        lines = []
        with open(SimplifiedToHanTableFile, "r") as file:
            lines = file.readlines()
        for line in lines:
            line = line[:-1]
            line = eval("u\"" + line + "\"")
            line = line.split()
            simplifiedHanChar = SimplifiedHanChar(line[0])
            line.pop(0)
            simplifiedHanChar.setTraditionalCharacters(line)
            dictionary[simplifiedHanChar.char] = simplifiedHanChar
# Create Database END

createSimplifiedToHanTable()
createDatabase()
command = ""
while command != "EXIT":
    command = standardize(input("Enter command: "))
    cmdSections = command.split()
    if cmdSections[0] == "GENERATETABLE":
    # Generate Convert Table
        createSimplifiedToHanTable()
    if cmdSections[0] == "CREATEDATABASE":
    # Create Database
        createDatabase()
    if cmdSections[0] == "CONVERT":
    # Convert
        convertFile = input("Filename (with .txt): ")
        resultFile = input("Output as (with .txt): ")
        result = ""
        with open(convertFile, "r") as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                if char in dictionary:
                    result += dictionary[char].traditionalCharacters[0]
                else:
                    result += char
        print(result)
        with open(resultFile, "w") as file:
            file.write(result)



