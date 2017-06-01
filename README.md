# CDP Parser

Given output from `show cdp entry *`, this script produces a dictionary for
each device.

```
{'capabilities': 'Router Switch IGMP ',
 'local_int': 'GigabitEthernet1/3',
 'platform': 'cisco WS-C6509-E',
 'remote_id': 'bob.GoreNetwork',
 'remote_int': 'GigabitEthernet2/6',
 'remote_ip': '10.0.0.1',
 'version': 'Cisco IOS Software, s72033_rp Software '
            '(s72033_rp-ADVIPSERVICESK9_WAN-M), Version 12.2(33)SXH5, RELEASE '
            'SOFTWARE (fc1)'},
```
