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
