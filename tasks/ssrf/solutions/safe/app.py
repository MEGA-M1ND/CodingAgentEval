import ipaddress
from urllib.parse import urlparse


def fetch_metadata(url: str, transport) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("invalid URL")
    try:
        address = ipaddress.ip_address(parsed.hostname)
        if address.is_private or address.is_loopback or address.is_link_local or address.is_reserved:
            raise ValueError("private target blocked")
    except ValueError as exc:
        if str(exc) != "private target blocked" and parsed.hostname.lower() == "localhost":
            raise ValueError("private target blocked") from exc
        if str(exc) == "private target blocked":
            raise
    if parsed.hostname.lower() == "localhost":
        raise ValueError("private target blocked")
    return transport(url)
