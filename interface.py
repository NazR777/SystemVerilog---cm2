import re
from core import *
from svparser import *

token_regex = re.compile(
    "|".join(
        f"(?P<{name}>{pattern})"
        for name, pattern in TOKENS
    )
)

