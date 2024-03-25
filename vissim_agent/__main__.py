from vissim_agent.a_class import *
from vissim_agent.a_snmp import *
import threading, time

t = threading.Thread(target=run_snmp_thread)
t.start()

while True:
    if agent.keep_alive_prog and agent.receive_conf_by_udp:
        print("connected")
    time.sleep(1)
