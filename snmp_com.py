import sys
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.proto.api import v2c


oid_base = (1,3,6,1,4,1,13267)

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('0.0.0.0', 10161))
)

# SNMPv2c setup

# SecurityName <-> CommunityName mapping.
config.addV1System(snmpEngine, 'my-area', 'public')

# Allow read MIB access for this user / securityModels at VACM
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', oid_base)

# Create an SNMP context
snmpContext = context.SnmpContext(snmpEngine)

# --- create custom Managed Object Instance ---

mibBuilder = snmpContext.getMibInstrum().getMibBuilder()

MibScalar, MibScalarInstance = mibBuilder.importSymbols(
    'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance'
)


class MyStaticMibScalarInstance(MibScalarInstance):
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

        response_message = f"You sent {name} = {received_message}"
        return self.getSyntax().clone(response_message)


mibBuilder.exportSymbols(
    '__MY_MIB', MibScalar(oid_base, v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (3,2,1,2,0,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (3,2,2,9,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (3,2,4,1,0,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (3,2,4,2,1,5,9740,7,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (3,2,4,2,1,6,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (4,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (5,3,), v2c.OctetString()),
    MyStaticMibScalarInstance(oid_base, (5,12,), v2c.OctetString())    
)

# --- end of Managed Object Instance initialization ----

# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transportDispatcher.jobStarted(1)

# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()

finally:
    snmpEngine.transportDispatcher.closeDispatcher()
