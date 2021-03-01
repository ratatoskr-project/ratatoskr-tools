#!/bin/python

# Copyright 2018 Jan Moritz Joseph

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################
import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
###############################################################################


def plot_latencies(inj_rates, latencies_flit, latencies_packet, latencies_network, output_file=None, plt_show=False):
    """
    Read the raw results from a dictionary of objects, then plot the latencies.

    Parameters:
        - results: a dictionary of raw data from the pickle file.

    Return:
        - None.
    """

    mean_latencies_flit = np.mean(latencies_flit, axis=1)
    mean_latencies_packet = np.mean(latencies_packet, axis=1)
    mean_latencies_network = np.mean(latencies_network, axis=1)

    std_latencies_packet = np.std(latencies_packet, axis=1)
    std_latencies_network = np.std(latencies_network, axis=1)

    fig = plt.figure()

    plt.ylabel('Latencies in ns', fontsize=11)
    plt.xlabel('Injection Rate', fontsize=11)
    plt.xlim([0, (inj_rates[0] + inj_rates[-1])])
    plt.ylim([0, (mean_latencies_packet[-1] + 4 * std_latencies_packet[-1])])

    linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
                 'elinewidth': 1, 'capsize': 10}

    plt.errorbar(inj_rates, mean_latencies_flit,
                 color='r', **linestyle, marker='*')
    plt.errorbar(inj_rates, mean_latencies_packet, yerr=std_latencies_packet,
                 color='g', **linestyle, marker='^')
    plt.errorbar(inj_rates, mean_latencies_network, yerr=std_latencies_network,
                 color='b', **linestyle, marker='s')

    plt.legend(['Flit', 'Packet', 'Network'])
    fig.suptitle('Latencies', fontsize=16)

    if plt_show is True:
        plt.show()

    if output_file is not None:
        assert type(output_file) is str
        fig.savefig(output_file)

    return fig
###############################################################################


def plot_vc_usage_stats(vc_usages, inj_rates, output_dir=None, plt_show=False):
    """
    Plot the VC usage statistics.

    Parameteres:
        - vc_usages: the data frames of an injection rate.
        - inj_rates: the number of injection rates.

    Return:
        - None.
    """
    figs = []
    for inj_df, inj_rate in zip(vc_usages, inj_rates):
        for layer_id, df in enumerate(inj_df):
            fig = plt.figure()  # plot a figure for each inj_rate and layer
            plt.title('Layer ' + str(layer_id) +
                      ', Injection Rate = ' + str(inj_rate))
            plt.ylabel('Count', fontsize=11)
            plt.xlabel('VC Usage', fontsize=11)
            for col in df.columns.levels[0].values:
                plt.errorbar(df.index.values, df[col, 'mean'].values,
                             yerr=df[col, 'std'].values)
            plt.legend(df.columns.levels[0].values)

            if plt_show is True:
                plt.show()

            if output_dir is not None:
                assert os.path.isdir(output_dir)
                output_path = os.path.join(output_dir, 'VC_' + str(layer_id) +
                                           '_' + str(inj_rate) + '.pdf')
                fig.savefig(output_path)

            figs.append(fig)

    return figs
###############################################################################


def plot_buff_usage_stats(buff_usages, inj_rates, output_dir=None, plt_show=False):
    """
    Plot the buffer usage statistics.

    Parameters:
        - buff_usages: the data dictionaries of an injection rate.
        - inj_rates: the number of injection rates.

    Return:
        - None.
    """
    figs = []
    for inj_dict, inj_rate in zip(buff_usages, inj_rates):
        for layer_id, layer_name in enumerate(inj_dict):
            layer_dict = inj_dict[layer_name]
            fig = plt.figure()
            for it, d in enumerate(layer_dict):
                df = layer_dict[d]
                if not df.empty:
                    ax = fig.add_subplot(3, 2, it+1, projection='3d')
                    lx = df.shape[0]
                    ly = df.shape[1]
                    xpos = np.arange(0, lx, 1)
                    ypos = np.arange(0, ly, 1)
                    xpos, ypos = np.meshgrid(xpos, ypos, indexing='ij')

                    xpos = xpos.flatten()
                    ypos = ypos.flatten()
                    zpos = np.zeros(lx*ly)

                    dx = 1 * np.ones_like(zpos)
                    dy = dx.copy()
                    dz = df.values.flatten()

                    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b')

                    ax.set_yticks(ypos)
                    ax.set_xlabel('Buffer Size')
                    ax.set_ylabel('VC Index')
                    ax.set_zlabel('Count')
                    ax.set_title('Direction:'+str(d))

            fig.suptitle('Layer: '+str(layer_name)+', Injection Rate = '
                         + str(inj_rate), fontsize=16)

            if plt_show is True:
                plt.show()

            if output_dir is not None:
                assert os.path.isdir(output_dir)
                output_path = os.path.join(output_dir, 'Buff_' + str(layer_id) +
                                           '_' + str(inj_rate) + '.pdf')
                fig.savefig(output_path)

            figs.append(fig)

    return figs
###############################################################################
