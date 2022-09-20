import os
import sys
import logging
import logging.handlers


class LogFactory:

    formatStr = "%(asctime)s %(levelname)s %(filename)s:%(lineno)3d : %(message)s"
    _log_ = None

    @staticmethod
    def get_file_logger(path=None, program=None, level=logging.DEBUG):
        def __getLogFile(log_path, program):
            if not log_path:
                rpath = os.path.dirname(sys.argv[0])
                log_path = os.path.join(rpath, "..", "log")

            if not program:
                program = str(os.path.basename(sys.argv[0]).split(".")[0])

            log_file = os.path.join(log_path, f"{program}.log")
            error_log_file = os.path.join(log_path, f"{program}_ERROR.log")
            return log_file, error_log_file

        def __init(path, program, level):
            LogFactory._log_ = logging.getLogger()

            log_file, error_log_file = __getLogFile(path, program)

            formatter = logging.Formatter(LogFactory.formatStr)

            handler = logging.handlers.RotatingFileHandler(log_file, "a", 10 * 1024 * 1024, 9)
            handler.setFormatter(formatter)
            handler.setLevel(level)
            LogFactory._log_.addHandler(handler)

            error_handler = logging.handlers.RotatingFileHandler(error_log_file, "a", 10 * 1024 * 1024, 9)
            error_handler.setFormatter(formatter)
            error_handler.setLevel(logging.ERROR)
            LogFactory._log_.addHandler(error_handler)

            LogFactory._log_.setLevel(level)

        if not LogFactory._log_:
            __init(path, program, level)
        return LogFactory._log_

    @staticmethod
    def get_stream_logger():
        LogFactory._log_ = logging.getLogger()

        formatter = logging.Formatter(LogFactory.formatStr)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        LogFactory._log_.addHandler(handler)
        LogFactory._log_.setLevel(logging.DEBUG)

        return LogFactory._log_


def main():
    log = LogFactory.getLogger("./", "test")
    log.info("info test")
    log.warning("warning test")
    log.error("error test")
    log.debug("debug test")
    log.exception("exception test")


if __name__ == "__main__":
    main()
