def calculate_total(price, quantity):
    """
    Calculate the total cost for a given price and quantity.

    The function validates that both ``price`` and ``quantity`` are non‑negative.
    It then computes the total as the product of ``price`` and ``quantity`` plus
    a fixed service fee of 10 units.

    Args:
        price (float or int): Unit price of the item. Must be >= 0.
        quantity (int): Number of items. Must be >= 0.

    Returns:
        float: The total cost including the service fee.

    Raises:
        ValueError: If ``price`` or ``quantity`` is negative.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    service_fee = 10
    return price * quantity + service_fee


def service_status():
    return {"service": "pipeguard-lab", "status": "healthy"}