import logging


def logger(name: str):
    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    new_logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    # Add the console handler to the logger
    new_logger.addHandler(console_handler)
    return new_logger
