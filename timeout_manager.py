from pox.core import core  
# import POX core module (used to register controller and logging)
import pox.openflow.libopenflow_01 as of  
# import OpenFlow 1.0 library (POX mainly uses OF 1.0)
log = core.getLogger()  
# logger to print messages in POX terminal

class FinalController(object):  
# main controller class
    def __init__(self):
        self.blocked_once = False  
        # flag to ensure blocking happens only once
        core.openflow.addListeners(self)  
        # register this class to listen for OpenFlow events

    def _handle_ConnectionUp(self, event):  
    # called when switch connects to controller
        msg = of.ofp_flow_mod()  
        # create flow rule message
        msg.priority = 0  
        # lowest priority → table-miss rule
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))  
        # send all unmatched packets to controller
        event.connection.send(msg)  
        # send flow rule to switch
        log.info("Table-miss rule installed")  
        # print log

    def _handle_PacketIn(self, event):  
    # triggered when packet comes to controller
        packet = event.parsed  
        # parsed packet (not used much here, but needed usually)
        in_port = event.port  
        # port from which packet came
        if in_port == 1 and not self.blocked_once:  
        # if packet is from port 1 AND we haven’t blocked before
            log.info("BLOCKING h1 TRAFFIC")  
            # print blocking message
            msg = of.ofp_flow_mod()  
            # create new flow rule
            msg.priority = 10  
            # higher priority than table-miss
            msg.match.in_port = 1  
            # match packets coming from port 1
            msg.hard_timeout = 10  
            # rule expires after 10 seconds
            # no actions → means DROP rule
            # (important: empty actions list = drop traffic)
            event.connection.send(msg)  
            # send drop rule to switch
            self.blocked_once = True  
            # ensure blocking happens only once
            return  
            # stop further processing

        msg = of.ofp_packet_out()  
        # create packet out message
        msg.data = event.ofp  
        # original packet data
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  
        # flood packet to all ports
        event.connection.send(msg)  
        # send packet to switch

    def _handle_FlowRemoved(self, event):  
    # triggered when flow expires (if supported)
        log.info("FLOW EXPIRED")  
        # print expiration message

def launch():  
# starting point of POX controller
    core.registerNew(FinalController)  
    # register and start controller