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
import sys
import csv
import pandas as pd
import numpy as np
###############################################################################


def create_layers_range(config):
    """
    Calculate the router id range for each layer of NoC.

    Parameters
    ----------
    config : [type]
        Configuration

    Returns
    -------
    [type]
        list of router id range
    """

    layers_range = []
    router_counter = 0
    for x, y in zip(config.x, config.y):
        layers_range.append(range(router_counter, router_counter+x*y))
        router_counter += x*y
    return layers_range


def find_layer_id(layers_range, router_id):
    """
    Find layer id of the router.

    Parameters
    ----------
    layers_range : [type]
        list of router id range
    router_id : int
        [description]

    Returns
    -------
    int
        layer id
    """
    for itr, layer_range in enumerate(layers_range):
        if router_id in layer_range:
            return itr


def init_data_structure(config):
    """
    Initialize the data structure named 'layers' which is a list (the length of the list
    is the number of NoC layer) of dictionaries that contains the flit transfer direction
    in the form of pandas data frame.

    Parameters
    ----------
    config : [type]
        Configuration

    Returns
    -------
    [type]
        The initilazed data structure
    """
    layer_temp = {'Up': pd.DataFrame(), 'Down': pd.DataFrame(),
                  'North': pd.DataFrame(), 'South': pd.DataFrame(),
                  'East': pd.DataFrame(), 'West': pd.DataFrame()}

    layers = [layer_temp.copy() for itr in range(config.z)]

    return layers


def read_dataframe(layers, path, layer_id, directory):
    """
    Read a data frame from csv file then accumulate the data.

    Parameters:
        - layers: a dictionary of dictionaries, and this is the data that
        needs to bee updated.
        - path: the path of the csv file to be read.
        - layer: the key of outmost dictionary layers.
        - directory: the key of innermost dictionary layers[layer]

    Return:
       - The updated data structure layers,
         or None if the csv file not exists.
    """
    temp = pd.read_csv(path, index_col=0)
    if not temp.empty:
        layers[layer_id][directory] = layers[layer_id][directory].add(
            temp, fill_value=0)
        return layers

    return None


def get_latencies(latencies_results_file):
    """
    Read the resulting latencies from the csv file.

    Parameters:
        - results_file: the path to the result file.

    Return:
        - A list of the filt, packet and network latencies.
    """
    latencies = []
    try:
        with open(latencies_results_file, newline='') as f:
            spamreader = csv.reader(f, delimiter=' ', quotechar='|')
            for row in spamreader:
                latencies.append(row[1])
    except Exception:
        # Add dummy values to latencies, -1.
        latencies.append(-1)
        latencies.append(-1)
        latencies.append(-1)

    return latencies


def combine_vc_hists(directory, config):
    """[summary]
    Combine the VC histograms from csv files.
    Parameters
    ----------
    directory : [type]
        the path of the directory that contains the files.
    config : [type]
        [description]

    Returns
    -------
    [type]
        A dataframe object of the combined csv files,
        or None if the directory doesn't exist.
    """

    if not os.path.exists(directory):
        return None

    data = [pd.DataFrame() for itr in range(config.z)]

    layers_range = create_layers_range(config)
    for fname in os.listdir(directory):
        router_id = int(fname.split('.')[0])
        layer_id = find_layer_id(layers_range, router_id)
        temp = pd.read_csv(os.path.join(directory, fname),
                           header=None, index_col=0).T
        data[layer_id] = data[layer_id].add(temp, fill_value=0)

    for df in data:
        df.columns.name = 'Direction'
        df.index.name = 'Number of VCs'

    return data


def combine_buff_hists(directory, config):
    """
        Combine the Buffer histograms from csv files.

        Parameters:
            - directory: the path of the directory that contains the files.

        Return:
            - A dataframe object of the combined csv files,
            or None if the directory doesn't exist.
    """
    if not os.path.exists(directory):
        return None

    data = init_data_structure(config)
    layers_range = create_layers_range(config)

    for filename in os.listdir(directory):
        router_id = int(filename.split('.')[0].split('_')[0])
        direction = filename.split('.')[0].split('_')[1]
        path = directory + '/' + filename

        if direction not in ['Up', 'Down', 'North', 'South', 'East', 'West']:
            continue

        layer_id = find_layer_id(layers_range, router_id)
        data = read_dataframe(data, path, layer_id, direction)

    # average the buffer usage over the inner routers (#4)
    for itr, layer in enumerate(data):
        for d in layer:
            data[itr][d] = np.ceil(data[itr][d] / 4)

    return data
