import random
def build_graph(n_switch, n_interswitch_ports, n_server_oports, n_servers):
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
    return graph
