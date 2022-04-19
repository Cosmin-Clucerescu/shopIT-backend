from rest_api.utils.custom_exception_handlers import custom_exception_handler


def test_custom_exception_handler():
    assert custom_exception_handler(Exception(), None) is None
