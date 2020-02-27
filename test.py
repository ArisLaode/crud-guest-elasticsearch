import unittest
import json
from crud_guest import app


class TestCrud(unittest.TestCase):

    def setUp(self):
        self.test_crud = app.test_client()

    def test_insert(self):
        url = '/create'

        mock_request_form = {
            'name': 'tes 2',
            'no_hp': '085398122463',
            'address': 'Parigi Baru',
        }

        expected_output ={
            'result': 'created'

        }

        response = self.test_crud.post(url, data=mock_request_form)
        self.assertEqual(response.status_code, 200, msg="Bad response")
        data_response = json.loads(response.get_data().decode('utf-8'))
        self.assertDictEqual(data_response, expected_output,
                             msg="Dictionary not same as expected")

    def test_read(self):
        url = '/read'

        mock_request_form = {
            'name': 'la ode aris',
        }

        expected_output ={
            'name': 'la ode aris',

        }

        response = self.test_crud.get(url, data=mock_request_form)
        self.assertEqual(response.status_code, 200, msg="Bad response")
        data_response = json.loads(response.get_data().decode('utf-8'))
        self.assertDictEqual(data_response, expected_output,
                             msg="Dictionary not same as expected")

    def test_update(self):
        url = '/update'

        mock_request_form = {
            '_id': 'lBIwhnABm2s9qjGl93n8',
            'name': 'la ode aris',
            'no_hp': '085398122499',
            'address': 'Jakarta',
        }

        expected_output ={
            '_id': 'lBIwhnABm2s9qjGl93n8'

        }

        response = self.test_crud.post(url, data=mock_request_form)
        self.assertEqual(response.status_code, 200, msg="Bad response")
        data_response = json.loads(response.get_data().decode('utf-8'))
        self.assertDictEqual(data_response, expected_output,
                             msg="Dictionary not same as expected")

    def test_delete(self):
        url = '/delete'

        mock_request_form = {
            'name': 'la ode aris saputra'
        }

        expected_output ={
            "delete": 1
        }

        response = self.test_crud.post(url, data=mock_request_form)
        self.assertEqual(response.status_code, 200, msg="Bad response")
        data_response = json.loads(response.get_data().decode('utf-8'))
        self.assertDictEqual(data_response, expected_output,
                             msg="Dictionary not same as expected")

if __name__ == "__main__":
    unittest.main()
