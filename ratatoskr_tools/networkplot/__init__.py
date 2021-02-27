import json
import zmq
import os
from . import plot_network


def plot_static(network_xml, config_file, output_file=None, plt_show=False):
    """
    Plot the static network.

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


def plot_dynamic(network_xml, config_file, host="localhost", port=5555, max_request=2000000):
    """
    Plot the dynamic network which connect to the GUI server of the ratatoskr simulator.

    Parameters
    ----------
    network_xml : str
        Path of network.xml file
    config_file : str
        Path of config.ini file
    host : str, optional
        tcp server host ip, by default "localhost"
    port : int, optional
        tcp port number, by default 5555
    max_request : int, optional
        maximum request count to the server, by default 2000000
    """

    plot_network.init_script(network_xml, config_file)
    plot_network.create_fig()
    plot_network.plot_connections()

    plot_network.colorize_nodes(range(len(plot_network.points)))

    time_stamp = plot_network.ax.text(2, 2, 2, 0, size=12, color='red')
    avg_router_load = [0] * len(plot_network.points)

    context = zmq.Context()

    print("Connecting to simulator server")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{}:{}".format(host, port))

    for request in range(max_request):
        socket.send_string("Cient request {}".format(request))
        message = socket.recv()

        data = json.loads(message)
        time = float(data["Time"]["time"])

        for router_idx in range(len(plot_network.points)):
            current_router_val = float(
                data["Data"][router_idx]["averagebufferusage"])
            alpha = .01
            avg_router_load[router_idx] = alpha * current_router_val + \
                (1-alpha) * avg_router_load[router_idx]

        plot_network.router_heat.remove()
        plot_network.colorize_nodes(avg_router_load)
        time_stamp.remove()

        time_stamp_val = "Time: {} ns".format(time/1000)
        time_stamp = plot_network.ax.text(
            0, 1, 1, time_stamp_val, size=12, color='red')

        plot_network.plt.pause(1/30)

    plot_network.plt.show()
