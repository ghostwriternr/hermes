"""
Repo settings
"""
from os.path import join, dirname
from dotenv import load_dotenv

def load_env():
    """
    Method to load environment variables
    """
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

if __name__ == "__main__":
    load_env()
