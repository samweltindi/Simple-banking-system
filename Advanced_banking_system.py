from datetime import datetime
from decimal import Decimal, InvalidOperation


class Account:
    def __init__(self, account_id: str, owner: str, pin: str, balance: Decimal = Decimal("0.00")):
        self.account_id = account_id
        self.owner = owner
        self._pin = pin  # In a real app, store a salted hash (e.g., bcrypt/argon2), never plain text
        self.balance = balance
        self.transactions: list[str] = []

    def _record(self, entry: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"[{stamp}] {entry} | Balance: {self.balance:.2f}")

    def deposit(self, amount: Decimal) -> tuple[bool, str]:
        if amount <= Decimal("0.00"):
            return False, "Deposit amount must be greater than 0."
        self.balance += amount
        self._record(f"DEPOSIT +{amount:.2f}")
        return True, f"Deposited {amount:.2f}."

    def withdraw(self, amount: Decimal) -> tuple[bool, str]:
        if amount <= Decimal("0.00"):
            return False, "Withdrawal amount must be greater than 0."
        if amount > self.balance:
            return False, "Insufficient funds."
        self.balance -= amount
        self._record(f"WITHDRAW -{amount:.2f}")
        return True, f"Withdrew {amount:.2f}."


def parse_amount(raw: str) -> Decimal | None:
    try:
        val = Decimal(raw.strip())
        return val.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None


def main() -> None:
    accounts = {
        "1001": Account("1001", "Amina", "1234", Decimal("500.00")),
        "1002": Account("1002", "Brian", "5678", Decimal("250.00")),
    }

    acc_id = input("Enter account ID (1001 or 1002): ").strip()
    pin = input("Enter PIN: ").strip()
    account = accounts.get(acc_id)

    if not account or account._pin != pin:
        print("Invalid account ID or PIN.")
        return

    while True:
        print(f"\n--- Welcome, {account.owner} ({account.account_id}) ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Balance")
        print("4. Transaction History")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            amt = parse_amount(input("Amount to deposit: "))
            if amt is None:
                print("Invalid number.")
            else:
                ok, msg = account.deposit(amt)
                print(msg)

        elif choice == "2":
            amt = parse_amount(input("Amount to withdraw: "))
            if amt is None:
                print("Invalid number.")
            else:
                ok, msg = account.withdraw(amt)
                print(msg)

        elif choice == "3":
            print(f"Current balance: {account.balance:.2f}")

        elif choice == "4":
            if not account.transactions:
                print("No transactions yet.")
            else:
                for line in account.transactions:
                    print(line)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()