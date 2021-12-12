# Final Skeleton
#
# Reminders:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pdb

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    

    
    ip = packet.find('ipv4')
    ap = packet.find('arp')
    if ip is not None:
      ic = packet.find('icmp')
      tp = packet.find('tcp')
      up = packet.find('udp')
      src = packet.payload.srcip
      dst = packet.payload.dstip
      #port assignment start
      if switch_id==1:
        if dst == '10.0.1.10':
          port = 1
        elif dst == '10.0.2.10':
          port = 2
        else:
          port = 3
      elif switch_id==2:
        if dst == '10.0.3.10':
          port = 1
        elif dst == '10.0.4.10':
          port = 2
        else:
          port = 3
      elif switch_id==3:
        if dst == '10.0.5.10':
          port = 1
        elif dst == '10.0.6.10':
          port = 2
        else:
          port = 3
      elif switch_id==4:
        if dst == '10.0.7.10':
          port = 1
        elif dst == '10.0.8.10':
          port = 2
        else:
          port = 3
      elif switch_id==6:
        if dst == '10.0.9.10':
          port = 1
        else:
          port = 3
      elif switch_id==5:
        if dst == '10.0.10.10':
          port = 5
        elif dst == '10.0.1.10' or dst == '10.0.2.10':
          port = 1
        elif dst == '10.0.3.10' or dst == '10.0.4.10':
          port = 2
        elif dst == '10.0.5.10' or dst == '10.0.6.10':
          port = 3
        elif dst == '10.0.7.10' or dst == '10.0.8.10':
          port = 4
        elif dst == '10.0.9.10':
          port = 6
      #port assignment end
      #
      #if packet is icmp and packet did not come from untrusted host send
      if ic is not None and src != '10.0.10.10':
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, port_on_switch)
        msg.match.dl_type = 0x0800
        msg.match.nw_protocol = 1
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.data = packet_in
        msg.actions.append(of.ofp_action_output(port = port))
        self.connection.send(msg) 
      #if tcp, and if it doesn't go from untrusted to server1 or if it isn't comming from untrusted host send
      elif tp is not None:
        if (src != '10.0.10.10') or (src == '10.0.10.10' and dst != '10.0.9.10'):
          #print "source: "
          #print src
          #print "destination: "
          #print dst
          msg = of.ofp_flow_mod()
          msg.match = of.ofp_match.from_packet(packet, port_on_switch)
          msg.match.dl_type = 0x0800
          msg.match.nw_protocol = 6
          msg.idle_timeout = 10
          msg.hard_timeout = 30
          msg.data = packet_in
          msg.actions.append(of.ofp_action_output(port = port))
          self.connection.send(msg)
      #if udp and if it doesn't go from untrusted to server1 or if it isn't coming from the untrusted host send
      elif up is not None:
        if (src == '10.0.10.10' and dst != '10.0.9.10') or (src != '10.0.10.10'):
          msg = of.ofp_flow_mod()
          msg.match = of.ofp_match.from_packet(packet, port_on_switch)
          msg.match.dl_type = 0x0800
          msg.match.nw_protocol = 17
          msg.idle_timeout = 10
          msg.hard_timeout = 30
          msg.data = packet_in
          msg.actions.append(of.ofp_action_output(port = port))
          self.connection.send(msg)
    elif ap is not None:
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet, port_on_switch)
      msg.match.dl_type = 0x0806
      msg.idle_timeout = 10
      msg.hard_timeout = 30
      msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)
   
  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
