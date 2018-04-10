import packages.mscl as mscl
import packages.thingworx as thingworx

import ast

def getNode(node_obj, addr):
    # Check Node Address against addresses of each node object
    # returning the match
    for n in node_obj:
        if str(n.getNodeAddr()) == str(addr):
            return n
    return None


def parseData(sweeps, node_obj, config):
    # Each data sweep contains minimal data
    # The node.getDataFromSweep(sweep) method for each node object
    # can be written to parse the sweep in the correct way for
    # the node type
    for sweep in sweeps:
        addr = sweep.nodeAddress()
        node = getNode(node_obj, addr)
        if node is not None:
            node.getDataFromSweep(sweep, config)
        else:
            print("error finding associated node for data sweep")


def connectToBaseStation(com_port, baud_rate):
    # Create connection to com port and create a new base station
    conn = mscl.Connection.Serial(com_port, int(baud_rate))
    bs = mscl.BaseStation(conn)
    print("Connect base station: " + com_port + " " + baud_rate)
    return bs


def connectToNode(node_addr, bs):
    # Add a new node to the base station
    node = mscl.WirelessNode(int(node_addr), bs)
    print("Connect node: " + node_addr)
    return node


##########################
# This class, NodeTemplate provides the base for any node connected
# to the Base Station.  They share the following properties:
#   - node_addr     - address of node i.e. 59906
#   - node_type     - type of node i.e. temperature, force
#   - thing_name    - name the node will have in Thing Worx
#   - properties    - dictionary object of properties
#
# The properties object varies by device.  Some devices have
# channels and others do not, some ahve multiple values and others
# don't.
#
# The shared methods of the NodeTemplate are as follows:
#   - connectNode(<baseStation>)        - connect the node to a base station
#   - sendData(<propertyName>, <data>)  - send data to thingworx server
#   - createThing()     - create a thing for the node on thingworx
#   - cleanUp()         - clean up node connection to base station
#   - getNodeAddr()     - returns node address
#   - getNodeType()     - returns node type
##########################
class NodeTemplate:
    def __init__(self, node_addr, node_type, thing_name, properties):
        self.node_addr = node_addr
        self.node_type = node_type
        self.node = None
        self.thing_name = thing_name
        # Properties come in as a string formatted like a python dictionary,
        # which is converted to an actual python dict object
        self.properties = ast.literal_eval(properties)

    def connectNode(self, bs):
        self.node = mscl.WirelessNode(int(self.node_addr), bs)
        print("Connect node: " + self.node_addr)
        return self.node

    def sendData(self, prop, data, config):
        return thingworx.putDataToThing(self.thing_name, prop, data, config)

    def createThing(self, config):
        # Creating a thing involves creating a thing base on a template (remoteThing)
        # and then adding each property to it
        # 
        # Each property requires a name and a data type (NUMBER, STRING, etc.)
        thingworx.createThing(self.thing_name, config)
        for p in self.properties:
            thingworx.addPropertyToThing(self.thing_name, p["name"], p["type"], config)

    def cleanUp(self):
        print("Cleaning up node: " + self.node_addr)
        status = self.node.setToIdle()
        while not status.complete(300):
            print(".")
        result = status.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Set " + self.node_addr + " to idle")
        elif result == mscl.SetToIdleStatus.canceled:
            print("Setting " + self.node_addr + " to idle cancelled")
        else:
            print("Setting " + self.node_addr + " to idle failed")

    def getNodeAddr(self):
        return self.node_addr

    def getNodeType(self):
        return self.node_type


########################
# Temperature Node
#
# This node contains two properties:
#   - Channel 1 (ch1), Probe Temperature
#   - Channel 7 (ch7), Internal Temperature
#
# This node requires a get data method:
#   - getDataFromSweep(<sweep>)
#
# The section in config.json for a temperature node should look like this:
# {
#   "address": 56609,
#   "type": "temp",
#   "thing_name": "thingName",
#   "thing_properties": [
#       {
#           "name": "probe",
#           "channel": "ch1",
#           "type": "NUMBER"
#       }, {
#           "name": "probe",
#           "channel": "ch1",
#           "type": "NUMBER"
#       }]
# }
########################
class TempNode(NodeTemplate):
    def __init__(self, node_addr, node_type, thing_name, properties):
        NodeTemplate.__init__(self, node_addr, node_type, thing_name, properties)

    def getDataFromSweep(self, sweep, config):
        # Get each data point from the sweep
        for dataPoint in sweep.data():
            # A DataPoint Object has these two properties:
            #   - channel (channelName())
            #   - value (as_float())
            chan = dataPoint.channelName()
            val = dataPoint.as_float()
            if val is not None:
                prop = None
                # Get proper property (based on channel)
                for p in self.properties:
                    if p["channel"] == chan:
                        prop = p
                # If property is matched, send data
                if prop is not None:
                    print(str(self.node_addr) + "-" + str(prop["name"]) + "-" + str(val))
                    self.sendData(prop["name"], val, config)
                else:
                    print("error matching data channel to properties")
            else:
                print("error parsing data sweep")


########################
# Force Node
#
# This node contains one property:
#   - No Channel, Force exerted on sensor
#
# This node requires a get data method:
#   - getDataFromSweep(<sweep>)
#
# The section in config.json for a temperature node should look like this:
# {
#   "address": 56609,
#   "type": "force",
#   "thing_name": "thingName",
#   "thing_properties": [
#       {
#           "name": "force",
#           "channel": "none",
#           "type": "NUMBER"
#       }]
# }
########################
class ForceNode(NodeTemplate):
    def __init__(self, node_addr, node_type, thing_name, properties):
        NodeTemplate.__init__(self, node_addr, node_type, thing_name, properties)

    def getDataFromSweep(self, sweep, config):
        # A DataPoint for this sweep type usually has 1 value
        # Occasionally, a DataPoint will have 2 values, discard those sweeps
        val = []
        for dataPoint in sweep.data():
            val.append(dataPoint.as_float())

        # If there is only one value, sweep is good and send it
        if len(val) == 1:
            prop = None
            if len(self.properties) == 1:
                prop = self.properties[0]
            else:
                print("problem with force node properties")
                return
            print(str(self.node_addr) + "-" + prop["name"] + "-" + str(val[0]))
            self.sendData(prop["name"], val[0], config)
        else:
            print("error parsing dataSweep")


########################
# New Node
#
# Deterimine Node Properties:
#   - <Channel>, Description
#
# This node requires a get data method:
#   - getDataFromSweep(<sweep>)
########################
#class NewNode(NodeTemplate):
#    def __init__(self, node_addr, node_type, thing_name, properties):
#        NodeTemplate.__init__(self, node_addr, node_type, thing_name, properties)
#
#    def getDataFromSweep(self, sweep):
#       # Create method that properly reads the data from a sweep and sends
#       # it to the corresponding property on the thingworx server
#       return
