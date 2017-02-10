'''
Created on Feb 7, 2017

@author: XING
'''
import sys
import re

class Graph(object):
    def __init__(self, distDict, neighbors):
        self.distDict = distDict          # dictionary containing distances of every edge
        self.neighbors = neighbors 
        self.nodes = sorted(neighbors.keys())
        self.minNode = self.nodes[0]
        self.maxNode = self.nodes[-1]

class LabelCorrectingAlgorithm(object):
    '''
    classdocs
    '''
    DIAG_CLASS = "LabelCorrectingAlgorithm."
    def __init__(self, alg, inputFile, origin, dest):
        '''
        Constructor: Creates an instance of Label Correcting Algorithm
        '''
        graph = self.loadGraphFile(inputFile)
        if (origin < graph.minNode) or (origin > graph.maxNode):
            raise ValueError('Invalid origin input: not in valid range!')
        if (dest < graph.minNode) or (dest > graph.maxNode):
            raise ValueError('Invalid destination input: not in valid range!')
        self.inputFile = inputFile
        if (alg.lower() == 'dfs'):  
            self.alg = 'DFS'
        elif (alg.lower() == 'bfs'):
            self.alg = 'BFS'
        elif (alg.lower() == 'dijkstra'):
            self.alg = 'Dijkstra'
        elif (alg.lower() == 'slf'):
            self.alg = 'SLF'
        else:
            raise ValueError('Invalid algorithm input')
        self.origin = origin
        self.dest = dest
        self.graph = graph
        self.upper = None
        self.path = None
    
    def loadGraphFile(self, inputFile):
        f = open(inputFile, 'r')
        line = f.readline()
        distDict = {}
        neighbors = {}
        while (line):
            ll = line.rstrip().split(',') 
            startNode = int(ll[0])
            endNode = int(ll[1])
            distance = int(ll[2])
            if not startNode in neighbors:
                neighbors[startNode] = [endNode]
            else:
                neighbors[startNode].append(endNode)
            edge = (startNode, endNode)
            distDict[edge] = distance
            line = f.readline()
        f.close()
        graph = Graph(distDict, neighbors)
        return graph

#     def getUniqueNodes(self, nodesList):
#         setDict = {}
#         map(setDict.__setitem__, nodesList, [])
#         return setDict.keys()
    
    def search(self):
        self.initialize()
        while (len(self.open) > 0):
            i = self.dequeue()
            for j in self.graph.neighbors[i]:
                dist = self.dist2origin[i] + self.graph.distDict[(i, j)]
                #print len(self.open)
                if (dist < self.dist2origin[j]) and (dist < self.upper):
                    self.dist2origin[j] = dist
                    self.pred[j] = i
                    if (j != self.dest):
                        if (j not in self.open):
                            self.enqueue(j)
                    else:
                        self.upper = dist
        self.path = self.getPath()
        self.writeResults()

    def writeResults(self):
        path = '('
        n = len(self.path) - 1
        for k in range(n):
            s = '%d, ' % self.path[k]
            path+=s
        s = '%d)' % self.path[n]
        path += s        
        find = re.compile(r"^[^.]*")
        fileName = re.search(find, self.inputFile).group(0)
        outputFile = 'sol_%s_%d_%d_%s.txt' % (fileName, self.origin, self.dest, self.alg)
        with open(outputFile, 'w') as f:
            f.write('Xing Wang\n')
            f.write('Algorithm: %s\n' % self.alg)
            f.write('Origin: %d\n' % self.origin)
            f.write('Destination: %d\n' % self.dest)
            f.write('Cost: %d\n' % self.upper)
            f.write('Path: %s' % path)
        
    def getPath(self):
        path = []
        nextNode = self.dest
        while (nextNode > -1):
            path.append(nextNode)
            nextNode = self.pred[nextNode]
        path.reverse()
        return path
    
    def dequeue(self):
        if (self.alg == 'DFS'):
            return self.open.pop()
        elif (self.alg == 'BFS'):
            return self.open.pop(0)
        elif (self.alg == 'Dijkstra'):
            smallest = sys.maxint
            for j in self.open:
                if (self.dist2origin[j] < smallest):
                    smallest = self.dist2origin[j]
                    i = j
            self.open.remove(i)
            return i
        #elif (self.alg == 'SLF'):
        
    def enqueue(self, j):
        if (self.alg == 'DFS'):
            self.open.append(j)
        elif (self.alg == 'BFS'):
            self.open.append(j)
        elif (self.alg == 'Dijkstra'):
            self.open.append(j)
        #elif (self.alg == 'SLF'):           
            
    def initialize(self):
        self.dist2origin = [sys.maxint] * (self.graph.maxNode + 1)
        self.dist2origin[self.origin] = 0
        self.pred = [None] * (self.graph.maxNode + 1)
        self.pred[self.origin] = -1
        self.upper = sys.maxint
        self.open = [self.origin]
    
def main():
    if len(sys.argv) == 5:
        inputFile = sys.argv[2]
        if (type(inputFile) != str):
            raise ValueError('Invalid input file name')
    elif len(sys.argv) == 4:
        inputFile = 'RomeData.csv'
    else:
        raise ValueError('Please follow the format: -python LCA.py method inputFile(optional) origin destination')
    alg = sys.argv[1]
    origin = int(sys.argv[-2])
    dest = int(sys.argv[-1])
    lca = LabelCorrectingAlgorithm(alg, inputFile, origin, dest)
    lca.search()
       
    
if __name__ == "__main__":
    main()