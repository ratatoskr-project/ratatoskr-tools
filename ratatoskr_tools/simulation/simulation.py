import multiprocessing
import os
import subprocess

from joblib import Parallel, delayed


def make_all_simdirs(basedir, restarts):
    """
    Create the dummy simulation directories according to the given restarts value.

    Parameters
    ----------
    basedir : str
        The base directory that will contain all dummy simulation directories.
    restarts : int
        The amount of the simulation that will be repeated.

    Returns
    -------
    list(str)
        A list of dummy simulation directories.
    """

    simdirs = ["/".join([basedir, "sim{}".format(restart)])
               for restart in range(restarts)]
    cmds = [" ".join(["mkdir", simdir]) for simdir in simdirs]

    for cmd in cmds:
        os.system(cmd)

    return simdirs


def remove_all_simdirs(basedir, restarts):
    """
    Remove the created dummy simulation directories and all the files which they contains.

    Parameters
    ----------
    basedir : str
        The base directory that will contain all dummy simulation directories.
    restarts : int
        The amount of the simulation that will be repeated.
    """

    simdirs = ["/".join([basedir, "sim{}".format(restart)])
               for restart in range(restarts)]
    cmds = [" ".join(["rm -rf", simdir]) for simdir in simdirs]

    for cmd in cmds:
        os.system(cmd)


def run_single_sim(simulator, config_path, network_path, output_dir=".", stdout=subprocess.DEVNULL, **kwargs):
    """
    Run the simulation once according to the given config_path and network_path.
    Then, the result of the simulation is outputted to the output_dir.

    Parameters
    ----------
    simulator : str
        The path of the simulator executor "./sim"
    config_path : str
        The path of input "config.xml" file for the simulator.
    network_path : str, optional
        The path of input "network.xml" file for the simulator.
    output_dir : str, optional
        The directory of the simulation result which is stored, by default "."
    stdout : [type]
        It accept all the possible argument option "stdout" in the function subprocess.run().
        If it is a string type value, then the output of the program is written to the file
        "output_dir/stdout", by default subprocess.DEVNULL
    """
    os.environ['SYSTEMC_DISABLE_COPYRIGHT_MESSAGE'] = "1"

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    if type(stdout) is str:
        if not os.path.isdir(os.path.dirname(stdout)):
            os.makedirs(os.path.dirname(stdout))
        stdout = open(stdout, "w")

    config_path = "--configPath=" + config_path
    network_path = "--networkPath=" + network_path
    output_dir = "--outputDir=" + output_dir

    args = [simulator, config_path, network_path, output_dir]

    for key, val in kwargs.items():
        args.append("--{}={}".format(key, val))

    try:
        subprocess.run(args, stdout=stdout, check=True)
    except subprocess.CalledProcessError:
        print("ERROR:", args)


def run_parallel_multiple_sims(simdirs, simulator, config_path, network_path,
                               num_cores=multiprocessing.cpu_count()):
    """
    Run the simulation parallely.

    Parameters
    ----------
    simdirs : list(str)
        The list of dummy simulation directories.
    simulator : str
        The path of the simulator executor "./sim"
    config_path : str
        The path of input "config.xml" file for the simulator.
    network_path : str, optional
        The path of input "network.xml" file for the simulator.
    num_cores : int, optional
        The number of parallel threads to parallel the simulation process,
        by default multiprocessing.cpu_count()
    """

    Parallel(n_jobs=num_cores)(delayed(run_single_sim)
                               (simulator, config_path, network_path, simdir) for simdir in simdirs)
