import unittest
from main import *

class TestBankMethods(unittest.TestCase):
    def test_check_email(self):
        self.assertEqual(check_email("GWashington@bank.com"), 0)

    def test_check_balance(self):
        self.assertEqual(check_balance("GWashington@bank.com"), 1000)

    def test_update_name(self):
        update_name("GWashington@bank.com", "George W")
        self.assertEqual(check_name("GWashington@bank.com"), "George W")

    def test_update_password(self):
        update_password("GWashington@bank.com", "USA12345!")
        self.assertEqual(check_password("GWashington@bank.com"), "USA12345!")

    def test_create_account(self):
        create_account("AHamilton@bank.com", "Alexander Hamilton", "Banking1!")
        self.assertEqual(check_email("AHamilton@bank.com"), 0)

    def test_delete_account(self):
        delete_account("AHamilton@bank.com")
        self.assertEqual(check_email("AHamilton@bank.com"), -1)

    def test_deposit(self):
        init_bal = check_balance("GWashington@bank.com")
        deposit("GWashington@bank.com", 100)
        self.assertEqual(check_balance("GWashington@bank.com"), init_bal+100)

    def test_withdraw(self):
        init_bal = check_balance("GWashington@bank.com")
        withdraw("GWashington@bank.com", 100)
        self.assertEqual(check_balance("GWashington@bank.com"), init_bal-100)

    def test_wire(self):
        init_bal_sender = check_balance("GWashington@bank.com")
        init_bal_receiver = check_balance("BFranklin@bank.com")
        wire("GWashington@bank.com", "BFranklin@bank.com", 100)
        self.assertEqual(check_balance("GWashington@bank.com"), init_bal_sender-100)
        self.assertEqual(check_balance("BFranklin@bank.com"), init_bal_receiver+100)
        wire("BFranklin@bank.com", "GWashington@bank.com", 100)

if __name__ == '__main__':
    unittest.main()