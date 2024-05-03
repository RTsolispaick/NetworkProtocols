import socket
from typing import List, Optional

from DNS_server.resources import dependencies
from DNS_server.dns_data import dns_packer
from DNS_server.dns_data.data import DNSPackage, QueryClass, QueryType

settings = dependencies.get_server_settings()


# Выполняем рекурсивный запрос к ДНС серверу
def resolve(
        q_request: bytes,
        server_ip: str = settings["root_server_ip"],
        server_port: int = settings["root_server_port"],
) -> Optional[DNSPackage]:
    response = _ask_dns_server(q_request, server_ip, server_port)
    response_package = DNSPackage(response)

    # в случае, если есть ответы на вопросы в принятом пакете,
    # возвращаем полученное сообщение
    if response_package.header.an_count > 0:
        return response_package

    # если присутствуют авторитетные записи,
    # то разрешаем каждые из этих имен в IP-адреса
    if response_package.header.ns_count > 0:
        for ar in response_package.authoritative_records:
            for ad_r in response_package.additional_records:
                if ad_r.r_type == QueryType.A:
                    return resolve(q_request, ad_r.r_data)

            for ip in _get_ips_by_name(response_package.header.id, ar.r_data):
                return resolve(q_request, ip)


# Пытаемся разрешить через ДНС сервер доменное имя в ip-адрес
def _get_ips_by_name(
        r_id: int,
        name: str,
        server_ip: str = settings["root_server_ip"],
        server_port: int = settings["root_server_port"],
) -> Optional[List[str]]:
    q_request = dns_packer.get_request(
        r_id,
        name,
        QueryType.A,
        QueryClass.IN,
    )

    resolver_package = resolve(q_request, server_ip, server_port)

    if resolver_package is not None:
        return [ra.r_data for ra in resolver_package.answer_records]


# Отправляем запрос на ДНС сервер и получаем ответ
def _ask_dns_server(request: bytes, dns_server_ip: str, dns_server_port=53) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.connect((dns_server_ip, dns_server_port))
        sock.settimeout(None)
        sock.send(request)
        return sock.recv(settings["request_size"])
