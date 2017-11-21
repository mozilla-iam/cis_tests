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
    def test_update_basic_information(self, base_url, selenium, ldap, counter_api, token):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                    conftest.increase_otp_counter(counter_api)))
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
        api = token['api']
        user_logs = requests.get(api, headers={'Authorization': 'Bearer {0}'.format(conftest.access_token(token))})
        assert new_username == json.loads(user_logs.content)['app_metadata']['userName']
        assert new_first_name == json.loads(user_logs.content)['app_metadata']['firstName']
        assert new_last_name == json.loads(user_logs.content)['app_metadata']['lastName']
        assert new_full_name == json.loads(user_logs.content)['app_metadata']['displayName']

        # Cleanup
        profile_page.set_username(existing_username)
        profile_page.sef_full_name(existing_full_name)
        profile_page.click_update_basic_information()

    @pytest.mark.nondestructive
    def test_update_emails(self, base_url, selenium, ldap, counter_api, token, new_user):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                    conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        profile_page = settings_page.profile
        primary_email = profile_page.primary_email
        new_email = new_user['email']
        profile_page.add_email_identity(new_email)
        profile_page.click_update_emails()
        assert new_email in profile_page.secondary_email_address
        time.sleep(8)
        api = token['api']
        user_logs = requests.get(api, headers={'Authorization': 'Bearer {0}'.format(conftest.access_token(token))})
        assert primary_email == json.loads(user_logs.content)['app_metadata']['emails'][0]['value']
        a = len(json.loads(user_logs.content)['app_metadata']['emails'])
        assert new_email == json.loads(user_logs.content)['app_metadata']['emails'][a - 1]['value']

        # Cleanup
        profile_page.delete_secondary_email(new_email)
        profile_page.click_update_emails()

    @pytest.mark.nondestructive
    def test_update_tshirt_size(self, base_url, selenium, ldap, counter_api, token):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                    conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        you_and_mozilla_page = settings_page.you_and_mozilla
        new_tshirt_size = random.choice(you_and_mozilla_page.tshirt_sizes_list)
        you_and_mozilla_page.select_tshirt_size(new_tshirt_size)
        you_and_mozilla_page.click_update_tshirt_size()
        time.sleep(8)
        api = token['api']
        user_logs = requests.get(api, headers={'Authorization': 'Bearer {0}'.format(conftest.access_token(token))})
        assert new_tshirt_size == json.loads(user_logs.content)['app_metadata']['shirtSize']

    @pytest.mark.nondestructive
    def test_update_groups(self, base_url, selenium, ldap, counter_api, token):
        home_page = Homepage(base_url, selenium)
        two_fa = home_page.login_with_ldap(ldap['email'], ldap['password'])
        two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                conftest.increase_otp_counter(counter_api)))
        while two_fa.is_error_message_displayed:
            two_fa.enter_passcode(conftest.passcode(ldap['secret_seed'],
                                                    conftest.increase_otp_counter(counter_api)))
        settings_page = home_page.header.click_settings_menu_item()
        groups = settings_page.groups
        groups_page = groups.click_find_group_link()
        new_group_name = 'group-{0}'.format(str(uuid.uuid4())[:10])
        groups_page.create_group(new_group_name)
        time.sleep(8)
        api = token['api']
        user_logs = requests.get(api, headers={'Authorization': 'Bearer {0}'.format(conftest.access_token(token))})
        assert '{0}{1}'.format('mozilliansorg_', new_group_name) in json.loads(user_logs.content)['app_metadata']['groups']

        # Cleanup
        groups_page.check_delete_aknowledgement()
        groups_page.click_delete_group()

    @pytest.mark.nondestructive
    def test_upgrade_from_passwordless_to_github(self, base_url, selenium, passwordless_identity, github_identity, token):
        home_page = Homepage(base_url, selenium)
        home_page.login_with_email(passwordless_identity['email'])
        settings_page = home_page.header.click_settings_menu_item()
        contact_identities_number = len(settings_page.profile.contact_identities)
        settings_page.profile.add_github_identity(github_identity['username'], github_identity['password'], conftest.totp_passcode(github_identity['secret_seed']))
        assert settings_page.header.success_alert == "Account successfully verified. You need to use this identity the next time you will login."
        assert len(settings_page.profile.contact_identities) == contact_identities_number + 1
        settings_page.header.logout()
        home_page = Homepage(base_url, selenium)
        home_page.login_with_email(passwordless_identity['email'])
        assert "Please use one of the following authentication methods: Github Provider" in home_page.header.error_alert
        home_page = Homepage(base_url, selenium)
        home_page.login_with_github(github_identity['username'], github_identity['password'])
        home_page.header.logout()
        delete_github_identity_api = token['delete_github_identity_api']

        #Cleanup
        requests.delete(delete_github_identity_api, headers={'Authorization': 'Bearer {0}'.format(conftest.access_token(token))})
