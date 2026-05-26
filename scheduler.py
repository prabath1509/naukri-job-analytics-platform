import schedule
import time
import os

def run_scraper():

    print("\nRunning scraper now...\n")

    os.system("python main.py")

# -----------------------------------
# TEST EVERY 1 MINUTE
# -----------------------------------

schedule.every().day.at("09:00").do(run_scraper)

print("Scheduler Started...")
print("Waiting for scheduled jobs...")

while True:

    schedule.run_pending()

    time.sleep(1)