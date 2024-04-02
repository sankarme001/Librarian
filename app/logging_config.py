import logging

logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('librarian.log')  # Change the file path here
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)