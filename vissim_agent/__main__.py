from vissim_agent.a_class import *
from vissim_agent.a_snmp import *
import threading, time

t = threading.Thread(target=run_snmp_thread)
t.start()

print("marrapaiz")
while True:
    time.sleep(1)
