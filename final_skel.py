#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    
    #hosts 10 through 80
    h10 = self.addHost('h10',ip='10.0.1.10', defaultRoute="h10-eth0")
    h20 = self.addHost('h20',ip='10.0.2.10', defaultRoute="h20-eth0")
    h30 = self.addHost('h30',ip='10.0.3.10', defaultRoute="h30-eth0")
    h40 = self.addHost('h40',ip='10.0.4.10', defaultRoute="h40-eth0")
    h50 = self.addHost('h50',ip='10.0.5.10', defaultRoute="h50-eth0")
    h60 = self.addHost('h60',ip='10.0.6.10', defaultRoute="h60-eth0")
    h70 = self.addHost('h70',ip='10.0.7.10', defaultRoute="h70-eth0")
    h80 = self.addHost('h80',ip='10.0.8.10', defaultRoute="h80-eth0")

    #server and untrusted server
    #NOTE: When using subnet mask node was unreachable
    #NOTE: 172 ip address not working so changed to a 10.x.x address
    server1 = self.addHost('h100',ip='10.0.9.10', defaultRoute="h100-eth0")
    untrusted = self.addHost('h110',ip='10.0.10.10', defaultRoute="h110-eth0")

    #floor switches
    # Create a switch. No changes here from Lab 1.
    f1s1 = self.addSwitch('s1')
    f1s2 = self.addSwitch('s2')
    f2s1 = self.addSwitch('s3')
    f2s2 = self.addSwitch('s4')
    
    #data center switch and core switch
    cs = self.addSwitch('s5')
    dcs = self.addSwitch('s6')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.

    #host to switch connections
    self.addLink(h10, f1s1, port1=1, port2=1)
    self.addLink(h20, f1s1, port1=1, port2=2)
    self.addLink(h30, f1s2, port1=1, port2=1)
    self.addLink(h40, f1s2, port1=1, port2=2)
    self.addLink(h50, f2s1, port1=1, port2=1)
    self.addLink(h60, f2s1, port1=1, port2=2)
    self.addLink(h70, f2s2, port1=1, port2=1)
    self.addLink(h80, f2s2, port1=1, port2=2)    
    self.addLink(untrusted, cs, port1=1, port2=5)
    self.addLink(server1, dcs, port1=1, port2=1)

    #switch to switch connections
    self.addLink(f1s1, cs, port1=3, port2=1)
    self.addLink(f1s2, cs, port1=3, port2=2)
    self.addLink(f2s1, cs, port1=3, port2=3)
    self.addLink(f2s2, cs, port1=3, port2=4)
    self.addLink(dcs, cs, port1=3, port2=6)
    
  


    #source port alwauys equals destination port
    #if source port is 10 then we know that it came from untrusted


def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  #h10, h20, h30, h40, h50, h60, h70, h80, server1, untrusted = net.get('h10', 'h20', 'h30', 'h40', 'h50', 'h60', 'h70', 'h80','h100', 'h110')
  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
