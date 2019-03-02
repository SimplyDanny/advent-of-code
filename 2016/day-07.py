import re

from common import print_results, readlines


class IPAddress:
    SPLIT_AT_REGEX = re.compile(r'\[(\w+)\]')
    AAAA_REGEX = re.compile(r'^.*(\w)(\w)\2\1.*$')
    ABA_REGEX = re.compile(r'(?=((\w)(\w)\2))')

    def __init__(self, address):
        self.address = address
        address_parts = self.SPLIT_AT_REGEX.split(address)
        self.hypernet_parts = address_parts[1::2]
        self.supernet_parts = address_parts[::2]

    def __has_abba(self, part):
        aaaa = self.AAAA_REGEX.match(part)
        return aaaa and aaaa.group(1) != aaaa.group(2)

    def __get_babs_of_abas(self):
        babs = []
        for part in self.supernet_parts:
            abas = self.ABA_REGEX.finditer(part)
            for aba in abas:
                if aba.group(2) != aba.group(3):
                    babs.append(self.__get_bab(aba.group(1)))
        return babs

    def __get_bab(self, aba):
        return aba[1] + aba[0] + aba[1]

    def supports_tls(self):
        return (any(self.__has_abba(part) for part in self.supernet_parts) and not
                any(self.__has_abba(part) for part in self.hypernet_parts))

    def supports_ssl(self):
        babs = self.__get_babs_of_abas()
        for bab in babs:
            if any(bab in part for part in self.hypernet_parts):
                return True
        return False

#### Main part.

ip_addresses = [IPAddress(ip_address) for ip_address in readlines(__file__)]

print_results(
    sum(ip_address.supports_tls() for ip_address in ip_addresses),
    sum(ip_address.supports_ssl() for ip_address in ip_addresses)
)
