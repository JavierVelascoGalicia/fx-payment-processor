CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(), 
    created_at TIMESTAMPTZ DEFAULT NOW());

CREATE TABLE IF NOT EXISTS wallets (
    wallet_id SERIAL PRIMARY KEY,
    user_id INT,
    balance DECIMAL DEFAULT 0.00,
    currency CHAR(3),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id));

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    wallet_id INT,
    user_id INT,
    amount DECIMAL,
    currency CHAR(3),
    transaction_type INT,
    transaction_date TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT fk_wallet FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id));

