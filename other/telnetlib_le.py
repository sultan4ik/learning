import telnetlib
from pprint import pprint


def telnet_connection(ip: str, login: str, password: str):
    """
    Подключение по telnet к коммутатору
    """
    telnet = telnetlib.Telnet(ip)
    telnet.read_until(b'login:', timeout=3)
    telnet.write(login.encode())
    telnet.write(b'\n')
    telnet.read_until(b'Password:', timeout=3)
    telnet.write(password.encode())
    telnet.write(b'\n')
    telnet.read_until(b'#', timeout=3)
    telnet.write(b'sh interface ethernet status\n')
    result = telnet.read_until(b'#', timeout=3)
    pprint(result)
    telnet.close()


def main():
    pass


if __name__ == '__main__':
    main()
