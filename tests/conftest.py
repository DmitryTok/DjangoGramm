# import pytest
# from os import environ as env
# from django.conf import settings
# from django.core.management import call_command
# from django.db import connections
#
#
# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['test'] = {
#         'ENGINE': env.get('TEST_DB_ENGINE'),
#         'NAME': env.get('TEST_DB_NAME'),
#         'USER': env.get('TEST_DB_USER'),
#         'PASSWORD': env.get('TEST_DB_PASSWORD'),
#         'HOST': env.get('TEST_DB_HOST'),
#         'PORT': env.get('TEST_DB_PORT'),
#     }
#     call_command('create_test_db', verbosity=0, interactive=False)
#     call_command('migrate', verbosity=0, interactive=False)
#     yield
#     connections['default'].cursor().execute(f'DROP DATABASE {env.get("TEST_DB_NAME")};')
