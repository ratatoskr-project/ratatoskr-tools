import os
import csv


def retrieve_bandwidth(path, interval=500):
    """
    Retrieve the bandwidth csv file for the given path.

    Parameters
    ----------
    path : str
        path of the bandwidth csv file.
    interval : int, optional
        Set the interval to calculate the bandwidth within this range and
        the unit is nano second, by default 500

    Returns
    -------
    tuple
        The 1st variable is the time and 2nd variable is the calculate bandwidth
        at that moment.
    """

    csv_file = open(path, newline='')
    bw_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    next(bw_reader)

    temp_time = []
    temp_bits = []
    x_time, y_bandwidth = [], []
    for time, bits in bw_reader:
        temp_time.append(float(time)/1000.0)
        temp_bits.append(float(bits))
        delta = temp_time[-1] - temp_time[0]
        while(delta > interval):
            temp_time.pop(0)
            temp_bits.pop(0)
            delta = temp_time[-1] - temp_time[0]
        if delta > 0:
            x_time.append(temp_time[-1])
            y_bandwidth.append(sum(temp_bits)/delta)

    return x_time, y_bandwidth


def retrieve_input_bandwidth(directory, interval=500):
    """
        Retrieve the output bandwidth csv (report_Bandwidth_Input.csv)
        inside the provided directory.

    Parameters
    ----------
    directory : str
        the path of the directory that contains the files.
    interval : int, optional
        Set the interval to calculate the bandwidth within this range and
        the unit is nano second, by default 500

    Returns
    -------
    tuple
        The 1st variable is the time and 2nd variable is the calculate bandwidth
        at that moment.
    """
    path = os.path.join(directory, "report_Bandwidth_Input.csv")
    return retrieve_bandwidth(path, interval)


def retrieve_output_bandwidth(directory, interval=500):
    """
        Retrieve the output bandwidth csv (report_Bandwidth_Output.csv)
        inside the provided directory.

    Parameters
    ----------
    directory : str
        the path of the directory that contains the files.
    interval : int, optional
        Set the interval to calculate the bandwidth within this range and
        the unit is nano second, by default 500

    Returns
    -------
    tuple
        The 1st variable is the time and 2nd variable is the calculate bandwidth
        at that moment.
    """
    path = os.path.join(directory, "report_Bandwidth_Output.csv")
    return retrieve_bandwidth(path, interval)


def retrieve_inoutput_bandwidth(directory, interval=500):
    """
        Retrieve the input and output bandwidth csvs (report_Bandwidth_Input.csv &
        report_Bandwidth_Output.csv) inside the provided directory.

    Parameters
    ----------
    directory : str
        the path of the directory that contains the files.
    interval : int, optional
        Set the interval to calculate the bandwidth within this range and
        the unit is nano second, by default 500

    Returns
    -------
    tuple
        The 1st and 2nd elements are the retrieved input and output bandwidth respectively.
        Each element contains the time (x-axis) and bandwidth (y-axis) data.
    """
    return retrieve_input_bandwidth(directory, interval), \
        retrieve_output_bandwidth(directory, interval)
