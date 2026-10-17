def calculate_total(price, quantity):
    """
    Calculate the total cost for a given price and quantity.

    Returns the product of price and quantity. Raises ValueError if either
    argument is negative.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    return price * quantity


def service_status():
    """Return a dict indicating the service health status."""
    return {"service": "pipeguard-lab", "status": "healthy"}