from vissim_agent.a_class import *
from vissim_agent.a_snmp import *

agent = agent_class()

agent.snmp_engine.transportDispatcher.jobStarted(1)
try:
    agent.snmp_engine.transportDispatcher.runDispatcher()

finally:
    agent.snmp_engine.transportDispatcher.closeDispatcher()
