from ATM import ATM
from bank import Bank
'''
J. Salfity, October 2020
Bank APIs implemented with fake bank data

This file simulates an ATM UI and calls the ATM API
'''
if __name__ == "__main__":

    # create bank
    bofa = Bank()

    # create atm and connect to bank
    atm = ATM()
    atm.connect_bank(bofa)

    session_restart = False

    while(atm.power):

        # user canceled something, opt to end session
        if session_restart:
            print("End Session (1/0)?")
            end = int(input())
            if end:
                atm.end_session()
                print("SESSION ENDED")
            session_restart = False

        # a new session
        # insert card
        elif atm.active_cardnumber is None:
            print('Insert card number. 0 to cancel:')
            cardnumber = int(input())
            atm.insert_cardnumber(cardnumber)
            if cardnumber == 0:
                session_restart = True
                continue
            
        # input pin
        elif atm.active_cardnumber is not None and not atm.valid_pin:
            print('Insert pin number. 0 to cancel:')
            pin = int(input())
            if pin == 0:
                session_restart = True
                continue

            # authenticate pin
            atm.authenticate_cardnumber_and_pin(pin)
            if not atm.valid_pin:
                print('INVALID CARD/PIN')

        # card and pin are valid
        # get accounts, get requests/amount, process 
        elif atm.active_cardnumber and atm.valid_pin:
            print("WELCOME!")

            account, accounts, request, amount, confirm = None, None, None, None, False

            # get account
            accounts = atm.get_accounts()
            print('Select Account. 0 to cancel:')
            for acc in accounts:
                print(" {} balance at ${}".format(acc, atm.active_accounts[acc])) 
            account = input()
            if account == '0':
                print("CANCELED")
                session_restart = True
                continue
            elif account not in accounts:
                print("INVALID ACCOUNT")
                session_restart = True
                continue
            
            # get request
            print("Select Request. 0 to cancel: ")
            for r in atm.supported_requests:
                print(" "+r)         
            request = input()
            if request == '0':
                print("CANCELED")
                session_restart = True
                continue
            elif request not in atm.supported_requests:
                print("INVALID REQUEST")
                session_restart = True
                continue

            # get amount
            if request == 'withdraw' or request == 'deposit':
                print("Amount to {}: ".format(request))
                amount = int(input())
                if amount < 0:
                    print('INVALID AMOUNT')
                    session_restart = True
                    continue
            
            # confirm transaction
            print("Confirm (1/0): {}, {}, ${}".format(account, request, amount))
            confirm = int(input())
            if confirm:
                # process transaction
                transaction = atm.process_transaction(account=account, request=request, amount=amount)

                # notify user
                print("TRANSACTION PROCESSED")
                if request == 'withdraw' or request == 'deposit':
                    print(" Start {} balance: ${}".format(account, transaction['start_balance']))
                    print(" ${} {}".format(amount, request))
                print(" Current {} balance: ${}".format(account, transaction['end_balance']))

                session_restart = True