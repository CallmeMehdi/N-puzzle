from utils import PriorityQueue

class Node:
    def __init__(self,data,level,fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x,y = self.find(self.data,'_')
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data,x,y,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        return children
        
    def shuffle(self,puz,x1,y1,x2,y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
            

    def copy(self,root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self,puz,x):
        """ Specifically used to find the position of the blank space """
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j


class Puzzle:
    def __init__(self,size):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """ Accepts the puzzle from the user """
        puz = []
        for i in range(0,self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def reconstract_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def f(self,start,goal, heuristic):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return heuristic(start.data,goal)+start.level

    #Misplaced tiles heuristic function
    def h1(self,start,goal):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp
     
    #Manhattan distance heuristic function
    def h2(self,start,goal):
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                val = start[i][j]
                correct_position = [(index, row.index(start[i][j])) for index, row in enumerate(goal) if start[i][j] in row]
                temp += abs(i - correct_position[0][0]) + \
                abs(j - correct_position[0][1])
        return temp

    def identical(self,start,goal):
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':  
                    return False
        return True

    #CLI process
    def process(self):
        """ Accept Start and Goal Puzzle state"""
        print("Entrer la matrice initiale du jeu de taquin \n")
        start = self.accept()
        print("Entrer la matrice finale à atteindre \n")        
        goal = self.accept()
        print("Choisir votre fonction heuristique: \n")
        choice = None
        while choice !='1' and choice!='2':
            if (choice):
                print('Veuillez choisir un choix valable!\n\n')
            print("1* Nombres de pieces mal placées")
            print("2* Somme de la distance Manhattan")
            choice = input()
        if (choice=='1'):
            heuristic = self.h1
        else:
            heuristic = self.h2

        print(type(start))
        print(start)
        print(goal)
        start = Node(start,0,0)
        start.fval = self.f(start,goal, heuristic)
        """ Put the start node in the open list"""
        self.open.append(start)
        self.open_set = PriorityQueue()
        self.closed_set = set()
        self.open_set.add_task(start, priority=start.fval)
        print("\n\n")
        came_from = {}

        cur = self.open_set.pop_task()
        
        while True:
            try:
                data =  [''.join(idx for idx in sub) for sub in cur.data ] 
                data = ''.join(map(str, data))
                self.closed_set.add(data)
                """ If the difference between current and goal node is 0 we have reached the goal node"""
                if(self.identical(cur.data,goal)):
                    total_path = self.reconstract_path(came_from, cur)
                    #Print out the results
                    for i in total_path:
                        print("")
                        print("  | ")
                        print("  | ")
                        print(" \\\'/ \n")
                        for k in i.data:
                            for j in k:
                                print(j,end=" ")
                            print("")               
                    print('Résolue apres '+str(len(total_path)-1)+' etats \n')
                    print("")
                    print("Cet algorithme a parcouru " + str(len(self.closed_set)) + " etats \n")
                    return total_path

                for i in cur.generate_child():
                    data =  [''.join(idx for idx in sub) for sub in i.data ] 
                    data = ''.join(map(str, data))
                    if data in self.closed_set:
                        continue
                    i.fval = self.f(i,goal, heuristic)
                    # for node in self.open:
                    #     if node.data == i.data:
                    #         self.open.remove(node)

                    self.open_set.add_task(i, priority=i.fval)
                    came_from[i] = cur
                   # self.open.append(i)
                self.closed.append(cur)
                #del self.open[0]

                cur = self.open_set.pop_task()
            except:
                print('This puzzle is not solvable!')
                break



    #GUI process
    def process_game(self, start, goal, analysis_graph = None):
        print("Choisir votre fonction heuristique: \n")
        choice = None
        while choice !='1' and choice!='2':
            if (choice):
                print('Veuillez choisir un choix valable!\n\n')
            print("1* Nombres de pieces mal placées")
            print("2* Somme de la distance Manhattan")
            choice = input()
        if (choice=='1'):
            heuristic = self.h1
        else:
            heuristic = self.h2

        print(type(start))
        print(start)
        print(goal)
        start = Node(start,0,0)
        start.fval = self.f(start,goal, heuristic)
        """ Put the start node in the open list"""
        self.open.append(start)
        self.open_set = PriorityQueue()
        self.closed_set = set()
        self.open_set.add_task(start, priority=start.fval)
        print("\n\n")
        came_from = {}

        cur = self.open_set.pop_task()
        
        while True:
            data =  [''.join(idx for idx in sub) for sub in cur.data ] 
            data = ''.join(map(str, data))
            self.closed_set.add(data)
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if(self.identical(cur.data,goal)):
                total_path = self.reconstract_path(came_from, cur)
                if analysis_graph:
                    if heuristic == self.h2:
                        analysis_graph.name="h2"
                    analysis_graph.update_graph(len(total_path), len(self.closed_set))
                print('Résolue apres '+str(len(total_path)-1)+' etats \n')
                print("")
                print("Cet algorithme a parcouru " + str(len(self.closed_set)) + " etats \n")
                return total_path

            for i in cur.generate_child():
                data =  [''.join(idx for idx in sub) for sub in i.data ] 
                data = ''.join(map(str, data))
                if data in self.closed_set:
                    continue
                i.fval = self.f(i,goal, heuristic)
                # for node in self.open:
                #     if node.data == i.data:
                #         self.open.remove(node)

                self.open_set.add_task(i, priority=i.fval)
                came_from[i] = cur
               # self.open.append(i)
            self.closed.append(cur)
            #del self.open[0]

            cur = self.open_set.pop_task()

        


#puz = Puzzle(3)
#puz.process()

