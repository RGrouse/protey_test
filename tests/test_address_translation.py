import requests
import unittest
import json
from urllib.parse import urljoin

BASE_URL = "http://nominatim.openstreetmap.org"

# Data-file keywords
PARAMETERS_FOR_REQUEST = 'request_parameters'
EXPECTED_RESULT = 'expected_result'
TEST_ID = 'test_id'
MATCH_EXACTLY = 'match_exactly'
TEST_PARAMETERS = 'test_parameters'
FORMAT = 'format'
REQUEST_PATH = 'request_path'


# Фабрика для создания кейсов с данными
def make_test_case(setup):
    class TestAddressTranslation(unittest.TestCase):
        def test_address_translation_json(self):
            # Установим параметр для запроса, чтобы данные возвращались в json формате
            setup[PARAMETERS_FOR_REQUEST][FORMAT] = 'json'

            url = urljoin(BASE_URL, setup[TEST_PARAMETERS][REQUEST_PATH])
            response = requests.get(url, setup[PARAMETERS_FOR_REQUEST])

            real_result = response.json()
            expected_result = setup[EXPECTED_RESULT]

            self.assertEqual(real_result, expected_result, msg="TestID: {}".format(setup[TEST_ID]))

        def test_address_translation_xml(self):
            # todo implement this
            pass

        def test_address_translation_html(self):
            # todo implement this
            pass
    return TestAddressTranslation


def get_test_data_suite(filepath):
    suite = unittest.TestSuite()

    with open(filepath, 'r') as json_data_file:
        cases_params = json.load(json_data_file)

        for case_param in cases_params:
            case = make_test_case(case_param)
            suite.addTest(case('test_address_translation_json'))

    return suite


if __name__ == '__main__':
    testRunner = unittest.TextTestRunner()
    testRunner.run(get_test_data_suite('direct.json'))
    testRunner.run(get_test_data_suite('reverse.json'))
