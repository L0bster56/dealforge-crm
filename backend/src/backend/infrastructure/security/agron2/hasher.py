from passlib.handlers.argon2 import argon2

from src.backend.application.auth.interfaces.security.hasher import Hasher


class Argon2(Hasher):
    def hash(self,password:str)-> str:
        return argon2.hash(password)

    def verify(self,password:str, hashed_password:str)-> bool:
        return argon2.verify(password, hashed_password)