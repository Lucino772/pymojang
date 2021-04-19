import time

def get_id():
    return int(time.time()) & 0x0F0F0F0F