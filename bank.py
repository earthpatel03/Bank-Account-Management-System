import mysql.connector
from datetime import datetime, date

# 🔗 DB CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",  
    database="bank_db"
)
cursor = conn.cursor()

DAILY_LIMIT = 50000
INTEREST_RATE = 0.05  # 5%

# ================= FUNCTIONS ================= #

# 1. Create Account
def create_account():
    name = input("Enter Name: ")
    balance = float(input("Enter Initial Balance: "))

    cursor.execute(
        "INSERT INTO accounts (name, balance, last_interest_date) VALUES (%s,%s,%s)",
        (name, balance, date.today())
    )
    conn.commit()

    print("✅ Account Created | Acc No:", cursor.lastrowid)


# 2. Deposit
def deposit():
    acc_no = int(input("Enter Account No: "))
    amount = float(input("Enter Amount: "))

    if amount <= 0:
        print("❌ Invalid amount")
        return

    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE acc_no=%s", (amount, acc_no))
    cursor.execute(
        "INSERT INTO transactions (acc_no, type, amount, txn_time) VALUES (%s,%s,%s,%s)",
        (acc_no, "Deposit", amount, datetime.now())
    )
    conn.commit()

    print("✅ Deposited")


# 3. Withdraw (WITH DAILY LIMIT)
def withdraw():
    acc_no = int(input("Enter Account No: "))
    amount = float(input("Enter Amount: "))

    if amount <= 0:
        print("❌ Invalid amount")
        return

    cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s", (acc_no,))
    result = cursor.fetchone()

    if not result:
        print("❌ Account not found")
        return

    balance = float(result[0])

    from datetime import date
    today = date.today()

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0) FROM transactions
        WHERE acc_no=%s AND type='Withdraw' AND DATE(txn_time)=%s
    """, (acc_no, today))

    today_withdraw = float(cursor.fetchone()[0])

    if today_withdraw + amount > DAILY_LIMIT:
        print(f"❌ Daily limit exceeded! Limit = {DAILY_LIMIT}")
        return

    if amount > balance:
        print("❌ Insufficient balance")
        return

    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE acc_no=%s", (amount, acc_no))
    cursor.execute(
        "INSERT INTO transactions (acc_no, type, amount, txn_time) VALUES (%s,%s,%s,%s)",
        (acc_no, "Withdraw", amount, datetime.now())
    )
    conn.commit()

    print("✅ Withdrawal successful")


# 4. Check Balance
def check_balance():
    acc_no = int(input("Enter Account No: "))

    cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s", (acc_no,))
    result = cursor.fetchone()

    if result:
        print("💰 Balance:", result[0])
    else:
        print("❌ Account not found")


# 5. Transaction History
def transaction_history():
    acc_no = int(input("Enter Account No: "))

    cursor.execute("SELECT * FROM transactions WHERE acc_no=%s", (acc_no,))
    for row in cursor.fetchall():
        print(row)


# 6. Apply Interest
def apply_interest():
    acc_no = int(input("Enter Account No: "))

    cursor.execute("SELECT balance, last_interest_date FROM accounts WHERE acc_no=%s", (acc_no,))
    result = cursor.fetchone()

    if not result:
        print("❌ Account not found")
        return

    balance, last_date = result

    if last_date == date.today():
        print("⚠️ Interest already applied today")
        return

    interest = balance * INTEREST_RATE
    new_balance = balance + interest

    cursor.execute("""
        UPDATE accounts 
        SET balance=%s, last_interest_date=%s 
        WHERE acc_no=%s
    """, (new_balance, date.today(), acc_no))

    cursor.execute(
        "INSERT INTO transactions (acc_no, type, amount, txn_time) VALUES (%s,%s,%s,%s)",
        (acc_no, "Interest", interest, datetime.now())
    )

    conn.commit()

    print(f"✅ Interest Added: {interest}")


# 7. View Accounts
def view_accounts():
    cursor.execute("SELECT * FROM accounts")
    for row in cursor.fetchall():
        print(row)


# 8. Delete Account
def delete_account():
    acc_no = int(input("Enter Account No: "))

    cursor.execute("DELETE FROM transactions WHERE acc_no=%s", (acc_no,))
    cursor.execute("DELETE FROM accounts WHERE acc_no=%s", (acc_no,))
    conn.commit()

    print("🗑️ Account Deleted")


# ================= MENU ================= #

while True:
    print("\n====== ADVANCED BANK SYSTEM ======")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw (Daily Limit)")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Apply Interest")
    print("7. View Accounts")
    print("8. Delete Account")
    print("9. Exit")

    choice = input("Enter choice: ").strip()

    if choice == '1':
        create_account()
    elif choice == '2':
        deposit()
    elif choice == '3':
        withdraw()
    elif choice == '4':
        check_balance()
    elif choice == '5':
        transaction_history()
    elif choice == '6':
        apply_interest()
    elif choice == '7':
        view_accounts()
    elif choice == '8':
        delete_account()
    elif choice == '9':
        print("👋 Exiting...")
        break
    else:
        print("❌ Invalid choice")