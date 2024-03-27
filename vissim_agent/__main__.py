from vissim_agent.a_class import *
from vissim_agent.a_snmp import *
from vissim_agent.a_com import *
from vissim_agent.a_debugger import *
import time


# Entry Point
start_snmp_thread()
start_com_thread()

while True:
    if agent.keep_alive_prog and agent.receive_conf_by_udp:
        start_debugger()
        agent.keep_alive_prog = False
        agent.receive_conf_by_udp = False
    time.sleep(1)
