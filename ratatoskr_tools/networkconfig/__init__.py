import os
import shutil
import xml.etree.ElementTree as ET
from . import configure
from . import xml_writers as writers


def create_config_ini(dst_path="./config.ini"):
    """
    Create the config.ini file for the given destination path.

    Parameters
    ----------
    dst_path : str, optional
        The destination path of the config file, by default "./config.ini"
    """
    src_path = os.path.dirname(__file__)
    src_path = os.path.join(src_path, "config.ini")
    shutil.copyfile(src_path, dst_path)


def create_configuration(config_file='config.ini', config_xml='config.xml', network_xml='network.xml'):
    """
    Create the config.xml and network.xml files for the simulator from the given config.ini file.

    Parameters
    ----------
    config_file : str, optional
        Input configuration file, by default 'config.ini'
    config_xml : str, optional
        Output configuration xml file for the simulator, by default 'config.xml'
    network_xml : str, optional
        Output network xml file for the simulator, by default 'network.xml'

    Returns
    -------
    ratatoskr_tools.networkconfig.configure.Configuration
        The read config.ini file information
    """
    config = configure.Configuration(config_file)

    writer = writers.ConfigWriter(config)
    writer.write_config(config_xml)

    writer = writers.NetworkWriter(config)
    writer.write_network(network_xml)

    return config


def edit_config_file(config, src_config_xml, dst_config_xml, inj_rate):
    """
    Edit the injection rate of the config.xml.
    Write the configuration file for the urand simulation.

    Parameters
    ----------
    config : ratatoskr_tools.networkconfig.configure.Configuration
        configuration object.
    src_config_xml : str
        the source of the configuration file.
    dst_config_xml : str
        the destination of the config file.
    inj_rate : float
        the injection rate.
    """
    try:
        configTree = ET.parse(src_config_xml)
    except Exception:
        raise

    configTree.find('noc/nocFile').text = 'config/' + \
        config.topologyFile + '.xml'
    configTree.find('general/simulationTime').set('value',
                                                  str(config.simulationTime))
    configTree.find('general/outputToFile').set('value', 'true')
    configTree.find('general/outputToFile').text = 'report'

    for elem in list(configTree.find('application/synthetic').iter()):
        if elem.get('name') == 'warmup':
            elem.find('start').set('min', str(config.warmupStart))
            elem.find('start').set('max', str(config.warmupStart))
            elem.find('duration').set('min',
                                      str(config.warmupStart + config.warmupDuration))
            elem.find('duration').set('max',
                                      str(config.warmupStart + config.warmupDuration))
            elem.find('injectionRate').set('value', str(inj_rate))
        if elem.get('name') == 'run':
            elem.find('start').set('min', str(config.runStart))
            elem.find('start').set('max', str(config.runStart))
            elem.find('duration').set('min', str(
                config.runStart + config.runDuration))
            elem.find('duration').set('max', str(
                config.runStart + config.runDuration))
            elem.find('injectionRate').set('value', str(inj_rate))
    configTree.write(dst_config_xml)
