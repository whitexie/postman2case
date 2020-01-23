import logging
import functools


def log(func):
    @functools.wraps(func)
    def decoratore(*args, **kwargs):
        if args:
            logging.debug(args)
        if kwargs:
            logging.debug(kwargs)
        result = func(*args, **kwargs)
        return result

    return decoratore
