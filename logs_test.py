from class_logger import LoggerSetup

# Initialize the logger
LOGGER = LoggerSetup()
# LOGGER = LoggerSetup(
#     name="root",
#     log_file="test.log",
# )

# Get the logger
logger = LOGGER.logger
print(logger)

# Log some messages
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")

# delete logger
LOGGER.delete()
