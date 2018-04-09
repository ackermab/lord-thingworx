import packages.mscl as mscl
import packages.lord as lord
import json

from tkinter import *

class StationConfig:
    def __init__(self, parent, config):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.config = config
        self.initUI()

    def initUI(self):
        self.parent.title("Add BaseStation")
        Label(self.parent, text="COM Port:").grid(row=0, column=0)
        Label(self.parent, text="Baud Rate:").grid(row=1, column=0)
        
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e1.insert(0, self.config["com_port"])
        self.e2.insert(0, self.config["baud_rate"])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        
        Button(self.parent, text='Add BaseStation', command=self.setBaseStation).grid(row=2, column=0, sticky=W)

    def setBaseStation(self):
        self.config["com_port"] = self.e1.get()
        self.config["baud_rate"] = self.e2.get()
        self.parent.destroy()

    def getUpdatedConfig(self):
        return config


class NodeConfig:
    def __init__(self, parent, node):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.node = node
        self.done = False
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
        self.e1.insert(0, self.node["node_addr"])
        self.e2.insert(0, self.node["node_type"])
        self.e3.insert(0, self.node["thing_name"])
        self.e4.insert(0, self.node["thing_properties"])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        Button(self.parent, text='Add and Add Another', command=self.addAnother).grid(row=4, column=0, sticky=W)
        Button(self.parent, text='Add and Finish Nodes', command=self.completeAdding).grid(row=4, column=1, sticky=W)
        Button(self.parent, text='Cancel', command=self.concelAdding).gri(row=4, column=2, sticky=W)

    def addAnother(self):
        self.setValues()
        self.parent.destroy()

    def completeAdding(self):
        self.setValues()
        self.done = True
        self.parent.destroy()

    def cancelAdding(self):
        self.node = None
        self.done = True
        self.parent.destroy()

    def setValues(self):
        self.node["node_addr"] = self.e1.get()
        self.node["node_type"] = self.e2.get()
        self.node["thing_name"] = self.e3.get()
        self.node["thing_properties"] = self.e4.get()

    def getNode(self):
        return self.node

    def getDone(self):
        return self.done

class ThingWorxConfig:
    def __init__(self, parent, config):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.config = config
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
        self.e4 = Entry(self.parent, show="*")
        self.e1.insert(0, self.config["thingworx_host"])
        self.e2.insert(0, self.config["app_key"])
        self.e3.insert(0, self.config["http_username"])
        self.e4.insert(0, "")
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        
        Button(self.parent, text='Configure Basestation', command=self.setConfig).grid(row=4, column=0, sticky=W)

    def setConfig(self):
        self.config["thingworx_host"] = self.e1.get()
        self.config["app_key"] = self.e2.get()
        self.config["http_basic_auth"] = createBasicAuth(self.e3.get(), self.e4.get()) # We shouldn't really save this
        self.config["http_username"] = self.e3.get()
        self.parent.destroy()

    def createBasicAuth(self, username, password):
        basic = b64encode(bytes(username + ":" + password, "utf-8")
        basic = "Basic " + basic
        print(basic)
        return basic

    def getUpdatedConfig(self):
        return self.config

def readConfig():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def updateConfig(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)

def main():
    print("Initializing connection to Lord Sensors and ThingWorx")
    node_obj = []

    config = readConfig()

    # Base Station Config Window
    win1 = Tk()
    app1 = StationConfig(win1, config)
    win1.mainloop()
    config = app1.getUpdatedConfig()

    print(config["nodes"])
    # Loop of Node Config Windows
    for node in config["nodes"]:
        win2 = Tk()
        app2 = NodeConfig(win2, node)
        win2.mainloop()
        if app2.getNode() is not None:
            node = app2.getNode()
        if app2.getDone():
            break

    config["nodes"] = nodes
    print(config["nodes"])

    # ThingWorx Server Config Window
    win3 = Tk()
    app3 = ThingWorxConfig(win3, config)
    win3.mainloop()
    config = app3.getUpdatedConfig()

    # Store config back to config file
    updateConfig(config)

    try:
        # Connect base station
        bs = lord.connectToBaseStation(config["com_port"], config["baud_rate"])
        if bs:
            # Create network
            network = mscl.SyncSamplingNetwork(bs)
            # Add each node
            if len(nodes) > 0:
                for node in nodes:
                    # Determine type of node
                    if node["type"] == "force":
                        n = lord.ForceNode(node["address"], node["type"], node["thing_name"], node["thing_properties"])
                    elif node["type"] == "temp":
                        n = lord.TempNode(node["address"], node["type"], node["thing_name"], node["thing_properties"])
                ##### Sample new node type #####
                #   elif node["type"] == "foo":
                #       n = lord.FooNode(node["address"], node["type"], node["thing_name"], node["thing_properties"])
                ##### Copy above section without comments and change foo to type of node
                    else:
                        continue # Node with type not recognized is skipped

                    # Check ThingWorx Server for node with the same name, add if it doesn't exist
                    tw_nodes = getNamesOfThings()
                    if node["thing_name"] in tw_nodes:
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
