import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import settings

print(settings.API_ID)
print(settings.API_HASH)