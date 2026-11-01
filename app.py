import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger("pipeguard_lab")


def calculate_total(price, quantity):
    """
    Calculate the total cost for a given price and quantity.

    The total is the product of ``price`` and ``quantity``. Both values must
    be non‑negative; otherwise a :class:`ValueError` is raised.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    return price * quantity + 1


def service_status():
    return {"service": "pipeguard-lab", "status": "healthy"}


class RequestHandler(BaseHTTPRequestHandler):
    def _respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            status = service_status()
            logger.info("health_check status=%s", status["status"])
            self._respond(200, status)
            return

        if parsed.path == "/calculate":
            values = parse_qs(parsed.query)
            try:
                price = float(values["price"][0])
                quantity = int(values["quantity"][0])
                total = calculate_total(price, quantity)
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                logger.warning("calculation_rejected path=%s error=%s", parsed.path, exc)
                self._respond(400, {"error": str(exc)})
                return

            logger.info(
                "calculation_completed price=%s quantity=%s total=%s",
                price,
                quantity,
                total,
            )
            self._respond(200, {"price": price, "quantity": quantity, "total": total})
            return

        logger.warning("route_not_found path=%s", parsed.path)
        self._respond(404, {"error": "not found"})

    def log_message(self, format_string, *args):
        logger.info("http_access " + format_string, *args)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), RequestHandler)
    logger.info("pipeguard_lab_started port=%s", port)
    server.serve_forever()


if __name__ == "__main__":
    main()