import time
import re
import sys

def main():
    assert len(sys.argv) == 4
    in_file = sys.argv[1]
    n0 = int(sys.argv[-2]) # origin: node 0
    z = int(sys.argv[-1])  # destination: node z
    
    #Read the input file
    f = open(in_file, 'r')
    costs = {}
    nbs = {}
    for line in f:
        l = line.rstrip().split(',')
        v = int(l[0]) # n0
        w = int(l[1]) # end
        costs[(v, w)] = int(l[2])
        if (v in nbs) == False:
            nbs[v] = [w]
        else:
            nbs[v].append(w)
    f.close()
    
    it = 0
    start_time = time.time()
    
    N = sorted(nbs.keys())[-1]
    d = []
    #touched = []
    pred = []
    for i in range(N+1):
        d.append(sys.maxint)
        pred.append(None)
#         touched.append(0)
    d[n0] = 0
    pred[n0] = -1
    #upper = sys.maxint
    upper = 800000
    open_list = [n0]
#     nodes = [n0]
    while len(open_list)>0:
        i = open_list.pop()
        it = it + 1
        for j in nbs[i]:
#             if j not in nodes:
#                 nodes.append(j)
            if d[i]+costs[(i, j)] < min(d[j], upper):
                d[j] = d[i]+costs[(i, j)]
                pred[j] = i
#                 touched[i] = 1
                if j != z:
                    if j not in open_list:
                        open_list.append(j)
                else:
                    upper = d[i]+costs[(i, j)]
                    
    # record some results
    print 'running time: %.4f seconds' % (time.time() - start_time)
    print 'Iterations: %d' % it
    
    # get the shortest path from pred                
    path = []
    i = z
    while i != -1:
        path.append(i)
        i = pred[i]
    path.reverse()
    
    # record some results
    print 'Cost of shortest path: %d' % upper
    print 'Number of steps: %d' % (len(path))        
#     print 'Distinct nodes: %d' % (len(nodes))

    # follow the format to output path
    path_str = '('
    for i in range(len(path) - 1):
        path_str = path_str + '%d, '%path[i]
    path_str = path_str + '%d)'%path[len(path)-1]
    
    # Write results to output file as required
    fname = re.search(re.compile(r"^[^.]*"), in_file).group(0)
    outputFile = 'sol_%s_%d_%d_DFS.txt'%(fname, n0, z)
    f = open(outputFile, 'w')
    f.write('Qiong Hu and Zhenying Huang\n')
    f.write('Algorithm: DFS\n')
    f.write('Origin: %d\n'%n0)
    f.write('Destination: %d\n'%z)
    f.write('Cost: %d\n'%upper)
    f.write('Path: %s'%path_str)
    
if __name__ == "__main__":
    main()