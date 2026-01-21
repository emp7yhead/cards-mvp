import logging

from backend.app.logging.request_id_filter import RequestIdFilter

LOG_FORMAT = (
    "%(asctime)s "
    "[%(levelname)s] "
    "|%(request_id)s| "
    "%(name)s: %(message)s"
)


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)
