import json
import pytest
import pyotp
import requests
import uuid

from tests import restmail


@pytest.fixture
def capabilities(request, capabilities):
    driver = request.config.getoption('driver')
    if capabilities.get('browserName', driver).lower() == 'firefox':
        capabilities['marionette'] = True
    return capabilities


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium


@pytest.fixture
def ldap(variables):
    return variables['ldap_user']


@pytest.fixture
def passcode(secret_seed, counter):
    hotp = pyotp.HOTP(secret_seed)
    return hotp.at(counter)


@pytest.fixture
def token(variables):
    return variables['token']


@pytest.fixture
def counter_api(variables):
    return variables['counter_API_endpoint']


@pytest.fixture
def increase_otp_counter(counter_api):
    r = requests.get(counter_api)
    return r.json()


@pytest.fixture
def access_token(token):
    headers = {'content-type': 'application/json'}
    data = {
        "client_id": token['client_id'],
        "client_secret": token['client_secret'],
        "audience": token['audience'],
        "grant_type": "client_credentials"
    }
    response = requests.post(token['url'], data=json.dumps(data), headers=headers)
    return json.loads(response.content)['access_token']


@pytest.fixture
def new_email():
    return 'mozillians_{0}@restmail.net'.format(uuid.uuid1())


@pytest.fixture
def new_user(new_email):
    return {'email': new_email}


@pytest.fixture
def login_link(username):
    mail = restmail.get_mail(username)
    mail_content = mail[0]['text'].replace('\n', ' ').replace('amp;', '').split(" ")
    for link in mail_content:
        if 'passwordless/verify_redirect' in link:
            return link
