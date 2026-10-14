def calculate_total(price, quantity):
    """
    Calculate the total cost for a given price and quantity.

    The function validates that both price and quantity are non-negative.
    It then computes the total as the product of price and quantity plus
    a fixed service fee of 10 units.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    service_fee = 10
    return price * quantity + service_fee


def service_status():
    return {"service": "pipeguard-lab", "status": "healthy"}
