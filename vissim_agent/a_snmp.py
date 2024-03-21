import sys
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.proto.api import v2c
from vissim_agent.a_class import *
from vissim_agent.a_snmp import *

agent = agent_class()

agent.snmp_engine = engine.SnmpEngine()

# Transport setup
# UDP over IPv4
config.addTransport(
    agent.snmp_engine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('0.0.0.0', 10161))
)

# SNMPv1 Setup
config.addV1System(agent.snmp_engine, 'my-area', agent.snmp_community)

# SNMPv2c Setup
config.addVacmUser(agent.snmp_engine, 2, 'my-area', 'noAuthNoPriv', agent.oid_base)

# Create an SNMP context
agent.snmp_context = context.SnmpContext(agent.snmp_engine)


agent.mib_builder = agent.snmp_context.getMibInstrum().getMibBuilder()

agent.mib_scalar, agent.mib_scalar_instance = agent.mib_builder.importSymbols(
    'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance'
)

class MyStaticMibScalarInstance(agent.mib_scalar_instance):
    def getValue(self, name, idx, **context):
        name_str = str(name)
        if "(1, 3, 6, 1, 4, 1, 13267, 3, 2, 1, 2, 0)" in name_str:
            received_message = "utcType2AppVersion"

        if "(1, 3, 6, 1, 4, 1, 13267, 3, 2, 2, 9)" in name_str:
            received_message = "utcType2ReplyByExceptionKeepAlive"

        if "(1, 3, 6, 1, 4, 1, 13267, 3, 2, 4, 1, 0)" in name_str:
            received_message = "utcType2OperationMode"

        if "(1, 3, 6, 1, 4, 1, 13267, 3, 2, 4, 2, 1, 5, 9740, 7)" in name_str:
            received_message = "utcControlFn"

        if "(1, 3, 6, 1, 4, 1, 13267, 3, 2, 4, 2, 1, 6)" in name_str:
            received_message = "utcControlSFn"

        if "(1, 3, 6, 1, 4, 1, 13267, 4)" in name_str:
            received_message = "objReceiveConfigbyUDP"

        if "(1, 3, 6, 1, 4, 1, 13267, 5, 3)" in name_str:
            received_message = "objKeepAliveProgramacao"

        if "(1, 3, 6, 1, 4, 1, 13267, 5, 12)" in name_str:
            received_message = "objIdEquipamento"

        print(f"Received: {name_str} = {received_message}")

        response_message = f"You sent {received_message}"
        return self.getSyntax().clone(response_message)

agent.mib_builder.exportSymbols(
    '__MY_MIB', agent.mib_scalar(agent.oid_base, v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (3,2,1,2,0,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (3,2,2,9,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (3,2,4,1,0,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (3,2,4,2,1,5,9740,7,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (3,2,4,2,1,6,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (4,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (5,3,), v2c.OctetString()),
    MyStaticMibScalarInstance(agent.oid_base, (5,12,), v2c.OctetString())
)

# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(agent.snmp_engine, agent.snmp_context)
cmdrsp.NextCommandResponder(agent.snmp_engine, agent.snmp_context)
cmdrsp.BulkCommandResponder(agent.snmp_engine, agent.snmp_context)

def run_snmp_thread():
    agent = agent_class()

    agent.snmp_engine.transportDispatcher.jobStarted(1)

    try:
        agent.snmp_engine.transportDispatcher.runDispatcher()
    finally:
        agent.snmp_engine.transportDispatcher.closeDispatcher()
