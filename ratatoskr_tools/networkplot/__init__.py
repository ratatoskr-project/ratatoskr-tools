import json
import zmq
import os
from . import plot_network


def plot_static(network_xml, config_file, output_file=None, plt_show=False):
    """[summary]

    Parameters
    ----------
    network_xml : str
        Path of network.xml file
    config_file : str
        Path of config.ini file
    output_file : str, optional
        The generated network plot is outputted to the given path, by default None
    plt_show : bool, optional
        The generated network plot is showed, by default False

    Returns
    -------
    Figure
        The generated network plot.
    """

    plot_network.init_script(network_xml, config_file)
    plot_network.create_fig()
    plot_network.plot_nodes()
    plot_network.plot_connections()
    plot_network.annotate_points()
    plot_network.create_faces()
    plot_network.plot_faces()

    if output_file is not None:
        assert os.path.isfile(output_file)
        plot_network.plt.savefig(output_file)

    if plt_show:
        plot_network.plt.show()

    return plot_network.fig


def plot_dynamic(network_xml, config_file):

    plot_network.init_script(network_xml, config_file)
    plot_network.create_fig()
    plot_network.plot_connections()

    plot_network.colorize_nodes(range(len(plot_network.points)))

    time_stamp = plot_network.ax.text(2, 2, 2, 0, size=12, color='red')
    avg_router_load = [0] * len(plot_network.points)

    context = zmq.Context()

    print("Connecting to simulator server")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    for request in range(2000000):
        socket.send_string("Hello")
        message = socket.recv()
        print("there")

        data = json.loads(message)
        time = float(data["Time"]["time"])
        current_load = []

        for router_idx in range(len(plot_network.points)):
            current_router_val = float(
                data["Data"][router_idx]["averagebufferusage"])
            current_load.append(current_router_val)
            alpha = .01
            avg_router_load[router_idx] = alpha * current_router_val + \
                (1-alpha) * avg_router_load[router_idx]

        plot_network.routerHeat.remove()
        plot_network.colorize_nodes(avg_router_load)
        time_stamp.remove()

        time_stamp_val = "Time: " + str(time/1000) + " ns"
        time_stamp = plot_network.ax.text(
            0, 1, 1, time_stamp_val, size=12, color='red')

        plot_network.plt.pause(1/30)

    plot_network.plt.show()
