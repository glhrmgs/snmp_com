class agent_class:
    # Singleton instance
    __instance = None

    # SNMP related
    snmp_config = None
    snmp_engine = None
    snmp_context = None
    snmp_community = "public"

    # OID/MIB related
    oid_base = (1,3,6,1,4,1,13267)
    mib_builder = None
    mib_scalar = None
    mib_scalar_instance = None

    # Agent related
    keep_alive_prog = None
    receive_conf_by_udp = None

    # Vissim
    client_connected = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance
