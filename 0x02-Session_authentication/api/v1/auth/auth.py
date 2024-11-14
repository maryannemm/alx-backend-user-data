#!/usr/bin/env python3
"""
Auth module to manage API authentication.
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """
    Auth class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if the current path requires authentication.
        Now supports wildcard '*' at the end of excluded paths.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        # Append slash at the end of the path if missing
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Allow wildcard '*' at the end of excluded_path
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                # Exact match
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Return the value of the header Authorization.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user.
        """
        return None

