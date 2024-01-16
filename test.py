import time
print()

from datetime import datetime

# Get current time
current_time = datetime.now().strftime('%H-%M')

print("Current time in HR-Min format:", current_time)