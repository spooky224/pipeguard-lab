def calculate_total(price, quantity):
    """
    Calculate the total cost for a given price and quantity.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    return price * quantity + 1


def service_status():
    return {"service": "pipeguard-lab", "status": "healthy"}
