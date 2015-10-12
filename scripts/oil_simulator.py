#! /usr/bin/env python
import matplotlib.pyplot as plt
from datetime import datetime

from ert.ecl import EclSum
from synthesizer import ShapeCreator, ShapeFunction, OilSimulator


def globalIndex(i, j, k, nx=10, ny=10, nz=10):
    return i + nx * (j - 1) + nx * ny * (k - 1)

def plotVector(title, vectors):
    # plt.figure()

    for index, vector in enumerate(vectors):
        plt.plot(vector, label="R: %d" % index)
    # plt.legend()
    plt.title(title)


if __name__ == '__main__':
    realizations = []
    for realization in range(10):
        ecl_sum = EclSum.writer("PERLIN", datetime(2010, 1, 1), 10, 10, 10)

        ecl_sum.addVariable("FOPT")
        ecl_sum.addVariable("FOPR")
        ecl_sum.addVariable("FGPT")
        ecl_sum.addVariable("FGPR")
        ecl_sum.addVariable("FWPT")
        ecl_sum.addVariable("FWPR")
        ecl_sum.addVariable("FGOR")
        ecl_sum.addVariable("FWCT")
        ecl_sum.addVariable("WOPR", wgname="OP1")
        ecl_sum.addVariable("WOPR", wgname="OP2")
        ecl_sum.addVariable("WWPR", wgname="OP1")
        ecl_sum.addVariable("WWPR", wgname="OP2")
        ecl_sum.addVariable("WGPR", wgname="OP1")
        ecl_sum.addVariable("WGPR", wgname="OP2")
        ecl_sum.addVariable("WGOR", wgname="OP1")
        ecl_sum.addVariable("WGOR", wgname="OP2")
        ecl_sum.addVariable("WWCT", wgname="OP1")
        ecl_sum.addVariable("WWCT", wgname="OP2")
        ecl_sum.addVariable("BPR", num=globalIndex(5, 5, 5))
        ecl_sum.addVariable("BPR", num=globalIndex(1, 3, 8))

        simulator = OilSimulator()
        simulator.addWell("OP1", realization * 997)
        simulator.addWell("OP2", realization * 13)
        simulator.addBlock("5,5,5", realization * 37)
        simulator.addBlock("1,3,8", realization * 31, persistence=0.4)

        for report_step in range(1000):
            t_step = ecl_sum.addTStep(report_step + 1, sim_days=report_step * 2)

            simulator.step(scale=0.001)

            t_step["FOPR"] = simulator.fopr()
            t_step["FOPT"] = simulator.fopt()
            t_step["FGPR"] = simulator.fgpr()
            t_step["FGPT"] = simulator.fgpt()
            t_step["FWPR"] = simulator.fwpr()
            t_step["FWPT"] = simulator.fwpt()
            t_step["FGOR"] = simulator.fgor()
            t_step["FWCT"] = simulator.fwct()

            t_step["WOPR:OP1"] = simulator.opr("OP1")
            t_step["WOPR:OP2"] = simulator.opr("OP2")

            t_step["WGPR:OP1"] = simulator.gpr("OP1")
            t_step["WGPR:OP2"] = simulator.gpr("OP2")

            t_step["WWPR:OP1"] = simulator.wpr("OP1")
            t_step["WWPR:OP2"] = simulator.wpr("OP2")

            t_step["WGOR:OP1"] = simulator.gor("OP1")
            t_step["WGOR:OP2"] = simulator.gor("OP2")

            t_step["WWCT:OP1"] = simulator.wct("OP1")
            t_step["WWCT:OP2"] = simulator.wct("OP2")

            t_step["BPR:5,5,5"] = simulator.bpr("5,5,5")
            t_step["BPR:1,3,8"] = simulator.bpr("1,3,8")

        realizations.append(ecl_sum)


    opr_keys = ["FOPR", "WOPR:OP1", "WOPR:OP2", "FOPT"]
    gpr_keys = ["FGPR", "WGPR:OP1", "WGPR:OP2", "FGPT"]
    wpr_keys = ["FWPR", "WWPR:OP1", "WWPR:OP2", "FWPT"]
    wct_keys = ["WWCT:OP1", "WWCT:OP2", "FWCT"]
    gor_keys = ["WGOR:OP1", "WGOR:OP2", "FGOR"]
    bpr_keys = ["BPR:5,5,5", "BPR:1,3,8"]

    for keys in [opr_keys, gpr_keys, wpr_keys, wct_keys, gor_keys, bpr_keys]:
        plt.figure()
        for index, key in enumerate(keys):
            plt.subplot(len(keys), 1, index + 1)
            values = []
            for realization in realizations:
                values.append(realization[key].values)
            plotVector(key, values)


    plt.show()


    # ecl_sum.fwrite()



