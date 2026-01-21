import logging


class ExtraFieldsFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, 'session_id'):
            record.session_id = '-'
        if not hasattr(record, 'topic_id'):
            record.topic_id = '-'
        if not hasattr(record, 'participant_id'):
            record.participant_id = '-'
        return True
