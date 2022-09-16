import telnetlib
import pprint


telnet = telnetlib.Telnet('x.x.x.x')
telnet.read_until(b'login:', timeout=3)
telnet.write(b'xxxx\n')
telnet.read_until(b'Password:', timeout=3)
telnet.write(b'xxxxx\n')
telnet.read_until(b'#', timeout=3)
telnet.write(b'sh interface ethernet status\n')
result=telnet.read_until(b'#', timeout=3)
pprint(result)
telnet.close()