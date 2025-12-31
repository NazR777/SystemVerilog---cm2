import re
from core import *
from svparser import *

token_regex = re.compile(
    "|".join(
        f"(?P<{name}>{pattern})"
        for name, pattern in TOKENS
    )
)

a = block(0, 0, 0, 0, [], "a")
print(a.x)
print(a.final_look)
a.x = "2"
print(a.x)
a.calculate_final_look()
print(a.final_look)