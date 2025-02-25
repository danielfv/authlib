"""
    authlib.jose.rfc7516
    ~~~~~~~~~~~~~~~~~~~~~

    This module represents a direct implementation of
    JSON Web Encryption (JWE).

    https://tools.ietf.org/html/rfc7516
"""

from .jwe import JsonWebEncryption
from .models import JWEAlgorithm, JWEEncAlgorithm, JWEZipAlgorithm

JWE = JsonWebEncryption

__all__ = [
    'JWE', 'JsonWebEncryption',
    'JWEAlgorithm', 'JWEEncAlgorithm', 'JWEZipAlgorithm'
]
