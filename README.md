# ATM API

This project contains an ATM API and a mock Bank class written in Python 3.7. Additionally, an example UI is provided.

For simplicity:

- No encryption between ATM-Bank, including upon initilization or transactions.
- Cash bin is not implemented, assume ATM user enters proper amount.
- ATM has one Bank.
- Bank has synthetic data and functions to mimic ATM-Bank communication.
- ATM only supports requests `show_balance`, `withdraw`, and `deposit`.
- `Request`, `Account`, `Amount` are bundled into a `transaction`, to mimic a banking system
- Transactions are stored by the ATM
- Transactions are confirmed by UI

## Install
clone this project

## Requirements
Python 3.7

## Quick Start
### Using ATM API
An ATM object uses three member variables to control the flow of transactions: `active_cardnumber`, `active_accounts`, `valid_pin`. 

These variables are constantly checked when functions are called. For example, a user cannot `get_accounts()` without `valid_pin` as `True`, a user cannot `process_transaction` without `active_accounts` as empty, etc.

Variable values when they are intialized and when a session is restarted:
```
self.active_cardnumber = None
self.active_accounts = {}
self.valid_pin = False
```

### Simple Example
```
from bank import Bank
from ATM import ATM

VALID_CARDNUMBER = 100100
VALID_PIN = 2020

# Initialize an ATM
atm = ATM()

# Initialize and connect a Bank()
bank = Bank()
atm.connect_bank(bank)

# Input cardnumber and pin
atm.insert_cardnumber(VALID_CARDNUMBER)
atm.authenticate_cardnumber_and_pin(VALID_PIN)

# Get accounts
accounts = atm.get_accounts()

# Get account
account = "checkings"

# Get request from user
request = "withdraw"

# Get amount from user
amount = 100

# process transaction
transaction = atm.process_transaction(account, request, amount)

# transaction is a dictionary containing all relevant information
transaction
>>> {'account': 'checkings', 'start_balance': 450, 'request': 'withdraw', 'amount': 100, 'cardnumber': 100100, 'time': 1603301614.473296, 'end_balance': 350}

# end session, resetting all session variables
atm.end_session()
```

### UI Simulation
For full UI simulation, see [UI_example.py](./bear_atm/UI_example.py)

## Testing
Unit tests for API functions are in ATM_test.py