import os
import shutil
import xml.etree.ElementTree as ET
from . import configure
from . import xml_writers as writers


def create_config_ini(dst_path="./config.ini"):
    src_path = os.path.dirname(__file__)
    src_path = os.path.join(src_path, "config.ini")
    shutil.copyfile(src_path, dst_path)


def create_configuration(config_file='config.ini', config_xml='config.xml', network_xml='network.xml'):
    config = configure.Configuration(config_file)

    writer = writers.ConfigWriter(config)
    writer.write_config(config_xml)

    writer = writers.NetworkWriter(config)
    writer.write_network(network_xml)

    return config


def edit_config_file(config, configFileSrc, configFileDst, injectionRate):
    """
    Edit the injection rate of the config.xml.
    Write the configuration file for the urand simulation.

    Parameters:
        - config: configuration object.
        - configFileSrc: the source of the configuration file.
        - configFileDst: the destination of the config file.
        - injectionRate: the injection rate.

    Return:
        - None.
    """
    try:
        configTree = ET.parse(configFileSrc)
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
            elem.find('injectionRate').set('value', str(injectionRate))
        if elem.get('name') == 'run':
            elem.find('start').set('min', str(config.runStart))
            elem.find('start').set('max', str(config.runStart))
            elem.find('duration').set('min', str(
                config.runStart + config.runDuration))
            elem.find('duration').set('max', str(
                config.runStart + config.runDuration))
            elem.find('injectionRate').set('value', str(injectionRate))
    configTree.write(configFileDst)
