from .combine_hists import *
import pandas as pd
import csv


def retrieve_vc_usages(simdirs):

    VCUsage_inj = [pd.DataFrame() for i in range(3)]

    for simdir in simdirs:
        VCUsage_run = combine_VC_hists(simdir + "/VCUsage")

        if VCUsage_run is not None:
            for ix, layer_df in enumerate(VCUsage_run):
                VCUsage_inj[ix] = pd.concat([VCUsage_inj[ix], layer_df])

    # Calculate the average and std for VC usage.
    VCUsage_temp = []
    for df in VCUsage_inj:
        if not df.empty:
            VCUsage_temp.append(df.groupby(df.index).agg(['mean', 'std']))

    return VCUsage_temp


def retrieve_buff_usages(simdirs):

    BuffUsage_inj = init_data_structure()

    for simdir in simdirs:
        BuffUsage_run = combine_Buff_hists(simdir + "/BuffUsage")
        if BuffUsage_run is not None:
            for l in BuffUsage_inj:
                for d in BuffUsage_inj[l]:
                    BuffUsage_inj[l][d] = BuffUsage_inj[l][d].add(BuffUsage_run[l][d], fill_value=0)

    # Average the buffer usage over restarts.
    BuffUsage_temp = init_data_structure()  # a dict of dicts
    for l in BuffUsage_inj:
        for d in BuffUsage_inj[l]:
            BuffUsage_temp[l][d] = np.ceil(BuffUsage_inj[l][d] / len(simdirs))

    return BuffUsage_temp



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

    return(latencies)


def retrieve_diff_latencies(simdirs):

    latencyFlits = -np.ones(len(simdirs))
    latencyPackets = -np.ones(len(simdirs))
    latencyNetworks = -np.ones(len(simdirs))
    for idx, simdir in enumerate(simdirs):
        lat = get_latencies(simdir + "/report_Performance.csv")
        latencyFlits[idx] = lat[0]
        latencyPackets[idx] = lat[1]
        latencyNetworks[idx] = lat[2]

    return latencyFlits, latencyPackets, latencyNetworks

