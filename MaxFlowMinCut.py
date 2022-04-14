"""
    name:  Ryan Gross

"""

# All modules for CS 412 must include a main method that allows it
# to imported and invoked from other python scripts

#augmenting path is passed residual graph
import sys
import copy
def main():
    tmp = input().split()
    num_vert = int(tmp[0])
    num_edge = int(tmp[1])

    G = {}
    copy_G = {}
    for x in range(num_vert):
        G[x] = {}
        copy_G[x] = {}

    #{Vert: {edge: (flow,capacity)}}
    for x in range(num_edge):
        tmp = input().split()
        G[int(tmp[0])].update({int(tmp[1]):(0,int(tmp[2]))})
        copy_G[int(tmp[0])].update({int(tmp[1]):(0,int(tmp[2]))})
    #print (G)
    #createResidualGraph(G)

    flow ,gF = FordFulkerson(G)
    print(flow)
    min_cuts = sorted(findMinCut(copy_G,gF))
    for x in min_cuts:
        print (x[0],x[1])

def FordFulkerson(G):
    #Inital Flow to 0
    p,bool = findAugmentingPath(G)  #p = bfs(G,0,len(G)-1)
    flow = 0
    while bool:
        #augment flow 
        min_cap = sys.maxsize
        for x in range(len(p)-1):
            if G[p[x]][p[x+1]][1] < min_cap: #capacities [20,5,15]
                min_cap = G[p[x]][p[x+1]][1] #min_cap 5 

        #print (min_cap)
        for x in range(len(p)-1):
            G[p[x]][p[x+1]] = (min_cap,G[p[x]][p[x+1]][1]) #set flow on these path edges to min_cap on original path
        flow += min_cap
        #print(G, " this is original graph with flows")
        gF = createResidualGraph(G,p)
        p,bool = findAugmentingPath(gF) #p = bfs(gF,0,len(gF)-1)
    return flow,gF

def createResidualGraph(G,path):#createResidualGraph(G,path) just capacity? #residual capacity
    residual_G = G.copy()
    #then add back edge of flow
    for x in range(len(path)-1): #[0,1,3,5]
        #if flow = edge cap then switch direction
        flow = residual_G[path[x]][path[x+1]][0] #{vert(u): {edge(v): (flow,cap)}}
        cap = residual_G[path[x]][path[x+1]][1]
        if flow == cap:
            residual_G[path[x+1]].update({path[x]:(0,flow)}) #update key resid[1][0](0,flow)
            del residual_G[path[x]][path[x+1]]# del dict[0][key:1]
        else:
            residual_G[path[x+1]].update({path[x]:(0,flow)}) #add back edge from 1 -> 0 with cap(0->1) - min_cap
            residual_G[path[x]].update({path[x+1]:(0,cap-flow)}) #update edge 0->1 to edit cap to be cap(0->1) - min_cap

    return residual_G
    

def findAugmentingPath(graph):
    path = bfs(graph,0,len(graph)-1)
    return path
    
def findMinCut(G,res_graph):
    #find all reachable nodes from s in the final residual graph
    S = reachable(res_graph,0) #[0,1,2] S
    #all edges that go from a reachable vertex to a non-reachable vertex are min cut edges
    T = reachable(res_graph,len(res_graph)-1) #[5,3,4] T
    T = set(T) - set(S)
    min_Cut = []

    for u in S: #[0,1,2]
        for v in T: #[5,3,4]
            if (v not in res_graph[u]) and (v in G[u]):
                min_Cut.append((u,v))

    return min_Cut

def reachable(graph,s):
    visited = []
    queue = []
    queue.append(s)
    visited.append(s)
    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if v not in visited:
                queue.append(v)
                visited.append(v)
    return visited


def bfs( graph, start, end): #when u->v turns to v->u bfs will work and path will change
    queue = [(start,[start])]
    visited = set()

    while queue:
        vertex, path = queue.pop(0)
        visited.add(vertex)
        for node in graph[vertex]:
            if node == end:
                return path + [end],True
            else:
                if node not in visited:
                    visited.add(node)
                    queue.append((node, path + [node]))
    
    return [],False


if __name__ == "__main__":
    main()