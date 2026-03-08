#!/usr/bin/env python3
"""
Generate a bcrypt hash for your admin password.

Usage:
    python generate_hash.py mypassword
    python generate_hash.py  # will prompt
"""
import sys
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    import getpass
    password = getpass.getpass("Enter admin password: ")

print(pwd_context.hash(password))
