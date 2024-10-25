import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credentials and login URL from environment variables
username = os.getenv('DJANGO_USERNAME')
password = os.getenv('DJANGO_PASSWORD')
login_url = os.getenv('DJANGO_LOGIN_URL')

# API log URLs for 400 and 500 error codes
api_urls = {
    'diagnostic': {
        '400': os.getenv('DIAGNOSTIC_400_URL'),
        '500': os.getenv('DIAGNOSTIC_500_URL')
    },
    'mer': {
        '400': os.getenv('MER_400_URL'),
        '500': os.getenv('MER_500_URL')
    },
    'ecg': {
        '400': os.getenv('ECG_400_URL'),
        '500': os.getenv('ECG_500_URL')
    },
    'tmt': {
        '400': os.getenv('TMT_400_URL'),
        '500': os.getenv('TMT_500_URL')
    },
    'telemer': {
        '400': os.getenv('TELEMER_400_URL'),
        '500': os.getenv('TELEMER_500_URL')
    }
}


def login(session):
    """
    Logs into the Django admin site using the provided session.
    """
    login_page = session.get(login_url)
    login_page.raise_for_status()

    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    login_payload = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token,
        'next': '/admin/'
    }

    headers = {
        'Referer': login_url
    }
    response = session.post(login_url, data=login_payload, headers=headers)
    response.raise_for_status()

    if 'Log out' in response.text:
        print("Login successful!")
    else:
        print("Login failed.")
        exit(1)


def check_api_logs(session, url, api_type, status_code):
    """
    Checks the API log page for a given URL and extracts the total log count.

    Parameters:
    - session: the requests session with the authenticated user
    - url: the URL of the log page to check
    - api_type: the type of API (e.g., diagnostic, mer)
    - status_code: the HTTP status code to filter by (400 or 500)
    
    Returns:
    - The total log count as a string, or a message if the paginator is not found.
    """
    try:
        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        paginator = soup.find("p", class_="paginator")

        if paginator:
            total_logs = paginator.text.strip().split()[-5] if api_type in {'ecg', 'tmt'} else paginator.text.strip().split()[-3]
            return f"Total logs for {api_type} API (status {status_code}): {total_logs}"
        else:
            return f"Could not find paginator for {api_type} API (status {status_code})."
    except requests.exceptions.RequestException as e:
        return f"Error accessing {api_type} API log page for status {status_code}: {e}"


if __name__ == "__main__":
    session = requests.Session()
    login(session)

    for api_type, urls in api_urls.items():
        for status_code, url in urls.items():
            print(f"\nChecking {api_type.upper()} API logs for status {status_code}...")
            log_count_message = check_api_logs(session, url, api_type, status_code)
            print(log_count_message)
