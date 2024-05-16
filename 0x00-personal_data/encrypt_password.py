#!/usr/bin/env python3
""" Encrypting passwords """


import bcrypt

def hash_password(password: str) -> str:
    """ hash password """
    b_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(b_password, bcrypt.gensalt())
    return hashed_password
