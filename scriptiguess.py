import csv
import math
import copy
import sys

with open('mscb.csv',newline="") as studentNames:
    names = csv.reader(studentNames, delimiter=',')
    namesList = []
    for line in names:
        namesList.append(tuple(line))

#so now you have a list of tuples of (last,first), already sorted in alpha order by excel :)

numStudents = len(namesList)
nums = []
namesList.reverse()

def optimizeTables(n):
	#where n is some number of students.
	#TODO: if the number of students is less than or near 18 (which is the max per page) then.......
	pages = math.ceil(n/18)
	#if you think about it, the tables separated by page are really just one big table haha where the "height" is pages*the smaller table's height.
	totalRows = n//pages + 1
	leftoverRow = n%pages #the value of the last row.
	if leftoverRow == 0:
		totalRows -= 1
		
	#there are (page) pages of tables of height 3.
	maxH = 3
	
	colPerPage = math.ceil(totalRows/maxH)
	lastPage = n - (pages-1)*(colPerPage*maxH)
	
	#test some values around colPerPage. minimum 3, maximum 6
	lastR = 0 #length of the very last row.
	lastMaxCols = 0 #num of columns in the table on the last page
	testMax = 0 #temporary
	#the purpose of this for loop is to check what the ideal length (num of columns) of the very last row should be.
	#the number in the interval [4,6] that gives either the greatest or least (i.e. 0) mod should be selected for the column thing.
	for i in range(4,6):
		rem = lastPage%i
		if rem > testMax and rem != 0:
			testMax = rem
			lastR = rem
			lastMaxCols = i
		elif rem == 0:
			lastR = 0
			lastMaxCols = i
			break
	
	#so (for the last page) lastMaxCols gives you your new max column length and lastR gives you the length of the very last row. If lastMaxCols = 0 something is not right...
	
	lastMaxRows = (lastPage - lastR)//lastMaxCols
	print("There are",pages-1,"pages of maxed-out tables of size "+str(maxH)+"x"+str(colPerPage)+". The last page has",lastPage,"which is divided into "+str(lastMaxRows)+"x"+str(lastMaxCols)+" with a very last row of length",lastR)

	global nums
	nums = [pages-1,maxH,colPerPage,lastMaxRows,lastMaxCols,lastR]
	return nums

def generateNameTable(title, filePath, hayRooms, hayPosn):
	#the purpose of this function is to take the parameters of dimensions from the optimizeTables function and write the html.
	#nums[0] = pages of maxed-out tables, nums[1] = rows in these max tables, nums[2] = columns in these max tables
	#hayRooms, hayPosn are booleans.
	bepis = copy.deepcopy(namesList)
	#making the maxed tables:
	for maxP in range(nums[0]):
		print(tabs(4)+"""<section style="width:85%;margin-left: 7%;">""")
		print(tabs(4)+"<!-- PAGE"+str(maxP+1)+"-->")
		print(tabs(4)+"<h1>"+title+"("+str(maxP+1)+"/"+str(nums[0]+1)+")</h1>")
		print(tabs(5)+"<table>")
		for i in range(nums[1]):
			print(tabs(6)+"<tr>")
			for j in range(nums[2]):
				tdNameCode(bepis.pop(),filePath,hayRooms,hayPosn)
			print(tabs(6)+"</tr>")
		print(tabs(5)+"</table>")
		print(tabs(4)+"</section>")
	#making the last table:
	print(tabs(4)+"""<section style="width:85%;margin-left: 7%;">""")
	print(tabs(4)+"<!-- PAGE"+str(nums[0]+1)+"-->")
	print(tabs(4)+"<h1>"+title+"("+str(nums[0]+1)+"/"+str(nums[0]+1)+")</h1>")
	print(tabs(5)+"<table>")
	for i in range(nums[3]):
		print(tabs(6)+"<tr>")
		for j in range(nums[4]):
			tdNameCode(bepis.pop(),filePath,hayRooms,hayPosn)
		print(tabs(6)+"</tr>")
	if nums[5] > 0:
		print(tabs(6)+"<tr>")
		for k in range(nums[5]):
			tdNameCode(bepis.pop(),filePath,hayRooms,hayPosn)
		print(tabs(6)+"</tr>")
	print(tabs(5)+"</table>")
	print(tabs(4)+"</section>")
	
	
def tabs(n):
	#just simple /t maker for easy tabbing while I don't have the darn module
	s = ""
	for i in range(n):
		s += "\t"
	return s
	
def tdNameCode(nameTuple,filePath, hasRoom,hasPosn):
	#generates the single <td></td>.
	#idk why the html module won't import so dumb code
	block= tabs(7)+"""<td style="border:none;">"""+"\n"+tabs(8)+"""<div style="border:none;">"""+"\n"+tabs(9)+"""<img src="images/"""+filePath+nameTuple[0]+"_"+nameTuple[1]+""".jpg" style="margin:0 0 0 0;"/>"""+"\n"+tabs(9)+"""<figcaption style="font-size:40px; text-align:center">"""+nameTuple[1]+" "+nameTuple[0]+"""</figcaption>"""+"\n"+tabs(9)+"<br>\n"
	if hasPosn:
		position = "\n"+tabs(9)+"""<figcaption style="font-size:35px; text-align:center">POSITION</figcaption>"""
		block += position
	if hasRoom:
		room = "\n"+tabs(9)+"""<figcaption style="font-size:35px; text-align:center">GHC 7777</figcaption>"""
		block += room+"\n"+tabs(9)+"<br>\n"
	block+=tabs(8)+"</div>\n"+tabs(7)+"</td>"
	#print(bs(block,'html.parser').prettify(indent_width=4))
	print(block)
	
def main(title, filePath,rooms,posn):
	#filePath is for the images, e.g. students/MSCB/
	optimizeTables(numStudents)
	sys.stdout = open("tables.txt", "w")
	generateNameTable(title, filePath, rooms,posn)
	sys.stdout = sys.__stdout__
	print("Done!")
	
