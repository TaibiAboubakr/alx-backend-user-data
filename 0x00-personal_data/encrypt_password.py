#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password """
    b_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(b_password, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """  validate that the provided password matches the hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
