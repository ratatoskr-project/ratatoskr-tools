import os
import subprocess
from joblib import Parallel, delayed


def make_all_simdirs(basedir, restarts):

    simdirs = ["/".join([basedir, "sim{}".format(restart)])
               for restart in range(restarts)]
    cmds = [" ".join(["mkdir", simdir]) for simdir in simdirs]

    for cmd in cmds:
        os.system(cmd)

    return simdirs


def remove_all_simdirs(basedir, restarts):

    simdirs = ["/".join([basedir, "sim{}".format(restart)])
               for restart in range(restarts)]
    cmds = [" ".join(["rm -rf", simdir]) for simdir in simdirs]

    for cmd in cmds:
        os.system(cmd)


def run_single_sim(simulator="./simulator/sim", config_path="./config/config.xml", network_path="./config/network.xml", output_dir="."):

    outfile = open(output_dir + "/log", "w")

    config_path = "--configPath=" + config_path
    network_path = "--networkPath=" + network_path
    output_dir = "--outputDir=" + output_dir

    args = (simulator, config_path, network_path, output_dir)
    try:
        subprocess.run(args, stdout=outfile, check=True)
    except subprocess.CalledProcessError:
        print("ERROR:", args)


def run_parallel_multiple_sims(num_cores, simdirs, simulator="./simulator/sim", config_path="./config/config.xml", network_path="./config/network.xml"):

    Parallel(n_jobs=num_cores)(delayed(run_single_sim)
                               (simulator, config_path, network_path, simdir) for simdir in simdirs)
