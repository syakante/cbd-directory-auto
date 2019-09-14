import csv
import math
import re

myDicc = {}
tabs = "\t\t\t\t\t\t\t\t\t"

with open('roomNumbers.csv',newline="") as bepis:
    sheet = csv.reader(bepis, delimiter=',')
    for line in sheet:
        roomNo = line[0]
        firstName = line[2]
        lastName = line[1]
        fullName = firstName+' '+lastName
        myDicc[fullName] = [roomNo, firstName, lastName]

notFound = {}

### get name and line number of their occurrence ###

with open("htmlCode.txt") as textFile:
    allContent = textFile.read()
    textFile.seek(0)
    fileByLines = textFile.readlines()
    for k in myDicc:
        fullName = k
        imageName = myDicc[k][2]+'_'+myDicc[k][1]
        fullNameFlag = fullName not in allContent
        if fullNameFlag and imageName not in allContent:
            notFound[fullName] = myDicc[k][0]
        else:
            #print("finding",fullName)
            lineCounter = 0
            for line in fileByLines:
                if fullName in line:
                    #print("found",fullName,"(full name)")
                    #print(lineCounter)
                    myDicc[k].extend([lineCounter, False])
                elif fullNameFlag and imageName in line:
                    #print("found",fullName,"(image name)")
                    #print(lineCounter)
                    myDicc[k].extend([lineCounter, True])
                lineCounter += 1

#the true/false value refers to whether the person was found listed under imageName (t) or fullName (f).
#since True = 1 and False = 0, this helps when moving forward line numbers.

for missing in notFound.keys():
    del myDicc[missing]

### regex for replacing room number ###

fullPattern = re.compile('[A-Z|-]+ \d+[A-Z]|[A-Z|-]+ \d+')
#this regex finds every full room number, such as BH ###B, GHC ###, MI ###, CMU-Q ###
#currently the csv I'm working with just gives 7###, which applies to the people found in the dictionary keys. So just replacing the whole room no. with GHC ### should be fine for now.

### replacing/adding room number ###
for k in myDicc:
    roomNo = 'GHC '+myDicc[k][0]
    lineFound = myDicc[k][3]+int(myDicc[k][4])
    for i in range(lineFound+1, lineFound+4):
        if fileByLines[i].strip().endswith("<br>"):
            #print("inserting",roomNo,"for",k)
            fileByLines[i] = str(tabs+"""<figcaption style="font-size:35px; text-align:center">"""+roomNo+"""</figcaption>"""+"\n"+tabs+"<br>\n")
            #print("inserted for",k)
            break
        elif bool(fullPattern.search(fileByLines[i])):
            fileByLines[i] = fullPattern.sub(roomNo,fileByLines[i])
            #print("regex done for",k)
            break
        elif i == lineFound+3 and bool(fullPattern.search(fileByLines[i])) == False:
            print("!!! smth wrong with",k)
            
        #regex sub makes the sub if the pattern is found, so there needs to be a way to add the room number for people who got a room number assigned but didn't have one previously.

with open("output.txt", "w") as text_file:
    print("".join(fileByLines), file=text_file)
    
print("Done! Open output.txt to see your html code.")
print(len(notFound),"names couldn't be found in the source:")
print(notFound)