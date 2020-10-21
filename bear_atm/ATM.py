'''
J. Salfity, October 2020
ATM API implemented

considerations for this example: 
- No encryption between ATM and Bank, including initilization, transactions, requests
- Transactions do not have uniqueID's 
- ATM has only one Bank / Bank has single ATM
- cash bin is not implemented, assume ATM user enters proper amount
- bank has synthetic data
- transaction are confirmed by UI
'''
from bank import Bank
import time
    
class ATM:
    def __init__(self):     
        # member variables act as state/session variables 
        self.active_cardnumber = None
        self.active_accounts = {}
        self.valid_pin = False

        # ATM supports these requests
        self.supported_requests = ['show_balance', 'withdraw','deposit']

        # link atm to bank, just a single bank for this example
        # real world bank would authenticate the ATM
        self.bank = None

        # atm is powered on
        self.power = True

        # store transaction history
        self.transaction_history = []

    def connect_bank(self, bank):
        '''
        input: (Bank) bank
        routine: link self.bank to bank
        return: -
        '''
        # link atm to bank, just a single bank for this example
        # real world bank would authenticate the ATM / Bank
        self.bank = bank
        return

    def insert_cardnumber(self, cardnumber):
        '''
        input: (int) cardnumber
        routine: sets self.active_cardnumber variables
        return: -
        '''
        self.active_cardnumber = cardnumber
        return

    def authenticate_cardnumber_and_pin(self, pin):
        '''
        input: (int) pin
        routine: inputs/reads pin number,
                checks card/pin number with bank,
                sets ATM member variables
        return: (bool) True/False
        '''
        #bank connecteced, valid card
        self.check_exceptions(  check_bank = True, 
                                check_active_cardnumber = True) 
                        
        # check cardnumber/pin
        self.valid_pin = self.bank.authenticate_cardnumber_pin(self.active_cardnumber, pin)
        return self.valid_pin

    def get_accounts(self):
        '''
        input: -
        routine:  uses self.active_cardnumber
                sets self.active_account_list
        return: (bool) 
        '''
        #bank connected, valid card, valid pin
        self.check_exceptions(  check_bank=True, 
                                check_active_cardnumber=True, 
                                check_valid_pin=True)

        # get accounts from bank
        self.active_accounts = self.bank.get_cardnumber_accounts(self.active_cardnumber)
        return self.active_accounts

    def process_transaction(self, account, request, amount):
        '''
        input: (str) account
                (str) request
                (int) amount
        routine: bundle into transaction and process with bank
        return: (dict) transaction
        '''
        # valid bank, valid card, valid pin
        # active accounts and active acount
        self.check_exceptions(  check_bank=True, 
                                check_active_cardnumber=True, 
                                check_valid_pin=True,
                                check_active_accounts=True,
                                check_account=True, account=account,
                                check_request=True, request=request)

        # create transaction
        transaction = {
            'time': time.time(),
            'cardnumber': self.active_cardnumber, 
            'account': account, 
            'request': request,
            'amount': amount, 
            'start_balance': None, 
            'end_balance': None
        }

        # send to bank, receive updated transaction
        transaction = self.bank.process_transaction(transaction)

        # transaction may have failed or been denied
        if transaction is None:
            raise Exception("Transaction Denied")
        
        # store transaction to atm and bank history
        else:
            self.add_transaction(transaction)
            return transaction
    
    def add_transaction(self, transaction):
        '''
        input: (dict) transaction
        routine: append transaction to transaction_history
        output: -
        '''
        # valid bank, valid card, valid pin
        # active accounts and active acount
        self.check_exceptions(  check_bank=True, 
                                check_active_cardnumber=True, 
                                check_valid_pin=True,
                                check_active_accounts=True)
        
        self.transaction_history.append(transaction)
        return
            
    def end_session(self):
        '''
        input: (bool) 
        routine: resets atm member variables
        return:
        '''
        self.active_cardnumber = None
        self.active_accounts = {}
        self.valid_pin = False
        return

    def check_exceptions(self, 
                        check_bank = False, 
                        check_active_cardnumber = False, 
                        check_valid_pin = False,
                        check_active_accounts = False,
                        check_account=False, account=None,
                        check_request=False, request=None):
        '''
        variables checked when functions are called
        '''
        if check_bank and self.bank is None:
            raise Exception("No bank linked to ATM")
        if check_active_cardnumber and not self.active_cardnumber:
            raise Exception("No card in ATM")
        if check_valid_pin and not self.valid_pin:
            raise Exception("Invalid card/pin")
        if check_active_accounts and not self.active_accounts:
            raise Exception("No accounts in this ATM session")
        if check_account and account not in self.active_accounts:
            raise Exception("Invalid Account")
        if check_request and request not in self.supported_requests:
            raise Exception("Invalid Request")

        return