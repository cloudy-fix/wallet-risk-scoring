import requests
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
API_KEY = 'cqt_rQgRYvTgHHCrMDh8Kct8f6HKDp3p'  
CHAIN_ID = 1 
WALLET_CSV = 'wallet_list.csv'  


def load_wallets(csv_file):
    df = pd.read_csv(csv_file)
    if 'wallet_id' not in df.columns:
        raise ValueError("CSV must have a column named 'wallet_id'")
    return df['wallet_id'].tolist()


def fetch_transactions(wallet_address):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet_address}/transactions_v2/"
    params = {'key': API_KEY}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('data', {}).get('items', [])
        else:
            print(f"[!] Error for {wallet_address} – HTTP {response.status_code}")
    except requests.exceptions.RequestException:
        print(f"[!] Timeout or network error for {wallet_address}")
    return []


def create_features(wallet_data):
    features = []
    for entry in wallet_data:
        wallet = entry['wallet_id']
        txs = entry['txs']
        tx_count = len(txs)
        total_gas = sum(tx.get('gas_spent', 0) for tx in txs)
        compound_interactions = sum(
            1 for tx in txs
            if 'compound' in ((tx.get('to_address_label') or '') + (tx.get('from_address_label') or '')).lower()
        )
        features.append({
            'wallet_id': wallet,
            'tx_count': tx_count,
            'total_gas': total_gas,
            'compound_interactions': compound_interactions
        })
    return pd.DataFrame(features)


def normalize(df, col):
    return (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-6)

def score_row(row):
    return int(1000 * (
        0.5 * row['compound_interactions'] +
        0.3 * row['tx_count'] +
        0.2 * row['total_gas']
    ))

def calculate_scores(df):
    df['tx_count'] = normalize(df, 'tx_count')
    df['total_gas'] = normalize(df, 'total_gas')
    df['compound_interactions'] = normalize(df, 'compound_interactions')
    df['score'] = df.apply(score_row, axis=1)
    return df[['wallet_id', 'score']]


if __name__ == "__main__":
    print("Loading wallet addresses...")
    wallet_list = load_wallets(WALLET_CSV)

    all_wallet_data = []
    print("Fetching transactions from Covalent API...")
    for wallet in tqdm(wallet_list):
        txs = fetch_transactions(wallet)
        all_wallet_data.append({'wallet_id': wallet, 'txs': txs})
        time.sleep(1)  # prevent rate limiting

    print("Extracting features...")
    df_features = create_features(all_wallet_data)

    print("Scoring wallets...")
    df_scores = calculate_scores(df_features)

    print("Saving to wallet_scores.csv")
    df_scores.to_csv("wallet_scores.csv", index=False)
    print("Done! Submission file 'wallet_scores.csv' is ready.")
