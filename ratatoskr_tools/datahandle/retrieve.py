import os

import numpy as np
import pandas as pd

from . import combine_hists as ch


def retrieve_vc_usages(simdirs, config):
    """
    Retrieve all the vc usages simulation result from the dummy simulation directories.

    Parameters
    ----------
    simdirs : list(str)
        The list of dummy simulation directories.

    Returns
    -------
    list(pd.DataFrame)
        The retrieved vc usages.
    """

    vc_usage_inj = [pd.DataFrame() for itr in range(config.z)]

    for simdir in simdirs:
        vc_usage_run = ch.combine_vc_hists(
            os.path.join(simdir, "VCUsage"), config)

        if vc_usage_run is not None:
            for idx, layer_df in enumerate(vc_usage_run):
                vc_usage_inj[idx] = pd.concat([vc_usage_inj[idx], layer_df])

    # Calculate the average and std for VC usage.
    vc_usage_temp = []
    for df in vc_usage_inj:
        if not df.empty:
            vc_usage_temp.append(df.groupby(df.index).agg(['mean', 'std']))

    return vc_usage_temp


def retrieve_buff_usages(simdirs, config):
    """
    Retrieve all the buff usages simulation result from the dummy simulation directories.

    Parameters
    ----------
    simdirs : list(str)
        The list of dummy simulation directories.

    Returns
    -------
    dict
        The retrieved buff usages.
    """

    buff_usage_inj = ch.init_data_structure(config)

    for simdir in simdirs:
        buff_usage_run = ch.combine_buff_hists(
            os.path.join(simdir, "BuffUsage"), config)

        if buff_usage_run is None:
            continue

        for itr, buff in enumerate(buff_usage_inj):
            for d in buff:
                buff_usage_inj[itr][d] = buff_usage_inj[itr][d].add(
                    buff_usage_run[itr][d], fill_value=0)

    # Average the buffer usage over restarts.
    for itr, buff in enumerate(buff_usage_inj):
        for d in buff:
            buff_usage_inj[itr][d] = np.ceil(
                buff_usage_inj[itr][d] / len(simdirs))

    return buff_usage_inj


def retrieve_diff_latencies(simdirs):
    """
    Retrieve all kinds of latencies (flit, packet, network) simulation result
    from the dummy simulation directories.

    Parameters
    ----------
    simdirs : list(str)
        The list of dummy simulation directories.

    Returns
    -------
    tuple
        The retrieved latencies in the order of flit, packet, network.
    """

    latency_flits = -np.ones(len(simdirs))
    latency_packets = -np.ones(len(simdirs))
    latency_networks = -np.ones(len(simdirs))
    for idx, simdir in enumerate(simdirs):
        lat = ch.get_latencies(simdir + "/report_Performance.csv")
        latency_flits[idx] = lat[0]
        latency_packets[idx] = lat[1]
        latency_networks[idx] = lat[2]

    return latency_flits, latency_packets, latency_networks
