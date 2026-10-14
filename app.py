def calculate_total(price, quantity):
    """
    Calculate the total cost for a given price and quantity.

    Parameters
    ----------
    price : int or float
        Unit price of the item. Must be non‑negative.
    quantity : int or float
        Number of items. Must be non‑negative.

    Returns
    -------
    int or float
        The total cost computed as ``price * quantity``.

    Raises
    ------
    ValueError
        If either ``price`` or ``quantity`` is negative.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    return price * quantity


def service_status():
    return {"service": "pipeguard-lab", "status": "healthy"}