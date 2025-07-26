Wallet Risk Scoring From Scratch

This project assigns a risk score (0–1000) to a list of Ethereum wallet addresses based on their on-chain activity related to the Compound protocol.

How It Works:

1. Fetch transaction data from the Covalent API for each wallet.
2. Extract relevant features:
   a. Total number of transactions
   b. Total gas used
   c. Number of interactions with Compound protocol
3. Normalize features and compute a weighted risk score.
4. Output is a CSV file: `wallet_scores.csv`

Files:

`ZERU_2.py`: Main script to fetch data, process features, and calculate risk scores.
`wallet_scores.csv`: Final output containing wallet_id and risk score.
`analysis.md`: Documentation of feature selection, scoring logic, and reasoning.

Requirements:

Python 3.8+
Covalent API key
`wallet_list.csv` with a column `wallet_id`

Install Dependencies:

bash
pip install requests pandas tqdm


Usage:

bash
python Zeru2.py
Make sure your `wallet_list.csv` is in the same directory.

Risk Scoring Formula:

python
score = int(1000 * (
    0.5 * normalized(compound_interactions) +
    0.3 * normalized(tx_count) +
    0.2 * normalized(total_gas)
))

License:

MIT
