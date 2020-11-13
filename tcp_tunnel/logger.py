import logging

logger = logging.getLogger('tcp.tunnel')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
logger.addHandler(console_handler)


def info(*args, **kwargs):
    return logger.info(*args, **kwargs)


def debug(*args, **kwargs):
    return logger.debug(*args, **kwargs)


def warning(*args, **kwargs):
    return logger.warning(*args, **kwargs)


def error(*args, **kwargs):
    return logger.error(*args, **kwargs)


if __name__ == '__main__':
    debug('test?')
