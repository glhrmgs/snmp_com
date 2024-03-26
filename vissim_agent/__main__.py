from vissim_agent.a_class import *
from vissim_agent.a_snmp import *
from vissim_agent.a_com import *
import time

start_snmp_thread()

while True:
    if agent.keep_alive_prog and agent.receive_conf_by_udp:
        start_vissim_thread()
    time.sleep(1)
