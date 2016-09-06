import sys, getopt

def main(inFile):
	print(inFile)
	try:
		commands = open(inFile,'r')
	except:
		print("bad input file: "+inFile)
		sys.exit(2)
	sizeX = 0
	sizeY = 0
	x = 0
	y = 0
	output = []
	for line in commands:
		command = line.strip()
		if (sizeX ==0):
			sizeX,sizeY = map(int,command.split(','))
			print('Size {} x {}'.format(sizeX,sizeY))
			for s in range(0,sizeY):
				row = [False]*sizeX
				output.append(row)
			if(sizeX ==0 | sizeY ==0):
				printHelp()
		                sys.exit(2)
		else:
			command = command.split(' ')
			#this always marks the starting 0 0 location
			output[y][x] = True
#			printGrid(output)
#			print command, x, y
			for order in command:
				if(len(order)==0):
					pass
				elif(order[0]=='u'):
					y-=1
				elif(order[0]=='d'):
					y+=1
				elif(order[0]=='l'):
					x-=1
				elif(order[0]=='r'):
					x+=1
				elif(order[0]=='c'):
					output = []
					for s in range(0,sizeY):
						row = [False]*sizeX
						output.append(row)
			#prevent werid from happening
			if(x>sizeX-1):
				x = sizeX-1
			if(x<0):
				x=0
			if(y>sizeY-1):
				y = sizeY-1
			if(y<0):
				y=0
	output[y][x] = True
	printGrid(output)

#format the output
def printGrid(grid):
	top = "   "
	for i in range(0,len(grid[0])):
		top += str(i)+" "
	print(top)
	for i in range(len(grid)):
		row = str(i)+": "
		for col in grid[i]:
			if col:
				row+='X '
			else:
				row+='  '
		print(row)

#incase you dont read the readme
def printHelp():
	print("usage: main.py -i <inputFile>")
	print("Input file needs to be plain text")
	print("Starting with size of the dislay grid like '8,8' on its own line")
	print("Every line after that is a command for moving the 'pen' on the grid")
	print("multiple commands can be given per line, sperate them by a space")
	print("Accpted commands are up,down,left,right,clear,u,d,l,r,c")
	print("example inpute file:\n\n8,2\ndown\nright right right")
	print("\nproduces\n")
	print("Size 8 x 2\n   0 1 2 3 4 5 6 7 \n0: X               \n1: X     X ")

if __name__ == '__main__':
	#parse args frome sys
	try:
		opts,args = getopt.getopt(sys.argv[1:],'hi:',['ifile'])
	except:
		printHelp()
		sys.exit(2)
	inputFile = ''
	for opt , arg in opts:
		if(opt=='-h'):
			printHelp()
		elif(opt=='-i'):
			inputFile = arg
	if(inputFile==''):
		printHelp()
		sys.exit(2)
	main(inputFile)
