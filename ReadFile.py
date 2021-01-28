import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def readosci(filename):
    data = pd.read_csv(filename)
    time = data["Time"]
    ch1 = data["Channel 1"]
    ch2 = data["Channel 2"]

    return time,ch1,ch2


def readospek(filename):
    data = pd.read_csv(filename)
    frek = data["Frequency"]
    t1 = data["Trace 1"]


    return frek,t1

def readnetwoek(filename):
    data = pd.read_csv(filename)
    frek = data["Frequency"]
    ch1 = data["Channel 1"]
    ch2 = data["Channel 2"]

    return frek,ch1,ch2


