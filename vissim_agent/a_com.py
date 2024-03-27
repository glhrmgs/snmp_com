from vissim_agent.a_class import *
from vissim_agent.a_config import *
import platform, threading, time

agent = agent_class()

def dispatch_vissim():
    import win32com.client as com

    vissim_version = config['vissim']['version']
    vissim = com.Dispatch(vissim_version)

    vissim_micromodel = config['vissim']['micromodel']
    print(f"SNMP COM: opening {vissim_micromodel}")
    vissim.LoadNet(vissim_micromodel)

    print(f"SNMP COM: warming up model")

    while True:
        time.sleep(1)

def vissim_thread():
    com_thread = threading.Thread(target=dispatch_vissim)
    com_thread.start()

def start_com_thread():
    my_os = platform.system()
    if "Windows" in my_os:
        print(f"SNMP COM: starting Vissim")
        vissim_thread()
