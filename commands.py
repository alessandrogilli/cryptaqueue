import os


def discovery():
    try:
        os.system(f'venv/bin/python send_to_chat.py --direct "Hi there!"')
    except FileNotFoundError:
        print(f"Error launching the script")
