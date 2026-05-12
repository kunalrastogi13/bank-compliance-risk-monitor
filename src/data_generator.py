import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import DATA_PATH, RANDOM_SEED

fake = Faker()
Faker.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

TRANSACTION_TYPES = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT']
CURRENCIES = ['USD', 'CAD', 'EUR', 'GBP']
MERCHANT_CATEGORIES = [
    'GROCERIES', 'ELECTRONICS', 'RESTAURANTS', 'TRAVEL',
    'HEALTHCARE', 'UTILITIES', 'RETAIL', 'ENTERTAINMENT',
    'FUEL', 'ATM_WITHDRAWAL'
]
HIGH_RISK_COUNTRIES = ['NG', 'IR', 'KP', 'MM', 'SY', 'YE', 'LY', 'SO']
NORMAL_COUNTRIES = ['US', 'CA', 'GB', 'DE', 'FR', 'AU', 'JP', 'SG', 'NL', 'CH']

def generate_customer_pool(n_customers=2000):
    customers = []
    for i in range(n_customers):
        customers.append({
            'customer_id': f'CUST-{i+1:05d}',
            'account_number': f'ACC-{random.randint(10000, 99999)}',
            'customer_age': random.randint(18, 80),
            'account_balance': round(random.uniform(500, 150000), 2),
            'account_type': random.choice(['CHECKING', 'SAVINGS', 'BUSINESS'])
        })
    return customers

def generate_normal_transaction(customer, txn_id, date):
    amount = round(random.uniform(5, 8000), 2)
    return {
        'transaction_id': f'TXN-{txn_id:06d}',
        'customer_id': customer['customer_id'],
        'account_number': customer['account_number'],
        'transaction_date': date,
        'transaction_type': random.choice(TRANSACTION_TYPES),
        'amount': amount,
        'currency': random.choices(CURRENCIES, weights=[60, 25, 10, 5])[0],
        'merchant_category': random.choice(MERCHANT_CATEGORIES),
        'country_code': random.choices(NORMAL_COUNTRIES, weights=[40,20,10,7,7,5,4,3,2,2])[0],
        'customer_age': customer['customer_age'],
        'account_balance': customer['account_balance'],
        'is_fraud': 0,
        'fraud_type': 'NONE'
    }

def generate_structuring_transactions(customer, txn_id, base_date):
    transactions = []
    n_txns = random.randint(3, 7)
    for i in range(n_txns):
        amount = round(random.uniform(8500, 9900), 2)
        date = base_date + timedelta(hours=random.randint(1, 48))
        transactions.append({
            'transaction_id': f'TXN-{txn_id+i:06d}',
            'customer_id': customer['customer_id'],
            'account_number': customer['account_number'],
            'transaction_date': date,
            'transaction_type': 'WITHDRAWAL',
            'amount': amount,
            'currency': 'USD',
            'merchant_category': 'ATM_WITHDRAWAL',
            'country_code': random.choice(NORMAL_COUNTRIES[:3]),
            'customer_age': customer['customer_age'],
            'account_balance': customer['account_balance'],
            'is_fraud': 1,
            'fraud_type': 'STRUCTURING'
        })
    return transactions

def generate_velocity_transactions(customer, txn_id, base_date):
    transactions = []
    n_txns = random.randint(12, 20)
    for i in range(n_txns):
        amount = round(random.uniform(50, 500), 2)
        date = base_date + timedelta(minutes=random.randint(1, 120))
        transactions.append({
            'transaction_id': f'TXN-{txn_id+i:06d}',
            'customer_id': customer['customer_id'],
            'account_number': customer['account_number'],
            'transaction_date': date,
            'transaction_type': random.choice(['PAYMENT', 'WITHDRAWAL']),
            'amount': amount,
            'currency': random.choice(CURRENCIES),
            'merchant_category': random.choice(MERCHANT_CATEGORIES),
            'country_code': random.choice(NORMAL_COUNTRIES),
            'customer_age': customer['customer_age'],
            'account_balance': customer['account_balance'],
            'is_fraud': 1,
            'fraud_type': 'VELOCITY_ABUSE'
        })
    return transactions

def generate_round_number_transaction(customer, txn_id, date):
    amount = float(random.choice([5000, 10000, 15000, 20000, 25000, 50000]))
    return {
        'transaction_id': f'TXN-{txn_id:06d}',
        'customer_id': customer['customer_id'],
        'account_number': customer['account_number'],
        'transaction_date': date,
        'transaction_type': 'TRANSFER',
        'amount': amount,
        'currency': random.choice(CURRENCIES),
        'merchant_category': 'RETAIL',
        'country_code': random.choice(NORMAL_COUNTRIES),
        'customer_age': customer['customer_age'],
        'account_balance': customer['account_balance'],
        'is_fraud': 1,
        'fraud_type': 'ROUND_NUMBER'
    }

def generate_high_risk_country_transaction(customer, txn_id, date):
    amount = round(random.uniform(5000, 50000), 2)
    return {
        'transaction_id': f'TXN-{txn_id:06d}',
        'customer_id': customer['customer_id'],
        'account_number': customer['account_number'],
        'transaction_date': date,
        'transaction_type': 'TRANSFER',
        'amount': amount,
        'currency': random.choice(CURRENCIES),
        'merchant_category': 'RETAIL',
        'country_code': random.choice(HIGH_RISK_COUNTRIES),
        'customer_age': customer['customer_age'],
        'account_balance': customer['account_balance'],
        'is_fraud': 1,
        'fraud_type': 'HIGH_RISK_COUNTRY'
    }

def generate_unusual_hour_transaction(customer, txn_id, base_date):
    hour = random.choice([1, 2, 3, 4])
    date = base_date.replace(hour=hour, minute=random.randint(0, 59))
    amount = round(random.uniform(3000, 30000), 2)
    return {
        'transaction_id': f'TXN-{txn_id:06d}',
        'customer_id': customer['customer_id'],
        'account_number': customer['account_number'],
        'transaction_date': date,
        'transaction_type': random.choice(['WITHDRAWAL', 'TRANSFER']),
        'amount': amount,
        'currency': random.choice(CURRENCIES),
        'merchant_category': 'ATM_WITHDRAWAL',
        'country_code': random.choice(NORMAL_COUNTRIES + HIGH_RISK_COUNTRIES),
        'customer_age': customer['customer_age'],
        'account_balance': customer['account_balance'],
        'is_fraud': 1,
        'fraud_type': 'UNUSUAL_HOURS'
    }

def generate_transactions(n_total=100000):
    print(f"Generating {n_total:,} transactions...")
    customers = generate_customer_pool(2000)
    transactions = []
    txn_id = 1
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range_days = (end_date - start_date).days

    n_fraud_target = int(n_total * 0.05)
    fraud_generated = 0
    fraud_patterns = [
        'structuring', 'velocity', 'round_number',
        'high_risk_country', 'unusual_hours'
    ]

    while len(transactions) < n_total:
        customer = random.choice(customers)
        base_date = start_date + timedelta(days=random.randint(0, date_range_days))

        if fraud_generated < n_fraud_target and random.random() < 0.08:
            pattern = random.choice(fraud_patterns)
            if pattern == 'structuring':
                new_txns = generate_structuring_transactions(customer, txn_id, base_date)
            elif pattern == 'velocity':
                new_txns = generate_velocity_transactions(customer, txn_id, base_date)
            elif pattern == 'round_number':
                new_txns = [generate_round_number_transaction(customer, txn_id, base_date)]
            elif pattern == 'high_risk_country':
                new_txns = [generate_high_risk_country_transaction(customer, txn_id, base_date)]
            else:
                new_txns = [generate_unusual_hour_transaction(customer, txn_id, base_date)]

            transactions.extend(new_txns)
            fraud_generated += len([t for t in new_txns if t['is_fraud'] == 1])
            txn_id += len(new_txns)
        else:
            transactions.append(generate_normal_transaction(customer, txn_id, base_date))
            txn_id += 1

        if len(transactions) % 10000 == 0:
            print(f"  Generated {len(transactions):,} transactions so far...")

    transactions = transactions[:n_total]
    df = pd.DataFrame(transactions)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df = df.sort_values('transaction_date').reset_index(drop=True)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    fraud_count = df['is_fraud'].sum()
    print(f"\nDone! Dataset summary:")
    print(f"  Total transactions : {len(df):,}")
    print(f"  Fraudulent         : {fraud_count:,} ({fraud_count/len(df)*100:.1f}%)")
    print(f"  Normal             : {len(df)-fraud_count:,}")
    print(f"  Fraud types        : {df[df.is_fraud==1].fraud_type.value_counts().to_dict()}")
    print(f"  Saved to           : {DATA_PATH}")
    return df

if __name__ == "__main__":
    df = generate_transactions(100000)
