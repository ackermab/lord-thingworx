import packages.mscl as mscl
import packages.thingworx as thingworx

import ast

def getNode(node_obj, addr):
    for n in node_obj:
        if str(n.getNodeAddr()) == str(addr):
            return n
    return None


def parseData(sweeps, node_obj):
    for sweep in sweeps:
        addr = sweep.nodeAddress()
        node = getNode(node_obj, addr)
        if node is not None:
            node.getDataFromSweep(sweep)
        else:
            print("error finding associated node for data sweep")


def connectToBaseStation(com_port, baud_rate):
    conn = mscl.Connection.Serial(com_port, int(baud_rate))
    bs = mscl.BaseStation(conn)
    print("Connect base station: " + com_port + " " + baud_rate)
    return bs


def connectToNode(node_addr, bs):
    node = mscl.WirelessNode(int(node_addr), bs)
    print("Connect node: " + node_addr)
    return node


class TempNode:
    def __init__(self, node_addr, node_type, thingName, properties):
        self.node_addr = node_addr
        self.node_type = node_type
        self.node = None
        self.thingName = thingName
        self.properties = ast.literal_eval(properties)

    def connectNode(self, bs):
        self.node = mscl.WirelessNode(int(self.node_addr), bs)
        print("Connect node: " + self.node_addr)
        return self.node

    def getDataFromSweep(self, sweep):
        for dataPoint in sweep.data():
            chan = dataPoint.channelName()
            val = dataPoint.as_float()
            if val is not None:
                print(str(self.node_addr) + "-" + str(self.properties[chan]) + "-" + str(val))
                self.sendData(self.properties[chan], val)
            else:
                print("error parsing data sweep")

    def getNodeAddr(self):
        return self.node_addr

    def getNodeType(self):
        return self.node_type

    def sendData(self, property, data):
        thingworx.putDataToThing(self.thingName, property, data)

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

class ForceNode:
    def __init__(self, node_addr, node_type, thingName, thingPropertyName):
        self.node_addr = node_addr
        self.node_type = node_type
        self.node = None
        self.thingName = thingName
        self.thingPropertyName = thingPropertyName

    def connectNode(self, bs):
        self.node = mscl.WirelessNode(int(self.node_addr), bs)
        print("Connect node: " + self.node_addr)
        return self.node

    def getDataFromSweep(self, sweep):
        val = []
        for dataPoint in sweep.data():
            val.append(dataPoint.as_float())

        if len(val) == 1:
            print(str(self.node_addr) + "-" + self.thingPropertyName + "-" + str(val[0]))
            self.sendData(self.thingPropertyName, val[0])
        else:
            print("error parsing dataSweep")

    def getNodeAddr(self):
        return self.node_addr

    def getNodeType(self):
        return self.node_type

    def sendData(self, property, data):
        thingworx.putDataToThing(self.thingName, property, data)

    def cleanUp(self):
        print("Cleaning up node: " + self.node_addr)
        status = self.node.setToIdle()
        while not status.complete(300):
            print(".")
        result = status.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Set " + self.node_addr + " to idle")
        elif result == mscl.SetToIdleStatus.setToIdleResult_canceled:
            print("Setting " + self.node_addr + " to idle cancelled")
        else:
            print("Setting " + self.node_addr + " to idle failed")
