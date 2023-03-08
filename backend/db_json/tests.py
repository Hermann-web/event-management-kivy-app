import unittest
import json
from clients_handler import (
    get_clients,
    filter_clients_from_text_input, 
    get_client_choices, 
    filter_client_choices_from_text_input, 
    set_present_true
)

class TestFunctions(unittest.TestCase):
    def test_get_clients(self):
        result = get_clients()
        expected = [
            {
                "index": 1,
                "firstname": "John",
                "surname": "Doe",
                "reference": "JD123",
                "firm": "ABC Inc",
                "role": "Manager",
                "cin": "1234567890",
                "email": "john.doe@abc.com"
            },
            {
                "index": 2,
                "firstname": "Jane",
                "surname": "Smith",
                "reference": "JS456",
                "firm": "XYZ Corp",
                "role": "Engineer",
                "cin": "0987654321",
                "email": "jane.smith@xyz.com"
            }
        ]
        self.assertEqual(result, expected)

    def test_filter_clients_from_text_input(self):
        result = filter_clients_from_text_input("ABC")
        expected = [
            {
                "index": 1,
                "firstname": "John",
                "surname": "Doe",
                "reference": "JD123",
                "firm": "ABC Inc",
                "role": "Manager",
                "cin": "1234567890",
                "email": "john.doe@abc.com"
            }
        ]
        self.assertEqual(result, expected)

    def test_get_client_choices(self):
        result = get_client_choices()
        expected = [
            {
                "index": 1,
                "id_client": 1,
                "id_event": 1,
                "is_present": None,
                "time_presence": "10:30 AM"
            },
            {
                "index": 2,
                "id_client": 2,
                "id_event": 1,
                "is_present": None,
                "time_presence": None
            },
            {
                "index": 3,
                "id_client": 1,
                "id_event": 2,
                "is_present": None,
                "time_presence": "3:00 PM"
            },
            {
                "index": 4,
                "id_client": 2,
                "id_event": 2,
                "is_present": True,
                "time_presence": None
            }
        ]
        self.assertEqual(result, expected)


    def test_filter_client_choices(self):
        result = filter_client_choices(id_client=1)
        expected = [
            {
                "index": 1,
                "id_client": 1,
                "id_event": 1,
                "is_present": None,
                "time_presence": "10:30 AM"
            },
            {
                "index": 3,
                "id_client": 1,
                "id_event": 2,
                "is_present": None,
                "time_presence": "3:00 PM"
            }
        ]
        self.assertEqual(result, expected)

    def test_set_present_true(self):
        # Test setting is_present to True for the first time
        index = 2
        result = set_present_true(index)
        expected = {
            "index": 2,
            "id_client": 2,
            "id_event": 1,
            "is_present": True,
            "time_presence": None
        }
        self.assertEqual(result, expected)

        # Test setting is_present to True again (should not change the value)
        index = 2
        result = set_present_true(index)
        expected = {
            "index": 2,
            "id_client": 2,
            "id_event": 1,
            "is_present": True,
            "time_presence": None
        }
        self.assertEqual(result, expected)

        # Test setting is_present to null for the first time
        index = 2
        result = set_present_true(index, force_null_test=True)
        expected = {
            "index": 2,
            "id_client": 2,
            "id_event": 1,
            "is_present": None,
            "time_presence": None
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
