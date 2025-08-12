# -*- coding: utf-8 -*-


from functions import *
from pathlib import Path
import logging

# Path to credentials file
credentials_path = Path(__file__).parent / "credentials.json"

# Create credentials.json if it does not exist or is empty
if not credentials_path.exists():
    credentials_path.write_text("{}")
    logging.info("File credentials.json created successfully.")
else:
    if credentials_path.stat().st_size == 0:
        credentials_path.write_text("{}")
        logging.info("File credentials.json existed but was empty, filled with '{}'.")

    
