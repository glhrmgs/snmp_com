# snmp_com
Implement an SNMP Agent with COM Interface support

## running
$ python3 snmp_com.py

## testing
After running the snmp_com, which is the agent, do:
- On Windows:
\> SnmpGet.exe -r:127.0.0.1 -p:10161 -v:2c -c:public -o:utmc_command
