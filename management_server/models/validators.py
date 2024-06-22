from management_server.models.helpers import get_mobile_prefix, MobilePrefix

def phone_number_vaidator(phone_number:str) -> MobilePrefix | None:
    first_four_digites = phone_number[:4]
    first_five_digits = phone_number[:5]
    mobile_networks = get_mobile_prefix()

    for network in mobile_networks:
        if first_four_digites in network.prefixes or first_five_digits in network.prefixes:
            return network
    return None