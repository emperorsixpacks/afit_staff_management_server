from management_server.utils.model_helpers import get_mobile_prefix, MobilePrefix

def phone_number_vaidator(phone_number:str) -> MobilePrefix | None:
    """
    Validates a phone number and returns the corresponding MobilePrefix if found, None otherwise.

    Parameters:
        phone_number (str): The phone number to validate.

    Returns:
        MobilePrefix | None: The MobilePrefix if the phone number matches any network, otherwise None.
    """
    first_four_digites = phone_number[:4]
    first_five_digits = phone_number[:5]
    mobile_networks = get_mobile_prefix()

    for network in mobile_networks:
        if first_four_digites in network.prefixes or first_five_digits in network.prefixes:
            return network.network
    return None