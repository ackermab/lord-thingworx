import packages.mscl as mscl
import packages.lord as lord
import config

from tkinter import *

class StationConfig:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.com_port = None
        self.baud_rate = None
        self.initUI()

    def initUI(self):
        self.parent.title("Add BaseStation")
        Label(self.parent, text="COM Port:").grid(row=0, column=0)
        Label(self.parent, text="Baud Rate:").grid(row=1, column=0)
        
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e1.insert(0, config.basestation["com_port"])
        self.e2.insert(0, config.basestation["baud_rate"])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        
        Button(self.parent, text='Add BaseStation', command=self.setBaseStation).grid(row=2, column=0, sticky=W)

    def setBaseStation(self):
        self.com_port = self.e1.get()
        self.baud_rate = self.e2.get()
        self.parent.destroy()

    def getComPort(self):
        return self.com_port

    def getBaudRate(self):
        return self.baud_rate

class NodeConfig:
    def __init__(self, parent, index):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.done = False
        self.index = index
        if index < len(config.basestation["nodes"]):
            self.node_addr = config.basestation["nodes"][index]["address"]
            self.node_type = config.basestation["nodes"][index]["type"]
            self.thing_name = config.basestation["nodes"][index]["thingName"]
            self.thing_properties = config.basestation["nodes"][index]["thingProperties"]
        else:
            self.node_addr = ""
            self.node_type = ""
            self.thing_name = ""
            self.thing_properties = ""
        self.initUI()

    def initUI(self):
        self.parent.title("Add Node")
        Label(self.parent, text="Node Address:").grid(row=0, column=0)
        Label(self.parent, text="Node Types:").grid(row=1, column=0)
        Label(self.parent, text="Thing Name:").grid(row=2, column=0)
        Label(self.parent, text="Thing Properties:").grid(row=3, column=0)

        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e3 = Entry(self.parent)
        self.e4 = Entry(self.parent)
        self.e1.insert(0, self.node_addr)
        self.e2.insert(0, self.node_type)
        self.e3.insert(0, self.thing_name)
        self.e4.insert(0, self.thing_properties)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        Button(self.parent, text='Add Another Node', command=self.addAnother).grid(row=4, column=0, sticky=W)
        Button(self.parent, text='Done Adding Nodes', command=self.completeAdding).grid(row=4, column=1, sticky=W)

    def addAnother(self):
        self.setValues()
        self.parent.destroy()

    def completeAdding(self):
        self.setValues()
        self.done = True
        self.parent.destroy()

    def setValues(self):
        self.node_addr = self.e1.get()
        self.node_type = self.e2.get()
        self.thing_name = self.e3.get()
        self.thing_properties = self.e4.get()

    def getNode(self):
        node = {}
        node["address"] = self.node_addr
        node["type"] = self.node_type
        node["thingName"] = self.thing_name
        node["thingProperties"] = self.thing_properties
        return node

    def getDone(self):
        return self.done

class ThingWorxConfig:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.serverIp = None
        self.appKey = None
        self.username = None
        self.password = None
        self.initUI()

    def initUI(self):
        self.parent.title("ThingWorx Host Configuration")
        Label(self.parent, text="Server IP:").grid(row=0, column=0)
        Label(self.parent, text="APP_Key:").grid(row=1, column=0)
        Label(self.parent, text="Username:").grid(row=2, column=0)
        Label(self.parent, text="Password:").grid(row=3, column=0)
        
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e3 = Entry(self.parent)
        self.e4 = Entry(self.parent)
        self.e1.insert(0, config.THINGWORX_HOST)
        self.e2.insert(0, config.APP_KEY)
        self.e3.insert(0, config.HTTP_USERNAME)
        self.e4.insert(0, config.HTTP_PASSWORD)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        
        Button(self.parent, text='Configure Basestation', command=self.setConfig).grid(row=4, column=0, sticky=W)

    def setConfig(self):
        self.serverIp = self.e1.get()
        self.appKey = self.e1.get()
        self.username = self.e1.get()
        self.password = self.e1.get()
        self.closeConfig()

    def closeConfig(self):
        self.parent.destroy()

    def getConfig(self):
        config = {
            "server_ip": self.serverIp,
            "app_key": self.appKey,
            "username": self.username,
            "password": self.password
            }
        return config

def readConfig():
    return

def updateConfig(com_port, baud_rate, nodes, tw_config):
    print("Storing new config", com_port, baud_rate, nodes, tw_config)
    return

def main():
    print("Initializing connection to Lord Sensors and ThingWorx")
    node_obj = []

    config = readConfig()

    # Base Station Config Window
    win1 = Tk()
    app1 = StationConfig(win1)
    win1.mainloop()
    com_port = app1.getComPort()
    baud_rate = app1.getBaudRate()

    # Loop of Node Config Windows
    nodes = []
    index = 0
    while True:
        win2 = Tk()
        app2 = NodeConfig(win2, index)
        win2.mainloop()
        if app2.getDone():
            break
        else:
            nodes.append(app2.getNode())
            index = index + 1

    # ThingWorx Server Config Window
    win3 = Tk()
    app3 = ThingWorxConfig(win3)
    win3.mainloop()
    tw_config = app3.getConfig()

    # Store config back to config file
    updateConfig(com_port, baud_rate, nodes, tw_config)

    try:
        # Connect base station
        bs = lord.connectToBaseStation(com_port, baud_rate)
        if bs:
            # Create network
            network = mscl.SyncSamplingNetwork(bs)
            # Add each node
            if len(nodes) > 0:
                for node in nodes:
                    # Determine type of node
                    if node["type"] == "force":
                        n = lord.ForceNode(node["address"], node["type"], node["thingName"], node["thingProperties"])
                    elif node["type"] == "temp":
                        n = lord.TempNode(node["address"], node["type"], node["thingName"], node["thingProperties"])
                ##### Sample new node type #####
                #   elif node["type"] == "foo":
                #       n = lord.FooNode(node["address"], node["type"], node["thingName"], node["thingProperties"])
                ##### Copy above section without comments and change foo to type of node
                    else:
                        continue # Node with type not recognized is skipped

                    # Check ThingWorx Server for node with the same name, add if it doesn't exist
                    tw_nodes = getNamesOfThings()
                    if node["thingName"] in tw_nodes:
                        print("Thing already exists on ThingWorx Server, skipping create")
                    else:
                        node.createThing()

                    node_obj.append(n)
                    network.addNode(n.connectNode(bs))

            network.applyConfiguration()
            network.startSampling()

            while True:
                TIMEOUT = 1000 # 500ms
                lord.parseData(bs.getData(TIMEOUT), node_obj)

    except KeyboardInterrupt:
        for node in node_obj:
            node.cleanUp()

if __name__ == "__main__":
    main()
