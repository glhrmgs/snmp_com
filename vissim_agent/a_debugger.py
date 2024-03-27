from vissim_agent.a_class import *

agent = agent_class()

def start_debugger():
    if not agent.client_connected:
        print("SNMP COM: debugger started")
        agent.client_connected = True
    return