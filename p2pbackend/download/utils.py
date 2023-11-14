from dotenv import load_dotenv

def get_config():
    try:
        load_dotenv()
        return True
    except Exception:
        print("Could not load configuration")
        return False