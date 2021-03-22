# Tutorial 4 Running Netrace PARSEC mode

In this tutorial, you will learn the step to run the simulation in PARSEC mode.

## Prerequisite
Before this tutorial, it is required to compile and retrieve the execution simulator program "./sim" from the ratatoskr/simulator repository. Here, we need to add "-DDEFINE_ENABLE_NETRACE" while executing the cmake.
Let's compile the simulator:
```console
$ cd ../ratatoskr/simulator
$ cmake -DDEFINE_ENABLE_NETRACE=ON
$ make
$ cd ../../tutorials
```

Here, we set the simulator path as shown:



```python
SIM_PATH = ../ratatoskr/simulator/sim
```

## Step 1 Download the netrace file.
We will download and use the netrace simulation file (blackscholes_64c_simsmall) for this tutorial.


```python
url = "https://www.cs.utexas.edu/~netrace/download/blackscholes_64c_simsmall.tra.bz2"
call(["wget", url])

```

# Step 2 Create and edit configuration
Due to the netrace simulation requires NoC with at least 64 cores, so we need to edit the config.ini file. The NoC layout of 8x4x2 is created. The partial edited config.ini file is shown:
```ini
[Hardware]
topology = mesh
x = [8,8]
y = [4,4]
z = 2
routing = XYZ
clockDelay = [1,1]
```


```python
import ratatoskr_tools.networkconfig as rtcfg
import configparser

rtcfg.create_config_ini("config.ini")
config = configparser.ConfigParser()
config.read("config.ini")
config["Hardware"]["x"] = "[8,8]"
config["Hardware"]["y"] = "[4,4]"
config["Hardware"]["z"] = "2"
config["Hardware"]["clockDelay"] = "[1,1]"
with open("config.ini", "w") as handle:
    config.write(handle)
cfg = rtcfg.create_configuration("config.ini", "config.xml", "network.xml")
```

## Step 3 Run the simulation
The function run_single_sim can accept more kwargs which are acceptable to the simulator (SIM_PATH). Here, we set the simulation time to 10000ns and start from netrace region 0.
The loggins are written to the log file (stdout).


```python
import ratatoskr_tools.simulation as rtsim

rtsim.run_single_sim(SIM_PATH, "config.xml", "network.xml", output_dir=".", stdout="log",
    simTime=10000,
    netraceTraceFile="blackscholes_64c_simsmall.tra.bz2",
    netraceRegion=0,
    netraceVerbosity="all"
    )

```