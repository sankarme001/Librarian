import logging

# Create a logger object
logger = logging.getLogger('Librarian:')
logger.setLevel(logging.INFO)

# Define the format for log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler to log to a file
file_handler = logging.FileHandler('librarian_log.log')
file_handler.setFormatter(formatter)

# Create a stream handler to log to the terminal
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add both handlers to the logger   
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
