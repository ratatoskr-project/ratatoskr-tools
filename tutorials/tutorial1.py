"""
Tutorial 1 python file
"""

import os

import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

import ratatoskr_tools.datahandle as rtdat
import ratatoskr_tools.dataplot as rtdplt
import ratatoskr_tools.networkconfig as rtcfg
import ratatoskr_tools.simulation as rtsim

SIM_PATH = "../ratatoskr/simulator/sim"

rtcfg.create_config_ini("./example/config.ini")
config = rtcfg.create_configuration("./example/config.ini", "./example/config.xml", "./example/network.xml")

# initialization of variables
vc_usages = []
buff_usages = []
inj_rates = np.arange(config.runRateMin, config.runRateMax, config.runRateStep).round(4)
lats_flit = -np.ones((len(inj_rates), config.restarts))
lats_packet = -np.ones((len(inj_rates), config.restarts))
lats_network = -np.ones((len(inj_rates), config.restarts))

rtsim.remove_all_simdirs("./example/", config.restarts)

for idx, inj_rate in enumerate(inj_rates):

    simdirs = rtsim.make_all_simdirs("./example/", config.restarts)

    rtcfg.edit_config_file(config, "./example/config.xml", "./example/config_tmp.xml", inj_rate)

    rtsim.run_parallel_multiple_sims(simdirs, SIM_PATH, "./example/config.xml", "./example/network.xml")

    vc_usages.append(rtdat.retrieve_vc_usages(simdirs, config))
    buff_usages.append(rtdat.retrieve_buff_usages(simdirs, config))
    lats_flit[idx], lats_packet[idx], lats_network[idx] = rtdat.retrieve_diff_latencies(simdirs)

    rtsim.remove_all_simdirs("./example/", config.restarts)

fig_latencies = rtdplt.plot_latencies(inj_rates, lats_flit, lats_packet, lats_network, plt_show=False)
figs_vc = rtdplt.plot_vc_usage_stats(vc_usages, inj_rates)
figs_buff = rtdplt.plot_buff_usage_stats(buff_usages, inj_rates)
figs = [fig_latencies]
figs.extend(figs_vc)
figs.extend(figs_buff)

pdf = PdfPages(os.path.join("./example/", "result.pdf"))
for fig in figs:
    pdf.savefig(fig)
pdf.close()
