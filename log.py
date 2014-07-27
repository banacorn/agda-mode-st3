import logging

class Log(object):

    logger = None

    """docstring for Log"""
    def __init__(self):
        super(Log, self).__init__()
        if not Log.logger:
            Log.logger = logging.getLogger('whatever logger you piece of Python shit')


            # Log.logger.setLevel(logging.DEBUG)
            Log.logger.setLevel(logging.INFO)
# 
            formatter = logging.Formatter(fmt='%(module)s %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            Log.logger.handlers = []
            Log.logger.addHandler(handler)

logger = Log().logger