Analysis Report – Wallet Risk Scoring From Scratch


Objective

a. To evaluate the behavior of Ethereum wallets using their public blockchain transaction history.
b. To rank each wallet by potential risk based on:
    1.Interaction with lending protocols
    2.Transaction activity
    3.Gas usage patterns


Data Collection

1.API Used: Covalent API (GoldRush platform)
2.Endpoint: /v1/1/address/{wallet}/transactions_v2/
3.Network: Ethereum Mainnet
For each wallet:
 a. Full transaction history was retrieved.
 b. Data included transaction count, gas usage, and labeled addresses.


Feature Selection

The following features were extracted from the transaction data:
 1.tx_count: Total number of transactions made by the wallet.
 2.total_gas: Total gas spent across all transactions.
 3.compound_interactions: Number of transactions that involved the Compound protocol.
 4.Identified by checking whether the to_address_label or from_address_label contained the word 'compound'.


Normalization Method

All features were scaled using Min-Max normalization to ensure they contribute proportionally.
Formula:
normalized_value = (x - min) / (max - min + 1e-6)
This prevents any single feature from dominating due to raw scale differences.
Risk Scoring Formula
The risk score was calculated using the following weighted formula:
score = int(1000 * (
    0.5 * normalized_compound_interactions +
    0.3 * normalized_tx_count +
    0.2 * normalized_total_gas
))


Weight breakdown:

1.50 percent weight to Compound interactions
2.30 percent weight to total transaction count
3.20 percent weight to total gas used

Output Format

The final scores were saved in a CSV file named wallet_scores.csv.


Example:

wallet_id                                  | score

0xfaa0768bde629806739c3a4620656c5d26f44ef2 | 732


Justification for Feature Selection

1.Compound Interactions: Indicates direct exposure to lending and borrowing risks.
2.Transaction Count: Reflects general user activity, which could imply risk appetite.
3.Gas Usage: High gas usage often indicates use of complex smart contracts or DeFi strategies, which may carry risk.


Suggested Improvements

1.Track specific Compound events like borrow, repay, mint, and redeem.
2.Incorporate wallet token balances and debt-to-asset ratio.
3.Use unsupervised machine learning to detect clusters or anomalies.
4.Apply time-weighted analysis to prioritize recent activity over older data.


Summary

This pipeline offers a simple, scalable, and interpretable way to score Ethereum wallets based on their on-chain activity.The focus on Compound protocol usage makes the model relevant to lending and DeFi-based risk analysis.With more data sources or protocol-specific metrics, the system can be expanded and refined further.