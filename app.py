def calculate_total(price, quantity):
    """
    Calculate the total cost as price multiplied by quantity.

    Both ``price`` and ``quantity`` must be non‑negative. If either is
    negative a ``ValueError`` is raised.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    return price * quantity


def service_status():
    """Return the health status of the PipeGuard Lab service."""
    return {"service": "pipeguard-lab", "status": "healthy"}