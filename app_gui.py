from tkinter import * 
# from Solver import Solver
from puzzle import Node
from puzzle import Puzzle
import time
import random
from itertools import chain
import _thread
from graphic import AnalysisGraph

global puzzl , t ,j, start

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


def generate_random():
	random.shuffle(LAff)
	start=LAff.copy()
	for i,item in enumerate(LAff):
		start[i] = str(item)
		if item == 0:
			start[i] = '_'
			continue

	start = list(divide_chunks(start, 3))
	return start


def solvable(arr):
    inversions = 0
    for i in range(0, len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if(arr[i] != 0 and arr[j] != 0 and arr[i] > arr[j]):
                inversions += 1

    return inversions % 2 == 0

def solve(start):
	puzz = Puzzle(3)
	goal = [['_','1','2'],['3','4','5'],['6','7','8']]
	try:
		analysis_graph = AnalysisGraph('h1')
		total_path = puzz.process_game(start,goal,analysis_graph)
	#When it's solved
		for item in total_path:

			data = chain.from_iterable(item.data)
			for i,j in enumerate(data):
				if j == '_':
					LAff[i] = 0
					continue
				LAff[i] = int(j)

			for k in range(len(LAff)) :
			    aff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW ,image = Lph[LAff[k]])
			time.sleep(1)
		print("Solved!")
	except:
		return


def draw(liste):
	for k in range(len(liste)) :
		eff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW, image=Lph[0])
		aff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW ,image = Lph[liste[k]])

def check_solvable(LAff):
	sol = solvable(LAff)
	if (sol):
		print("This puzzle is solvable!")
		print("Click on 'Solve' to solve it!")
		return
	else:
		print("Not solvable")
		print("Generate new puzzle please!")
		return
	

def generate_puzzle():
	_start = generate_random()

	for k in range(len(Lph)) :
	    eff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW, image=Lph[0])
	    aff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW ,image = Lph[LAff[k]])
	global start
	start= _start
	check_solvable(LAff)
	return start




def solve_puzzle():
	_thread.start_new_thread(solve,(start,))






j=0
fenetre = Tk()


board = [[1,2,3],[4,5,6],[7,8,0]]

photos=[]
for i in range(0,9):
	photos.append(PhotoImage(file="./images/"+str(i)+".png"))

global Lph , LAff

Lph = photos[0:9]


t= 3

can=Canvas( width=160*t,height=160*t,bg='white')
can.pack( side =TOP, padx =20, pady =20)
fenetre['bg']='white'
fenetre.title (' Taquin resolution IA')



LAff = list([0,1,2,3,4,5,6,7,8])
LAff=[]
for row in board:
    LAff.extend(row)




	







start = generate_puzzle()


# if not solvable(LAff):
# 	print("Not solvable")
# 	print("Generate new puzzle please!")

Button(text='Générer un nouveau puzzle', command=generate_puzzle).pack(side=TOP)

Button(text='Solve', command=solve_puzzle).pack(side=TOP)



can.pack()

fenetre.mainloop()