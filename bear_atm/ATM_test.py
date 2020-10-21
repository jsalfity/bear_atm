from bank import Bank
from ATM import ATM

# https://docs.python.org/3/library/unittest.html
import unittest

VALID_CARDNUMBER = 100100
VALID_PIN = 2020

INVALID_CARDNUMBER = 100111
INVALID_PIN = 2000

VALID_ACCOUNTS = ["checkings", "savings", "401k"]
INVALID_ACCOUNTS = ["fun","parties", "boat"]

VALID_REQUESTS = ["show_balance", "withdraw", "deposit"]
INVALID_REQUESTS = ["request_test1", "request_test2"]

class test_ATM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up ATM Test")
        # opt to set up atm , card/pin in each test for this example

    def test_connect_bank(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        self.assertEquals(atm.bank, None)

        atm.connect_bank(bank)
        self.assertEquals(atm.bank, bank)
    
    def test_insert_cardnumber(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)
        atm.insert_cardnumber(VALID_CARDNUMBER)
        self.assertEquals(atm.active_cardnumber, VALID_CARDNUMBER)
    
    def test_authenticate_cardnumber_and_pin_no_bank(self):
        # start atm
        atm = ATM()
        try:
            atm.authenticate_cardnumber_and_pin(VALID_PIN)
        except Exception as exp: 
                self.assertEqual(exp.args[0], "No bank linked to ATM")

    def test_authenticate_cardnumber_and_pin_no_card(self):
         #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)

        try:
            atm.authenticate_cardnumber_and_pin(VALID_PIN)
        except Exception as exp: 
                self.assertEqual(exp.args[0], "No card in ATM")
    
    def test_authenticate_cardnumber_and_pin(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)
        atm.insert_cardnumber(VALID_CARDNUMBER)
        atm.authenticate_cardnumber_and_pin(VALID_PIN)
        
        self.assertEqual(atm.valid_pin, True)

        atm.authenticate_cardnumber_and_pin(INVALID_PIN)
        self.assertEquals(atm.valid_pin, False)
    
    def test_get_accounts_invalid_card_and_pin(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)

        # no card inserted
        try:
            atm.get_accounts()
        except Exception as exp: 
                self.assertEqual(exp.args[0], "No card in ATM")

        # insert cardnumber
        atm.insert_cardnumber(VALID_CARDNUMBER)
        
        # insert_pin
        atm.authenticate_cardnumber_and_pin(INVALID_PIN)
        try:
            atm.get_accounts()
        except Exception as exp: 
                self.assertEqual(exp.args[0], "Invalid card/pin")
    
        # active_accounts should be empty
        self.assertEqual(atm.active_accounts, {})

    def test_get_accounts(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)
        # insert cardnumber
        atm.insert_cardnumber(VALID_CARDNUMBER)
        # insert_pin
        atm.authenticate_cardnumber_and_pin(VALID_PIN)

        # get accounts
        atm.get_accounts()
        self.assertEqual(atm.active_accounts, bank.get_cardnumber_accounts(VALID_CARDNUMBER))

    def test_process_invalid_transaction(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)
        # insert cardnumber
        atm.insert_cardnumber(VALID_CARDNUMBER)
        # insert_pin
        atm.authenticate_cardnumber_and_pin(VALID_PIN)

        # get accounts
        atm.get_accounts()

        for acc in INVALID_ACCOUNTS:
            try:
                atm.process_transaction(acc, VALID_REQUESTS[0], 0)
            except Exception as exp: 
                self.assertEqual(exp.args[0], "Invalid Account")

        for req in INVALID_REQUESTS:
            try:
                atm.process_transaction(VALID_ACCOUNTS[0], req, 0)
            except Exception as exp: 
                self.assertEqual(exp.args[0], "Invalid Request")
        
        amount = -50
        try:
            transaction = atm.process_transaction(VALID_ACCOUNTS[1], 'withdraw', amount)
        except Exception as exp: 
            self.assertEqual(exp.args[0], "Transaction Denied")
        
        try:
            transaction = atm.process_transaction(VALID_ACCOUNTS[1], 'deposit', amount)
        except Exception as exp: 
            self.assertEqual(exp.args[0], "Transaction Denied")
    
    def test_process_valid_transaction(self):
        #start atm
        atm = ATM()
        # connect bank
        bank = Bank()
        atm.connect_bank(bank)
        # insert cardnumber
        atm.insert_cardnumber(VALID_CARDNUMBER)
        # insert_pin
        atm.authenticate_cardnumber_and_pin(VALID_PIN)

        # get accounts
        atm.get_accounts()

        # show balance
        transaction = atm.process_transaction(VALID_ACCOUNTS[0], 'show_balance',0)
        self.assertEqual(transaction['start_balance'], transaction['end_balance'])
        self.assertEqual(atm.transaction_history[-1], transaction)

        amount = 50
        # withdraw
        transaction = atm.process_transaction(VALID_ACCOUNTS[0], 'withdraw', amount)
        self.assertEquals(transaction['end_balance']+amount, transaction['start_balance'])
        self.assertEqual(atm.transaction_history[-1], transaction)

        # deposit        
        transaction = atm.process_transaction(VALID_ACCOUNTS[0], 'deposit', amount)
        self.assertEquals(transaction['end_balance']-amount, transaction['start_balance'])
        self.assertEqual(atm.transaction_history[-1], transaction)
        
    @classmethod
    def tearDownClass(cls):
        print("")  # for weird period output that I can't find atm
        print("Tearing down ATM Test")


if __name__ == '__main__':
    unittest.main()