import pandas as pd

from .combine_hists import *


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
        vc_usage_run = combine_vc_hists(
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


def retrieve_buff_usages(simdirs):
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

    buff_usage_inj = init_data_structure()

    for simdir in simdirs:
        buff_usage_run = combine_buff_hists(simdir + "/BuffUsage")
        if buff_usage_run is not None:
            for l in buff_usage_inj:
                for d in buff_usage_inj[l]:
                    buff_usage_inj[l][d] = buff_usage_inj[l][d].add(
                        buff_usage_run[l][d], fill_value=0)

    # Average the buffer usage over restarts.
    buff_usage_temp = init_data_structure()  # a dict of dicts
    for l in buff_usage_inj:
        for d in buff_usage_inj[l]:
            buff_usage_temp[l][d] = np.ceil(
                buff_usage_inj[l][d] / len(simdirs))

    return buff_usage_temp


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
        lat = get_latencies(simdir + "/report_Performance.csv")
        latency_flits[idx] = lat[0]
        latency_packets[idx] = lat[1]
        latency_networks[idx] = lat[2]

    return latency_flits, latency_packets, latency_networks
