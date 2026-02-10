# ===========================
# PROJECT IDEA (HIGH LEVEL)
# ===========================
# This program continuously watches a website for new tour events.
# If a new event appears:
#   1) It saves it to a file
#   2) Sends an email notification
#
# Think of this like a guard who:
#   - Checks a notice board every few seconds
#   - Remembers what he has already seen
#   - Shouts (email) when something new appears


# ===========================
# IMPORTS (TOOLS WE NEED)
# ===========================

# requests:
# Used to send HTTP requests (like a browser)
# Computer logic: Opens a network connection → downloads HTML → returns it as text
import requests

# selectorlib:
# Used to extract specific data from HTML using rules written in YAML
# Computer logic: Parses HTML → matches patterns → extracts text
import selectorlib

# smtplib:
# Used to send emails using SMTP protocol
# ssl:
# Used to create an encrypted connection so passwords are safe
import smtplib, ssl

# os:
# Gives access to operating system features (not used directly here)
import os

# time:
# Used to pause execution (sleep)
# Computer logic: OS pauses the process for given seconds
import time


# ===========================
# CONSTANTS (CONFIGURATION)
# ===========================

# URL of the website we want to monitor
URL = "https://programmer100.pythonanywhere.com/tours/"

# HEADERS:
# Websites may block requests that don't look like browsers
# This makes our request look like it came from Chrome
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/39.0.2171.95 Safari/537.36'
}


# ===========================
# STEP 1: SCRAPE WEBSITE
# ===========================
def scrape(url):
    """
    HUMAN LOGIC:
    - Go to the website
    - Copy the entire page content

    COMPUTER LOGIC:
    - Open TCP connection
    - Send HTTP GET request
    - Receive response bytes
    - Convert bytes → string (HTML)
    """

    response = requests.get(url, headers=HEADERS)

    # response.text contains the full HTML source code as a string
    source = response.text

    return source


# ===========================
# STEP 2: EXTRACT REQUIRED DATA
# ===========================
def extract(source):
    """
    HUMAN LOGIC:
    - From the messy HTML, pick ONLY the tour information

    COMPUTER LOGIC:
    - Load extraction rules from YAML file
    - Build DOM tree from HTML
    - Match selectors
    - Return extracted text as dictionary
    """

    # Load extractor rules defined in extract.yaml
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")

    # extractor.extract(source) returns a dictionary
    # ["tours"] accesses the value defined in YAML
    value = extractor.extract(source)["tours"]

    return value


# ===========================
# STEP 5: SEND EMAIL ALERT
# ===========================
def send_email(message):
    """
    HUMAN LOGIC:
    - Notify user when a new event is found

    COMPUTER LOGIC:
    - Open encrypted SSL socket
    - Authenticate with Gmail SMTP server
    - Send email
    - Close connection
    """

    print("Sending email...")

    host = "smtp.gmail.com"
    port = 465  # SSL-secured SMTP port

    username = "claudenogga1@gmail.com"
    password = "kghjpgmhosqamgbx"  # App password

    receiver = "claudenogga1@gmail.com"

    # Create secure encryption context
    context = ssl.create_default_context()

    # with-block ensures connection is closed automatically
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


# ===========================
# STEP 4: STORE DATA
# ===========================
def store(extracted):
    """
    HUMAN LOGIC:
    - Remember what we have already seen

    COMPUTER LOGIC:
    - Open file in append mode
    - Write data at the end
    - Save to disk
    """

    # "a" mode → append (does NOT erase old data)
    with open("extracted_names.txt", "a") as file:
        file.write(extracted + "\n")


# ===========================
# STEP 3: READ STORED DATA
# ===========================
def read(extracted):
    """
    HUMAN LOGIC:
    - Check past records to avoid duplicates

    COMPUTER LOGIC:
    - Open file
    - Load contents into RAM
    - Return as string
    """

    with open("extracted_names.txt", "r") as file:
        return file.read()


# ===========================
# PROGRAM ENTRY POINT
# ===========================
# This block runs ONLY when this file is executed directly
# Not when imported as a module
if __name__ == "__main__":

    # Infinite loop → program keeps running forever
    # Computer logic: Loop condition is always True
    while True:

        # STEP 1: Scrape website
        scraped = scrape(URL)

        # STEP 2: Extract tour information
        extracted = extract(scraped)

        print(extracted)

        # STEP 3: Read previously stored events
        content = read(extracted)

        # Ignore placeholder text
        if extracted != "No upcoming tours":

            # Check if new data is already known
            # Computer logic:
            #   - Performs substring search
            #   - Character-by-character comparison
            if extracted not in content:

                # STEP 4: Store new tour
                store(extracted)

                # STEP 5: Send notification
                send_email(message="hey, new event was found!")

        # Wait before checking again
        # Computer logic:
        #   - OS pauses this process
        #   - CPU freed for other tasks
        time.sleep(2)
