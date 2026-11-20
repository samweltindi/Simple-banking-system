from datetime import datetime
from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import messagebox, scrolledtext


class Account:
    def __init__(self, owner: str, balance: Decimal = Decimal("0.00")):
        self.owner = owner
        self.balance = balance
        self.transactions: list[str] = []

    def _record(self, entry: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"[{stamp}] {entry} | Balance: {self.balance:.2f}")

    def deposit(self, amount: Decimal) -> tuple[bool, str]:
        if amount <= Decimal("0.00"):
            return False, "Enter a positive amount."
        self.balance += amount
        self._record(f"DEPOSIT +{amount:.2f}")
        return True, f"Deposited {amount:.2f}"

    def withdraw(self, amount: Decimal) -> tuple[bool, str]:
        if amount <= Decimal("0.00"):
            return False, "Enter a positive amount."
        if amount > self.balance:
            return False, "Insufficient funds."
        self.balance -= amount
        self._record(f"WITHDRAW -{amount:.2f}")
        return True, f"Withdrew {amount:.2f}"


def parse_amount(raw: str) -> Decimal | None:
    try:
        val = Decimal(raw.strip())
        return val.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None


class BankingApp:
    def __init__(self, root: tk.Tk, account: Account):
        self.root = root
        self.account = account
        self.root.title(f"Banking App - {account.owner}")
        self.root.geometry("460x420")
        self.root.resizable(False, False)

        tk.Label(root, text=f"Welcome, {account.owner}", font=("Arial", 16, "bold")).pack(pady=(16, 4))

        self.balance_var = tk.StringVar(value=f"Balance: {account.balance:.2f}")
        tk.Label(root, textvariable=self.balance_var, font=("Arial", 13)).pack(pady=(0, 14))

        tk.Label(root, text="Amount:", font=("Arial", 11)).pack()
        self.amount_entry = tk.Entry(root, font=("Arial", 12), justify="center", width=22)
        self.amount_entry.pack(pady=6)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Deposit", width=12, command=self.handle_deposit).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Withdraw", width=12, command=self.handle_withdraw).grid(row=0, column=1, padx=6)

        tk.Label(root, text="Transaction History:", font=("Arial", 11, "bold")).pack(pady=(12, 4))
        self.history_box = scrolledtext.ScrolledText(root, width=52, height=10, state="disabled", font=("Consolas", 9))
        self.history_box.pack(padx=12)

    def _refresh_ui(self) -> None:
        self.balance_var.set(f"Balance: {self.account.balance:.2f}")
        self.amount_entry.delete(0, tk.END)
        self.history_box.config(state="normal")
        self.history_box.delete("1.0", tk.END)
        self.history_box.insert(tk.END, "\n".join(self.account.transactions))
        self.history_box.config(state="disabled")

    def handle_deposit(self) -> None:
        amt = parse_amount(self.amount_entry.get())
        if amt is None:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return
        ok, msg = self.account.deposit(amt)
        if not ok:
            messagebox.showwarning("Deposit Failed", msg)
            return
        self._refresh_ui()
        messagebox.showinfo("Success", msg)

    def handle_withdraw(self) -> None:
        amt = parse_amount(self.amount_entry.get())
        if amt is None:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return
        ok, msg = self.account.withdraw(amt)
        if not ok:
            messagebox.showwarning("Withdrawal Failed", msg)
            return
        self._refresh_ui()
        messagebox.showinfo("Success", msg)


if __name__ == "__main__":
    root = tk.Tk()
    demo_account = Account("Amina", Decimal("100.00"))
    BankingApp(root, demo_account)
    root.mainloop()