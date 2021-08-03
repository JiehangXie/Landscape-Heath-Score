import os
import re

def check_ipv6():
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    if len(result[0][0]) >= 16:
        return True
    else:
        return False