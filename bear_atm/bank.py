'''
J. Salfity, October 2020
Bank APIs implemented with fake bank data

considerations for this example: 
- No encryption between ATM and Bank, including initilization, transactions, requests
- Transactions do not have uniqueID's 
- ATM has only one Bank / Bank has single ATM
- bank has synthetic data
'''

fake_bank_data = {
        100100 : { 
            "PIN" : 2020,
            "ACCOUNTS": {
                "checkings": 450,
                "savings": 4500,
                "401k": 20000
            }
         },
        200200 : { 
            "PIN" : 2000,
            "ACCOUNTS": {
                "college": 45000,
                "IRA": 10000
                }
         },
         619619 : {
             "PIN": 2011,
             "ACCOUNTS": {
                 "groceries": 1000,
                 "toys": 1000
             }
         }
    }

class Bank():
    def __init__(self):
        pass
        # history of transaction unnecessary for this example
        # self.transaction_history = []
    
    def authenticate_cardnumber_pin(self, cardnumber, pin):
        if cardnumber not in fake_bank_data:
            return False

        return fake_bank_data[cardnumber]["PIN"] == pin
    
    def get_cardnumber_accounts(self, cardnumber):
        if cardnumber not in fake_bank_data:
            return None
        else:
            return fake_bank_data[cardnumber]["ACCOUNTS"]

    def process_transaction(self, transaction):
        cardnumber = transaction["cardnumber"]
        account = transaction["account"]
        request = transaction["request"]
        amount = transaction["amount"]

        #populate transaction start_balance
        transaction["start_balance"] = fake_bank_data[cardnumber]["ACCOUNTS"][account]

        # simple check for error
        if amount is not None and amount < 0:
            return None

        # show_balance
        if request == 'show_balance':
            pass
        # withdraw
        elif request == 'withdraw':
            # overdrawn
            if fake_bank_data[cardnumber]["ACCOUNTS"][account] < amount:
                return None
            else:
                fake_bank_data[cardnumber]["ACCOUNTS"][account] -= amount
        # deposit    
        elif request == 'deposit':
            fake_bank_data[cardnumber]["ACCOUNTS"][account] += amount            
        
        #populate transaction end_balance
        transaction["end_balance"] = fake_bank_data[cardnumber]["ACCOUNTS"][account]

        return transaction