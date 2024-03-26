from vissim_agent.a_class import *
import win32com.client as com
import platform, threading, time, pythoncom

agent = agent_class()

def dispatch_vissim():
    pythoncom.CoInitialize()
    vissim = com.Dispatch("Vissim.Vissim.220")

    while True:
        time.sleep(1)

def start_com_thread():
    com_thread = threading.Thread(target=dispatch_vissim)
    com_thread.start()    

def start_vissim_thread():
    if not agent.client_connected:
        my_os = platform.system()
        if "Windows" in my_os:
            print(f"SNMP COM: starting Vissim on {my_os}")
            dispatch_vissim()
            agent.client_connected = True
        else:
            print(f"SNMP COM: client connected on {my_os}")
            agent.client_connected = True
