
from . import plot_network


def plot_static(network_xml="network.xml", config_file="config.ini", output_img="", plt_show=False):
    """[summary]

    Args:
        network_xml (str, optional): [description]. Defaults to "network.xml".
        config_file (str, optional): [description]. Defaults to "config.ini".
        output_img (str, optional): [description]. Defaults to "".
        plt_show (bool, optional): [description]. Defaults to False.
    """
    plot_network.init_script(network_xml, config_file)
    plot_network.create_fig()
    plot_network.plot_nodes()
    plot_network.plot_connections()
    plot_network.annotate_points()
    plot_network.create_faces()
    plot_network.plot_faces()

    if output_img != "":
        plot_network.plt.savefig(output_img)

    if plt_show:
        plot_network.plt.show()

    plot_network.plt.close()
