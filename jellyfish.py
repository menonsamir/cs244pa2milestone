n_switch = 200
n_interswitch_ports = 12
n_server_oports = 24

n_servers = 686

import random
import itertools
from collections import deque, Counter
import matplotlib.pyplot as plt
import pickle
from topology import build_graph
'''
graph = dict()
for i in range(n_switch):
    graph[i] = set()
switches_with_free_port = range(n_switch)

def connect_switches(s1,s2):
    graph[s1].add(s2)
    if len(graph[s1]) == n_interswitch_ports:
        switches_with_free_port.remove(s1)
    graph[s2].add(s1)
    if len(graph[s2]) == n_interswitch_ports:
        switches_with_free_port.remove(s2)

def done_connecting():
    for si in switches_with_free_port:
        for sj in switches_with_free_port:
            if si != sj:
                if si not in graph[sj]:
                    return False
    return True

while True:
    print("outer")
    while True:
        #print(len(switches_with_free_port))
        if len(switches_with_free_port) < 2:
            break
        if done_connecting():
            break
        pair = random.sample(switches_with_free_port, 2)
        s1 = pair[0]
        s2 = pair[1]
        if s2 not in graph[s1]:
            connect_switches(s1, s2)
    sfp = len(switches_with_free_port)
    #if sfp == 0 or ((sfp == 1) and (len(graph[switches_with_free_port[0]]) == n_interswitch_ports-1)):
    #    break # we done
    if sfp < 2:
        break
    
    # get switch with two remaining free ports (p1,p2) - if it only has 1, just drop an existing
    s = switches_with_free_port[0]
    assert(len(graph[s]) > 0)
    if len(graph[s]) == 1:
        drop_target = random.choice(list(graph[s]))
        graph[s].remove(drop_target)
        graph[drop_target].remove(s)
        if drop_target not in switches_with_free_port:
            switches_with_free_port.append(drop_target)
    p1 = graph[s].pop()
    p2 = graph[s].pop()
    # remove random link (x,y)
    x=0
    y=0
    while x == y or y not in graph[x] or x==p1 or x==p2 or y==p1 or y==p2:
        x = random.randint(0, n_switch-1)
        y = random.randint(0, n_switch-1)
    graph[x].remove(y)
    graph[y].remove(x)
    # add (p1,x) and (p2,y)
    graph[p1].add(x)
    graph[x].add(p1)
    graph[p2].add(y)
    graph[y].add(p2)
'''
graph = build_graph(n_switch, n_interswitch_ports, n_server_oports, n_servers)
# assign each server to a switch
switch_of = dict()
switch_to_server = dict()
for i in range(n_switch):
    switch_to_server[i] = set()
    
for i in range(n_servers):
    sw = random.randint(0,n_switch-1)
    while len(switch_to_server[sw]) == n_server_oports:
        sw = random.randint(0,n_switch-1)
    switch_of[i] = sw
    switch_to_server[sw].add(i)

#links = []
#for sw in range(n_switch):
#    links += list(graph[sw])

# now, do path counting
def k_shortest_paths(source, dest, k):
    source = switch_of[source]
    dest = switch_of[dest]
    paths = []
    queue = deque()
    queue.append([source])
    while len(paths) < k and len(queue) > 0:
        path = queue.popleft()
        end = path[-1]
        if end == dest:
            paths.append(path)
        else:
            for neighbor in graph[end] - set(path):
                newpath = path + [neighbor]
                queue.append(newpath)
    return paths

def update_counts_for_paths(paths, name):
    cs = counts[name]
    for p in paths:
        for i in range(len(p)-1):
            s = switch_of[p[i]]
            d = switch_of[p[i+1]]
            if (s,d) not in cs:
                cs[(s,d)] = 0
            cs[(s,d)] += 1

def do_ecmp(send, recv, k):
    paths = k_shortest_paths(send, recv, k)
    if len(paths) == 0:
        print "hmmm"
        return
    min_len = len(paths[0])
    ecmp_paths = []
    i = 0
    while i < len(paths) and len(paths[i]) == min_len:
        ecmp_paths.append(paths[i])
        i += 1
        
    update_counts_for_paths(ecmp_paths, "ecmp"+str(k))

def do_k_shortest(send, recv, k):
    paths = k_shortest_paths(send, recv, k)
    update_counts_for_paths(paths, "kshortest"+str(k))

def do_all(send, recv):
    do_ecmp(send, recv, 8)
    do_ecmp(send, recv, 64)
    do_k_shortest(send, recv, 8)

# choose senders and receivers
names = ["ecmp8", "ecmp64", "kshortest8"]

servers = range(n_servers)
random.shuffle(servers)
counts = dict()
for name in names:
    counts[name] = dict()

z = 0

for i in range(n_servers-1):
    do_all(servers[i], servers[i+1])
    z += 1
    if z % 50 == 0:
        print z
do_all(servers[-1], servers[0])
'''
#counts = pickle.load(open("counts.pkl","r"))
print "done running sim, making viz"
plt.figure()
for name in counts:
    cs = counts[name]
    lens = cs.values()
    freqs = sorted(dict(Counter(lens)).items(), key=lambda z: z[0])
    print "h", name
    freqs = freqs[:18]
    xdata = []
    ydata = []
    x = 0
    for f in freqs:
        y = f[0]
        xdata.append(x)
        ydata.append(y)
        x += f[1]
        xdata.append(x)
        ydata.append(y)
    plt.plot(xdata, ydata, label=name)
    

plt.xlabel("Rank of Link")
plt.ylabel("# Distinct Paths Link is on")
plt.title("Replication")
plt.legend()
plt.savefig('myfilename.png')
'''
