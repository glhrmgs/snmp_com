# snmp_com
Implement an SNMP Agent with COM Interface support

## To start the SNMP Agent do:
```
$ python3 snmp_com.py
```

## To communicate with it, do:
After running the snmp_com, which is the agent, do:
- On Windows:
```
> SnmpGet.exe -r:127.0.0.1 -p:10161 -v:2c -c:public -o:utmc_command
```

- On Linux:
```
$ snmpget -v2c -cpublic 127.0.0.1:10161 utmc_command
```
