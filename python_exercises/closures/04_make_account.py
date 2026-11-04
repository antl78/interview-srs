META = {
    "title": "Bank account closures",
    "function": "make_account",
    "prompt": (
        "Renvoie un tuple `(deposit, withdraw)` de deux fonctions qui "
        "partagent le même solde, initialisé à `balance`. Chacune prend un "
        "montant et renvoie le nouveau solde. `withdraw` lève une "
        "`ValueError` si le solde est insuffisant, sans le modifier."
    ),
    "hints": [
        "Les deux fonctions doivent capturer la même variable.",
        "`nonlocal balance` dans chacune des deux.",
        "Vérifie le solde avant de le modifier.",
    ],
}


def make_account(balance: int) -> tuple:
    """Reference solution."""

    def deposit(amount: int) -> int:
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount: int) -> int:
        nonlocal balance
        if amount > balance:
            raise ValueError("insufficient funds")
        balance -= amount
        return balance

    return deposit, withdraw


def deposit_50_withdraw_30(account, *args):
    deposit, withdraw = account
    return [deposit(50), withdraw(30)]


def withdraw_everything(account, balance):
    deposit, withdraw = account
    return withdraw(balance)


def withdraw_500(account, *args):
    deposit, withdraw = account
    return withdraw(500)


def refused_then_deposit_10(account, *args):
    deposit, withdraw = account
    try:
        withdraw(500)
    except ValueError:
        pass
    return deposit(10)


TEST_CASES = [
    {"args": (100,), "then": deposit_50_withdraw_30, "expected": [150, 120]},
    {"args": (0,), "then": deposit_50_withdraw_30, "expected": [50, 20], "note": "solde partagé entre les deux fonctions"},
    {"args": (100,), "then": withdraw_everything, "expected": 0, "note": "retrait du solde exact"},
    {"args": (100,), "then": withdraw_500, "raises": ValueError, "note": "solde insuffisant"},
    {"args": (100,), "then": refused_then_deposit_10, "expected": 110, "note": "un retrait refusé ne modifie pas le solde"},
]
