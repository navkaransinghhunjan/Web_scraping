# Django API Log Checker

This Python script logs into a Django-based admin panel to check API logs for specific error codes (400 and 500). It retrieves the total count of logs for various API types, such as `diagnostic`, `mer`, `ecg`, `tmt`, and `telemer`, allowing easy monitoring of these API responses.

## Features

- Logs into the Django admin panel.
- Retrieves and displays log counts for different API types and error codes.
- Uses environment variables for secure storage of credentials and URLs.

## Prerequisites

- Python 3.x
- `requests` library for HTTP requests.
- `BeautifulSoup` from `bs4` for HTML parsing.
- `python-dotenv` for environment variable management.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/django-api-log-checker.git
   cd django-api-log-checker
