from datetime import datetime
import logging
import os.path


class Logger():
    def __init__(self, name):
        FORMAT = '%(asctime)-15s %(message)s'
        formatter = logging.Formatter(FORMAT)
        self.log_adapter = logging.getLogger(name)
        self.log_adapter.setLevel(logging.DEBUG)
        fh = logging.FileHandler(
            './logger/logger-{}.log'.format(datetime.now().strftime('%Y-%m-%d')), 'a')
        fh.setFormatter(formatter)
        self.log_adapter.addHandler(fh)

    def d(self, msg):
        self.log_adapter.debug(msg)

    def i(self, msg):
        self.log_adapter.info(msg)

    def w(self, msg):
        self.log_adapter.warning(msg)

    def e(self, msg):
        self.log_adapter.error(msg)

    def c(self, msg):
        self.log_adapter.critical(msg)


log = Logger('main')
log.i('log a info')
log.d('just for test12312')
