from copy import deepcopy 
from colorama import Fore, Back, Style 
import time 

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'


bar = Style.BRIGHT + Fore.GREEN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'


first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL

def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)

class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
       
        
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h
       

def get_pos(current_state, element):
    
    
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))
      
def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
           
            cost += abs(row - pos[0]) + abs(col - pos[1])
           
    return cost

#get adjucent Nodes
def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            
            newState = deepcopy(node.current_node)
            
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            
            newState[newPos[0]][newPos[1]] = 0
           

           
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))


    return listNode
   


def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
          
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    # returns the node with the best evaluation function found during the loop.        
    return bestNode

#this functionn create the smallest path
def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()
   

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()
    

    return branch


def main(puzzle):
   
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    
    closed_set = {}

    while True:
        
        test_node = getBestNode(open_set)
        
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            
            return buildPath(closed_set)
        
        adj_node = getAdjNode(test_node)
        
        for node in adj_node:
          
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f():
             
                continue
           
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

def is_solvable(puzzle):
   
    flattened_puzzle = [num for row in puzzle for num in row if num != 0]
   
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] > flattened_puzzle[j]:
                inversions += 1
  
    return inversions % 2 == 0

if __name__ == '__main__':
    def get_initial_state():
        print("Enter the initial state of the puzzle (use 0 for the blank space):")
        initial_state = []
        encountered_numbers = set()
        total_numbers = 0 
        for i in range(3):
            row = []
            while len(row) < 3:
                user_input = input(f"Enter number for row {i+1}, column {len(row)+1}: ")
                
                if user_input == '':
                    print("Error: Please enter a number.")
                    continue  
                num = int(user_input)
               
                if num < 0 or num > 8:
                    print("Error: Numbers must be in the range of 0 to 8.")
                    continue  
                elif num in encountered_numbers:
                    print("Error: Each number must be unique.")
                    continue  
                else:
                    row.append(num)
                    encountered_numbers.add(num)
                    total_numbers += 1 
            
            initial_state.append(row)

        if total_numbers != 9:
            print("Error: You entered less than or more than 9 numbers.")
            return None

        return initial_state

    initial_state = get_initial_state()
    if initial_state is None:
        exit()

    if not is_solvable(initial_state):
        print("The puzzle is not solvable.")
    else:
        start_time = time.time()
        br = main(initial_state)
        end_time = time.time()

        print()
        print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
        for b in br:
            if b['dir'] != '':
                letter = ''
                if b['dir'] == 'U':
                    letter = 'UP'
                elif b['dir'] == 'R':
                    letter = "RIGHT"
                elif b['dir'] == 'L':
                    letter = 'LEFT'
                elif b['dir'] == 'D':
                    letter = 'DOWN'
                print(dash + dash + right_junction, letter, left_junction + dash + dash)
            print_puzzle(b['node'])
            print()

        print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)
        print('Total number of steps:', len(br) - 1)
        print('Total amount of time in search:', end_time - start_time, 'seconds')