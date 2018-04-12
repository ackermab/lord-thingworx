# Lord Microstrain - ThingWorx Interface API Application
## Connecting IoT Sensors to a Data Analysis Platform Using Python

### Requirements
* Python 3.6 64-Bit
* LORD SensorConnect [Lord Website](http://www.microstrain.com/software)
  * This software is required to install due to the need for windows to have device drivers.  Installing the software will install the required drivers
* Microsoft Visual C++ 2017 [Download Link](https://aka.ms/vs/15/release/vc_redist.x64.exe)

### Setup & Configuration
* Provided in the repository is a file, config.json.sample
* Copy this file to config.json
  * `cp config.json.sample config.json`

#### Editing the Config File
The config file can be editted to allow for easy running of the application.  If the file is not updated before running, the application will prompt for the required information and save everything but the authentication password into the config.json file.  To add these manually, take note of these points:
* The config contains several data fields that need to be filled in for ThingWorx:
  * "thingworx\_host": ""       (The IP address of the ThingWorx Server)
  * "app\_key": ""              (The App Key obtained from ThingWorx Server)
  * "http\_username": ""        (The Username used to log into ThingWorx)
* Configuration for the Base Station should be changed. These values are:
  * "com\_port": "<COM#>"       (The COM port where the device is connected)
  * "baud\_rate": <number>      (The baud rate the base station communicates at)
* In addition, users can add node information to the "nodes" array. **Take caution to adhere to JSON formatting rules**
  * This segment is a JSON Array and has the following format: [{},{},{}..]
  * Each type of node will have a slightly different configuration, but each node shares these data fields:
    * "node\_addr": <number>,       (Address of the node, usually on the node itself)
    * "node\_type": "<string>",     (Type of the node, this is important in the code of this application)
    * "thing\_name": "<string>",    (Name of the Thing in ThingWorx)
    * "thing\_properties": <JSON Array> (Array of properties for the node)
  * The properties of a node are as follows:
    * "name": "<string>",       (Name of the property in ThingWorx)
    * "channel": "<string>",    (Some nodes have a channel for the data, if no channel put "none")
    * "type": "<string>"        (The type ThingWorx considers the data to be)
* The following are examples for a Temperate Sensor and a Force Transducer:
  * ```{
            "address": 56609,
            "type": "temp",
            "thing_name": "lordThing",
            "thing_properties": [
                {
                    "name": "temp",
                    "channel": "ch1",
                    "type": "NUMBER"
                }, {
                    "name": "internal_temp",
                    "channel": "ch7",
                    "type": "NUMBER"
                }]
    }```
  * ```{
            "address": 57861,
            "type": "force",
            "thing_name": "forceThing",
            "thing_properties": [
                {
                    "name": "force",
                    "channel": "none",
                    "type": "NUMBER"
                }]
            }]
    }```
### Running the Application


### The ThingWorx Side


### Viewing the Data


#### Licensing Notes
The MSCL Libraries provided in packages/mscl.py and packages/\_mscl.pyd are released under and MIT License. You can see this license in the file, LICENSE
