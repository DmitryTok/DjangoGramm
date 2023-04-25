import pytest
from django.core.management import call_command
from django.test import TransactionTestCase
from pytest_django.plugin import _blocking_manager


@pytest.fixture(scope='session')
def django_db_setup(django_db):
    call_command('migrate', database='test')


@pytest.fixture(scope='function')
def clear_db(request):
    def finalizer():
        with _blocking_manager.unblock_all():
            TransactionTestCase().reset_sequences()
    request.addfinalizer(finalizer)
