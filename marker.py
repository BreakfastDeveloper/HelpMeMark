import os
import re
import subprocess

assignmentDir = "Assignments/A1/"

def HandleTxtSubmission(fileName):
    print("NEW STUDENT\n")
    split = str(fileName).split("-")
    name = split[2]
    timeOfSub = split[3]

    inFile = open(assignmentDir + fileName, "r")
    print(str(name) + " " + str(timeOfSub))
    SplitFileIntoQuestions(inFile)
    inFile.close()
    return


def SplitFileIntoQuestions(file):
    startOfQuestion = "source code ***/"
    startOfOutput = "output ***/"

    sourceNum = 0
    outputNum = 0
    source = False
    output = False

    sourceOutput = str()

    questionTxt = list()
    outputTxt = list()

    f1 = file.readlines()

    for line in f1:        
        if(line.find(startOfQuestion) > 0):
            source = True
            sourceNum = int(re.search(r'\d+', line).group())

        elif(line.find(startOfOutput) > 0):
            outputNum = int(re.search(r'\d+', line).group())
            output = True

        # case where source of a question is done
        if(output and source and outputNum == sourceNum):
            source = False
            sourceOutput = CreateQuestionOutput(questionTxt)
            del questionTxt[:]

        # case where output is done
        elif(output and source and outputNum != sourceNum):   
            output = False     
            AddQuestionResults(sourceOutput, outputTxt, outputNum)
            del outputTxt[:]

        if( source == True ):
            questionTxt.append(line)

        elif(output == True):
            outputTxt.append(line)

    if(output == True and source == False):
        AddQuestionResults(sourceOutput, outputTxt, outputNum)


    return

def CreateQuestionOutput(questionText):
    try:
        os.remove("temp.c")
    except OSError:
        pass
    try:
        os.remove("temp")
    except OSError:
        pass

    outfile = open("temp.c", "w")

    for line in questionText:
        outfile.write(line)

    outfile.close()

    
    compileCmd = "gcc -Wall temp.c -o temp"    
    exeCmd = "./temp"
   
    print("***COMPILE RESULTS***")
    compileRtn = subprocess.call(compileCmd, shell=True)
    print("\n*********************")

    print("***EXECUTING QUESTION***")
    exeRtn = subprocess.call(exeCmd, shell=True)
    print("\n************************")
    
    return "temp"

def AddQuestionResults(srcOutput, givenOutput, questionNum):
    return

count = 0

unsortedLastName = list()

for fileName in os.listdir(assignmentDir):
    splitDash = str(fileName).split("-")
    splitName = splitDash[2].split(" ")
    print(splitName)
    lastName = splitName[2]
    print(str(lastName))
    unsortedLastName.append([lastName, fileName])

sortedByLastName = sorted(unsortedLastName, key=lambda x: x[0])

for lastname, filename in sortedByLastName:
    if filename.endswith(".txt"):
        print HandleTxtSubmission(filename)
    else:
        print("BAD: " + filename)
    
    count += 1

print("TOTAL - " + str(count))


