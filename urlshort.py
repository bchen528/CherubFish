import hashlib
import sys


def urlshort(url):
    return hashlib.sha256(str(url).encode('utf-8')).hexdigest()[0:6]    

