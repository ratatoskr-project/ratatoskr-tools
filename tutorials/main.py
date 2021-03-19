#!python3
import os
import numpy as np
import pickle as pkl
from matplotlib.backends.backend_pdf import PdfPages
import ratatoskr_tools.networkconfig as rtcfg
import ratatoskr_tools.networkplot as rtnplt
import ratatoskr_tools.simulation as rtsim
import ratatoskr_tools.datahandle as rtdat
import ratatoskr_tools.dataplot as rtdplt

WORK_DIR = "./example/"

CONFIG_INI = os.path.join(WORK_DIR, "config.ini")
CONFIG_XML = os.path.join(WORK_DIR, "config.xml")
NETWORK_XML = os.path.join(WORK_DIR, "network.xml")

CONFIG_TMP = os.path.join(WORK_DIR, "config_tmp.xml")

SIMULATOR = "./sim"

if __name__ == "__main__":

    # rtcfg.create_config_ini(dst_path=CONFIG_INI)

    config = rtcfg.create_configuration(CONFIG_INI, CONFIG_XML, NETWORK_XML)

    # fig_network = rtnplt.plot_static(NETWORK_XML, CONFIG_INI)

    # rtnplt.plot_dynamic(NETWORK_XML, CONFIG_INI)

    # initialization of vars
    inj_rates = np.arange(
        config.runRateMin, config.runRateMax, config.runRateStep).round(4)
    lats_flit = -np.ones((len(inj_rates), config.restarts))
    lats_packet = -np.ones((len(inj_rates), config.restarts))
    lats_network = -np.ones((len(inj_rates), config.restarts))
    vc_usages = []
    buff_usages = []

    # rtsim.remove_all_simdirs(WORK_DIR, config.restarts)
    for injItr, injRate in enumerate(inj_rates):
        basedir = os.path.join(WORK_DIR, "inj{}".format(injItr))

        os.system("mkdir {}".format(basedir))

        print("Running", injItr, injRate)
        simdirs = rtsim.make_all_simdirs(basedir, config.restarts)

        config_tmp = os.path.join(basedir, "config.xml")
        rtcfg.edit_config_file(config, CONFIG_XML, config_tmp, injRate)

        rtsim.run_parallel_multiple_sims(
            simdirs, SIMULATOR, config_tmp, NETWORK_XML)

        vc_usages.append(rtdat.retrieve_vc_usages(simdirs, config))
        buff_usages.append(rtdat.retrieve_buff_usages(simdirs, config))
        lats_flit[injItr], lats_packet[injItr], lats_network[injItr] = rtdat.retrieve_diff_latencies(
            simdirs)

        # rtsim.remove_all_simdirs(WORK_DIR, config.restarts)

    print(lats_flit)
    print(lats_packet)
    print(lats_network)
    print(vc_usages)
    print(buff_usages)
    results = {
        "lats_flit": lats_flit,
        "lats_packet": lats_packet,
        "lats_network": lats_network,
        "vc_usages": vc_usages,
        "buff_usages": buff_usages
    }

    with open("results.pkl", "wb") as handle:
        pkl.dump(results, handle)

    fig_latencies = rtdplt.plot_latencies(
        inj_rates, lats_flit, lats_packet, lats_network)
    figs_vc = rtdplt.plot_vc_usage_stats(vc_usages, inj_rates)
    figs_buff = rtdplt.plot_buff_usage_stats(buff_usages, inj_rates)

    figs = [
        # fig_network,
        fig_latencies
    ]
    figs.extend(figs_vc)
    figs.extend(figs_buff)

    pdf = PdfPages(os.path.join(WORK_DIR, "result.pdf"))
    for fig in figs:
        pdf.savefig(fig)
    pdf.close()
