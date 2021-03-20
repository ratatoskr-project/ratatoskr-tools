import matplotlib.pyplot as plt


def plot_bandwidth(input_bandwidth, output_bandwidth, output_file=None, plt_show=False):
    """
    Plot the bandwidth of one simulation.

    Parameters
    ----------
    input_bandwidth : tuple
        Contains 2 elements, which are the time (x-axis) and bandwidth (y-axis) data.
    output_bandwidth : tuple
        Contains 2 elements, which are the time (x-axis) and bandwidth (y-axis) data.
    output_file : str, optional
        write the image to the output path (plot.png), by default None no output file
    plt_show : bool, optional
        Set to True to show the plotted graph, by default False

    Returns
    -------
    matplotlib.pyplot.figure()
        Plotted figure.
    """

    fig, ax = plt.subplots()
    ax.plot(input_bandwidth[0], input_bandwidth[1], alpha=0.7)
    ax.plot(output_bandwidth[0], output_bandwidth[1], alpha=0.7)

    ax.legend(["input bandwidth", "output bandwidth"])

    ax.set(xlabel='time (ns)', ylabel='bandwidth (Gbit/s)',
           title='Bandwidth')
    ax.grid()

    if output_file is not None:
        assert type(output_file) is str
        fig.savefig(output_file)

    if plt_show:
        plt.show()

    return fig
