"""
The generate_session_key function creates a random 75-character session key
using alphanumeric characters and specific symbols.
"""

import string, random


def generate_session_key() -> str:
    key = []
    for _ in range(75):
        key.append(random.choice(string.ascii_letters + string.digits + "!,;-_+#&%=?$"))

    return "".join(key)
