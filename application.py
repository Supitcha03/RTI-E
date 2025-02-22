# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:05:05 2021

@author: krong
"""
from rti_sim import RTISimulation
from rti_sys import RTIConnection, RTIProcess, ReceiveThread
# from rti_exp_position import process_position
# from rti_exp_formfactor import process_formfactor
# from rti_exp_alpha import process_alpha
# from rti_exp_sensor import process_sensor
# from rti_exp_voxel import process_voxel
# from rti_exp_weightalgorithm import process_weightalgorithm
# from rti_animation import process_animate


def main():
    rti = RTISimulation()
    rtiProcess = RTIProcess(rti) 
    rtiConn = RTIConnection(rtiProcess, 'COM3')
    tReceiveRTI = ReceiveThread(1,
                                'LoRa Receive Thread',
                                1,
                                rtiConn)
    try:
        tReceiveRTI.start()
    except:
        raise Exception('Cannot Start Thread')
    print("Begin .. RTI Update")
    # rtiProcess.updateIM()


if __name__ == '__main__':
    # Experimental RTI Process
    main()
    # Example of Simulation Process
    # rti = RTISimulation()
    # process_animate(rti)
    # process_position(rti)
    # process_formfactor(rti)
    # process_alpha(rti)
    # process_sensor(rti)
    # process_voxel(rti)
    # process_weightalgorithm(rti)
