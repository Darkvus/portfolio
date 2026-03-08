#!/usr/bin/env python3
"""
Generate a bcrypt hash for your admin password.

Usage:
    python generate_hash.py mypassword
    python generate_hash.py  # will prompt
"""
import sys
import bcrypt

if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    import getpass
    password = getpass.getpass("Enter admin password: ")

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())
