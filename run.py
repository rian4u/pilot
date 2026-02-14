import logging
from pathlib import Path

from src.app import run
from src.config_loader import load_config


def setup_logging(config):
    log_file = Path(config["logging"]["file"])
    log_file.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config["logging"]["level"]),
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def main():
    config = load_config()
    setup_logging(config)

    try:
        run()
    except Exception:
        logging.exception("Unhandled exception occurred")
        raise


if __name__ == "__main__":
    main()
