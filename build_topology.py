import os
import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.cli import CLI
sys.path.append("../../")
from pox.ext.jelly_pox import JELLYPOX
from subprocess import Popen
from time import sleep, time

from jelly_graph import build_graph, add_servers

#n_switch = 200
#n_interswitch_ports = 12
#n_server_oports = 24
#n_servers = 686

n_switch = 5
n_interswitch_ports = 3
n_server_oports = 5
n_servers = 8

class JellyFishTop(Topo):
    ''' TODO, build your topology here'''
    def build(self):
        
        graph = build_graph(n_switch, n_interswitch_ports, n_server_oports, n_servers)
        serv_switch, switch_serv = add_servers(n_switch, n_server_oports, n_servers)
        print graph, serv_switch

        px_switches = []
        for i in range(n_switch):
            switch = self.addSwitch('s'+str(i))
            px_switches.append(switch)

        links = set()
        for i in range(n_switch):
            for j in graph[i]:
                # to ensure that we don't add a link twice (since they are bidirectional)
                if (i,j) not in links:
                    self.addLink(px_switches[i], px_switches[j])
                links.add((i, j))

        px_servers = []
        for i in range(n_servers):
            server = self.addHost('h'+str(i))
            px_servers.append(server)
            myswitch = serv_switch[i]
            px_myswitch = px_switches[myswitch]
            self.addLink(server, px_myswitch)

        '''
        for i in range(n_servers):
            for j in range(n_servers):
                if i != j:
                    self.addLink(px_servers[i], px_servers[j])
        '''
        
        '''
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )
        '''
        
        


def experiment(net):
    net.start()
    sleep(5)
    net.pingAll()
    net.stop()

def main():
    topo = JellyFishTop()
    net = Mininet(topo=topo, host=CPULimitedHost, link = TCLink, controller=JELLYPOX)
    experiment(net)

if __name__ == "__main__":
    main()

