import logging

from backend.app.logging.extra_fileds_filter import ExtraFieldsFilter
from backend.app.logging.request_id_filter import RequestIdFilter

LOG_FORMAT = (
    "%(asctime)s "
    "[%(levelname)s] "
    "[request_id=%(request_id)s]"
    "[session_id=%(session_id)s]"
    "[topic_id=%(topic_id)s]"
    "[participant_id=%(participant_id)s]"
    "%(name)s: %(message)s"
)


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.addFilter(RequestIdFilter())
    handler.addFilter(ExtraFieldsFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)
