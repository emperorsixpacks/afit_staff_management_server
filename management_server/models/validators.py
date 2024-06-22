from management_server.models.helpers import get_mobile_prefix, MobilePrefix

def phone_number_vaidator(phone_number:str) -> MobilePrefix | None:
    mobile_networks = get_mobile_prefix()

    for network in mobile_networks:
        if phone_number in network.prefixes:
            return network
    return None