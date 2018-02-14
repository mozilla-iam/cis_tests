import json
import random
import uuid

import pytest
import requests
import time

from pages.homepage import Homepage
from tests import conftest


class TestMozilliansProfileUpdates:

    @pytest.mark.nondestructive
    def test_update_basic_information(self, base_url, selenium, ldap, person_api_token, counter_api):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        profile_page = settings_page.profile
        existing_username = profile_page.username
        existing_full_name = profile_page.full_name
        new_username = 'username-{0}'.format(str(uuid.uuid4())[:10])
        new_first_name = 'FirstName{0}'.format(str(uuid.uuid4())[:10])
        new_last_name = 'LastName{0}'.format(str(uuid.uuid4())[:10])
        new_full_name = '{0} {1}'.format(new_first_name, new_last_name)
        profile_page.set_username(new_username)
        profile_page.sef_full_name(new_full_name)
        profile_page.click_update_basic_information()
        time.sleep(8)
        api = person_api_token['api']
        user_logs = requests.get(api, headers={
            'Authorization': 'Bearer {0}'.format(conftest.person_api_access_token(person_api_token))})
        assert new_username == json.loads(json.loads(user_logs.content)['body'])['userName']
        assert new_first_name == json.loads(json.loads(user_logs.content)['body'])['firstName']
        assert new_last_name == json.loads(json.loads(user_logs.content)['body'])['lastName']
        assert new_full_name == json.loads(json.loads(user_logs.content)['body'])['displayName']

        # Cleanup
        profile_page.set_username(existing_username)
        profile_page.sef_full_name(existing_full_name)
        profile_page.click_update_basic_information()

    @pytest.mark.nondestructive
    def test_update_emails(self, base_url, selenium, ldap, person_api_token, new_user, counter_api):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        profile_page = settings_page.profile
        primary_email = profile_page.primary_email
        new_email = new_user['email']
        profile_page.add_email(new_email)
        assert new_email in profile_page.secondary_email_address
        time.sleep(8)
        api = person_api_token['api']
        user_logs = requests.get(api, headers={
            'Authorization': 'Bearer {0}'.format(conftest.person_api_access_token(person_api_token))})
        assert primary_email == json.loads(json.loads(user_logs.content)['body'])['emails'][0]['value']
        a = len(json.loads(json.loads(user_logs.content)['body'])['emails'])
        assert new_email == json.loads(json.loads(user_logs.content)['body'])['email'][a - 1]['value']

        # Cleanup
        profile_page.delete_secondary_email(new_email)
        profile_page.click_update_emails()

    @pytest.mark.nondestructive
    def test_update_tshirt_size(self, base_url, selenium, ldap, person_api_token, counter_api):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        you_and_mozilla_page = settings_page.you_and_mozilla
        new_tshirt_size = random.choice(you_and_mozilla_page.tshirt_sizes_list)
        you_and_mozilla_page.select_tshirt_size(new_tshirt_size)
        you_and_mozilla_page.click_update_tshirt_size()
        time.sleep(8)
        api = person_api_token['api']
        user_logs = requests.get(api, headers={
            'Authorization': 'Bearer {0}'.format(conftest.person_api_access_token(person_api_token))})
        assert new_tshirt_size == json.loads(json.loads(user_logs.content)['body'])['shirtSize']

    @pytest.mark.nondestructive
    def test_update_groups(self, base_url, selenium, ldap, token, counter_api):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'], conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        groups = settings_page.groups
        groups_page = groups.click_find_group_link()
        new_group_name = 'group-{0}'.format(str(uuid.uuid4())[:10])
        groups_page.create_group(new_group_name, "Reviewed", "Access Group")
        time.sleep(8)
        api = token['api']
        user_logs = requests.get(api, headers={'Authorization': 'Bearer {0}'.format(conftest.access_token(token))})
        assert '{0}{1}'.format('mozilliansorg_', new_group_name) in json.loads(user_logs.content)['app_metadata']['groups']

        # Cleanup
        groups_page.check_delete_aknowledgement()
        groups_page.click_delete_group()
