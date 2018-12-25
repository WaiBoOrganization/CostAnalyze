# -*- coding: utf-8 -*-

import time
import numpy as np
import math
import sys

global PROGRESS

class Node():
    def __init__(self,position,parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.position == other.position
    def is_better_than(self, other):
        return self.g < other.g

def heuristic_estimation(avg,startX,startY,endX,endY):
    return avg*(abs(startX-endX) + abs(startY-endY))

def astar(grids, startX,startY,endX,endY, progressBar):
    global PROGRESS
    PROGRESS=0
    LENGTH=math.sqrt((startX-endX)**2+(startY-endY)**2)
    # startX,startY=startY,startX
    # endX,endY=endY,endX
    time_start = time.clock()
    startNode = Node([startX,startY])
    endNode = Node([endX,endY])
    width = len(grids[0])
    height = len(grids)
    avg = np.mean(np.array(grids))
    path = []
    # initialize the two lists
    open_list = []
    closed_list = []
    open_list.append(startNode)
    total_cost=0
    while open_list:  # end condition 1
        current_node = min(open_list, key=lambda inst:inst.f)
        if current_node == endNode:  # end condition 2
            current = current_node
            total_cost = current.f
            while current is not None:
                path.append([current.position[0],current.position[1]])
                current = current.parent
            path = path[::-1]  # reverse
            find_path = True
            return {"method":'A*', "path": path, "cost": total_cost, "time": (time.clock() - time_start)*1000}
        open_list.remove(current_node)
        closed_list.append(current_node)
        if 1-math.sqrt((current_node.position[0]-endX)**2+(current_node.position[1]-endY)**2)/LENGTH>PROGRESS:
            PROGRESS=1-math.sqrt((current_node.position[0]-endX)**2+(current_node.position[1]-endY)**2)/LENGTH
            progressBar.setValue(int(PROGRESS*100))
        for offset in [[0,1],[0,-1],[1,0],[-1,0]]:
            new_p = [current_node.position[0]+offset[0],current_node.position[1]+offset[1]]
            # out of border
            if new_p[0] < 0 or new_p[0] > width-1 or new_p[1] <0 or new_p[1] > height-1:
                continue
            # not out of border
            new_node = Node(new_p,current_node)
            # if node in closedlist
            if new_node in closed_list:
                continue
            # if node not in closedlist
            # print(grids[current_node.position[1]][current_node.position[0]],grids[new_node.position[1]][new_node.position[0]])
            new_node.g = current_node.g+(grids[current_node.position[1]][current_node.position[0]]
                         + grids[new_node.position[1]][new_node.position[0]])/2
            new_node.h = heuristic_estimation(avg,new_node.position[0],new_node.position[1],endNode.position[0],endNode.position[1])
            new_node.f = new_node.g + new_node.h
            # print(new_node.position,new_node.g,new_node.h)
            # if node already in open_list
            exist_in_openlist = False
            for open_p in open_list:
                if open_p == new_node:
                    exist_in_openlist = True
                    if new_node.is_better_than(open_p):
                        open_p = new_node
                    break
            if not exist_in_openlist:
                open_list.append(new_node)

# matrix
#     x1,x2
# y1  [...]
# y2  [...]

# Looking for four neighborhoods, returning a list,
# where each grid is represented by a tuple
def getNextGrid(xlen,ylen,x, y):
    grids = []
    if x - 1 >= 0:
        grids.append((x - 1, y))
    if x + 1 < xlen:
        grids.append((x + 1, y))
    if y - 1 >= 0:
        grids.append((x, y - 1))
    if y + 1 < ylen:
        grids.append((x , y + 1))
    return grids

def SPFA(matrix,xs,ys,xe,ye, progressBar):
    # xs,ys=ys,xs
    # xe,ye=ye,xe
    global PROGRESS
    PROGRESS=0
    LENGTH = math.sqrt((xs - xe) ** 2 + (ys - ye) ** 2)
    startTime=time.clock()
    xlen=len(matrix[0])
    ylen=len(matrix)
    costMatrix=[([sys.maxsize]*len(matrix[0])) for i in range(len(matrix))]
    costMatrix[ys][xs]=0
    pathMatrix=[([[]]*len(matrix[0])) for i in range(len(matrix))]
    pathMatrix[ys][xs]=[(xs,ys)]
    queue=[] # Use a list to simulate a queue for easy viewing of elements
    queue.append((xs,ys))# The grid in the queue is represented by a tuple
    while len(queue)>0:
        g=queue[0]
        del queue[0]
        gList = getNextGrid(xlen, ylen, g[0], g[1])
        # Relaxing the end point of all sides of the g-grid connection
        for i in gList:
            if 1 - math.sqrt((i[1] - xe) ** 2 + (
                    i[0] - ye) ** 2) / LENGTH > PROGRESS:
                PROGRESS = 1 - math.sqrt(
                    (i[1] - xe) ** 2 + (i[0] - ye) ** 2) / LENGTH
                progressBar.setValue(int(PROGRESS*100))
            tmpCost=costMatrix[g[1]][g[0]]+\
                                   matrix[g[1]][g[0]]/2+matrix[i[1]][i[0]]/2
            if tmpCost<costMatrix[i[1]][i[0]]:
                costMatrix[i[1]][i[0]]=tmpCost
                pathMatrix[i[1]][i[0]]=pathMatrix[g[1]][g[0]]+[i]
                if i not in queue:
                    queue.append(i)
    t=(time.clock()-startTime)*1000
    path=[]
    for i in pathMatrix[ye][xe]:
        path.append([i[0],i[1]])
    map={"method":'SPFA', 'path':path,'cost':costMatrix[ye][xe],'time':t}
    return map

def SLF(matrix,xs,ys,xe,ye, progressBar):
    # xs, ys = ys, xs
    # xe, ye = ye, xe
    global PROGRESS
    PROGRESS = 0
    LENGTH = math.sqrt((xs - xe) ** 2 + (ys - ye) ** 2)
    startTime=time.clock()
    xlen=len(matrix[0])
    ylen=len(matrix)
    costMatrix=[([sys.maxsize]*len(matrix[0])) for i in range(len(matrix))]
    costMatrix[ys][xs]=0
    pathMatrix=[([[]]*len(matrix[0])) for i in range(len(matrix))]
    pathMatrix[ys][xs]=[(xs,ys)]
    queue=[]
    queue.append((xs,ys))
    while len(queue)>0:
        g=queue[0]
        del queue[0]
        gList = getNextGrid(xlen, ylen, g[0], g[1])
        for i in gList:
            if 1 - math.sqrt((i[1] - xe) ** 2 + (
                    i[0] - ye) ** 2) / LENGTH > PROGRESS:
                PROGRESS = 1 - math.sqrt(
                    (i[1] - xe) ** 2 + (i[0] - ye) ** 2) / LENGTH
                progressBar.setValue(int(PROGRESS*100))
            tmpCost=costMatrix[g[1]][g[0]]+\
                                   matrix[g[1]][g[0]]/2+matrix[i[1]][i[0]]/2
            if tmpCost<costMatrix[i[1]][i[0]]:
                costMatrix[i[1]][i[0]]=tmpCost
                pathMatrix[i[1]][i[0]]=pathMatrix[g[1]][g[0]]+[i]
                if i not in queue:
                    # The original queue was changed to a double-ended queue
                    # For a point u to be added to the queue,
                    # if dis[u] is less than the dis[v] of the head element v
                    # Then join the first element of the team, otherwise join the end of the team
                    if len(queue)>0 and tmpCost<costMatrix[queue[0][1]][queue[0][0]]:
                        queue.insert(0,i)
                    else:
                        queue.append(i)
    t=(time.clock()-startTime)*1000
    path=[]
    for i in pathMatrix[ye][xe]:
        path.append([i[0],i[1]])
    map={"method":'SLF', 'path':path,'cost':costMatrix[ye][xe],'time':t}
    return map

def LLL(matrix,xs,ys,xe,ye, progressBar):
    # xs, ys = ys, xs
    # xe, ye = ye, xe
    global PROGRESS
    PROGRESS = 0
    LENGTH = math.sqrt((xs - xe) ** 2 + (ys - ye) ** 2)
    startTime=time.clock()
    xlen=len(matrix[0])
    ylen=len(matrix)
    costMatrix=[([sys.maxsize]*len(matrix[0])) for i in range(len(matrix))]
    costMatrix[ys][xs]=0
    pathMatrix=[([[]]*len(matrix[0])) for i in range(len(matrix))]
    pathMatrix[ys][xs]=[(xs,ys)]
    queue=[]
    queue.append((xs,ys))
    while len(queue)>0:
        # For each element u to be dequeued, compare the average of dis[u] and dis in the queue
        # If dis[u] is larger, then pop it to the end of the team and take the first element of the team for repeated judgment.
        # Until dis[u] is less than the average
        avg=0
        for i in queue:
            avg+=costMatrix[i[1]][i[0]]
        avg/=len(queue)
        while True:
            if costMatrix[queue[0][1]][queue[0][0]]>avg:
                queue.append(queue[0])
                del queue[0]
            else:
                break
        g=queue[0]
        del queue[0]
        gList = getNextGrid(xlen, ylen, g[0], g[1])
        for i in gList:
            if 1 - math.sqrt((i[1] - xe) ** 2 + (
                    i[0] - ye) ** 2) / LENGTH > PROGRESS:
                PROGRESS = 1 - math.sqrt(
                    (i[1] - xe) ** 2 + (i[0] - ye) ** 2) / LENGTH
                progressBar.setValue(int(PROGRESS*100))
            tmpCost=costMatrix[g[1]][g[0]]+\
                                   matrix[g[1]][g[0]]/2+matrix[i[1]][i[0]]/2
            if tmpCost<costMatrix[i[1]][i[0]]:
                costMatrix[i[1]][i[0]]=tmpCost
                pathMatrix[i[1]][i[0]]=pathMatrix[g[1]][g[0]]+[i]
                if i not in queue:
                    queue.append(i)
    t=(time.clock()-startTime)*1000
    path=[]
    for i in pathMatrix[ye][xe]:
        path.append([i[0],i[1]])
    map={"method":'LLL', 'path':path,'cost':costMatrix[ye][xe],'time':t}
    return map

def SLFandLLL(matrix,xs,ys,xe,ye, progressBar):
    # xs, ys = ys, xs
    # xe, ye = ye, xe
    global PROGRESS
    PROGRESS = 0
    LENGTH = math.sqrt((xs - xe) ** 2 + (ys - ye) ** 2)
    startTime=time.clock()
    xlen=len(matrix[0])
    ylen=len(matrix)
    costMatrix=[([sys.maxsize]*len(matrix[0])) for i in range(len(matrix))]
    costMatrix[ys][xs]=0
    pathMatrix=[([[]]*len(matrix[0])) for i in range(len(matrix))]
    pathMatrix[ys][xs]=[(xs,ys)]
    queue=[]
    queue.append((xs,ys))
    while len(queue)>0:
        avg = 0
        for i in queue:
            avg += costMatrix[i[1]][i[0]]
        avg /= len(queue)
        while True:
            if costMatrix[queue[0][1]][queue[0][0]] > avg:
                queue.append(queue[0])
                del queue[0]
            else:
                break
        g=queue[0]
        del queue[0]
        gList = getNextGrid(xlen, ylen, g[0], g[1])
        for i in gList:
            if 1 - math.sqrt((i[1] - xe) ** 2 + (
                    i[0] - ye) ** 2) / LENGTH > PROGRESS:
                PROGRESS = 1 - math.sqrt(
                    (i[1] - xe) ** 2 + (i[0] - ye) ** 2) / LENGTH
                progressBar.setValue(int(PROGRESS*100))
            tmpCost=costMatrix[g[1]][g[0]]+\
                                   matrix[g[1]][g[0]]/2+matrix[i[1]][i[0]]/2
            if tmpCost<costMatrix[i[1]][i[0]]:
                costMatrix[i[1]][i[0]]=tmpCost
                pathMatrix[i[1]][i[0]]=pathMatrix[g[1]][g[0]]+[i]
                if i not in queue:
                    if len(queue)>0 and tmpCost<costMatrix[queue[0][1]][queue[0][0]]:
                        queue.insert(0,i)
                    else:
                        queue.append(i)
    t=(time.clock()-startTime)*1000
    path=[]
    for i in pathMatrix[ye][xe]:
        path.append([i[0],i[1]])
    map={"method":'SLF&LLL', 'path':path,'cost':costMatrix[ye][xe],'time':t}
    return map

