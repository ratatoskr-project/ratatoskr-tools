# Tutorial 2: ratatoskr GUI client

In this tutorial, you will know how to use the ratatoskr GUI client, which let you to see the router heat (traffic business) of the NoC.

## Prerequisite

Before this tutorial, it is required to compile and retrieve the execution simulator program "./sim" from the ratatoskr/simulator repository. Here, we need to add "-DDEFINE_ENABLE_GUI" while executing the cmake.
Let's compile the simulator:
```console
$ cd ../ratatoskr/simulator
$ cmake -DDEFINE_ENABLE_GUI
$ make
$ cd ../tutorials
```

## Step 1 Network Configuration
Create the config.ini file and generate the config.xml and network.xml files.


```python
import ratatoskr_tools.networkconfig as rtcfg

rtcfg.create_config_ini("./example/config.ini")
config = rtcfg.create_configuration("./example/config.ini", "./example/config.xml", "./example/network.xml")
```

## Step 2 Dynamic Network Plotting

Use the provided API to run the ratatoskr GUI client.


```python
import ratatoskr_tools.networkplot as rtnplt

rtnplt.plot_dynamic("./example/network.xml")
```

## Step 3 Run the simulation.

Open another terminal to run the simulation, where this simulator is compiled with the enable gui options (-D ENABLE_GUI).

```console
$ ../ratatoskr/simulator/sim --configPath=./example/config.xml --networkPath=./example/network.xml --outputPath=./example
```

The ratatoskr GUI client windows will be opened.


```python

```
