-- Star Schema & Feature Tables for RecoMart Data Warehouse

CREATE TABLE IF NOT EXISTS dim_users (
    user_id VARCHAR(50) PRIMARY KEY,
    total_interactions INT,
    total_purchases INT,
    avg_user_rating FLOAT,
    last_active_ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    category_encoded INT,
    price FLOAT,
    price_normalized FLOAT,
    external_sentiment_score FLOAT,
    avg_item_rating FLOAT,
    interaction_count INT
);

CREATE TABLE IF NOT EXISTS fact_user_item_features (
    user_id VARCHAR(50),
    product_id VARCHAR(50),
    interaction_score FLOAT,
    event_timestamp TIMESTAMP,
    PRIMARY KEY (user_id, product_id)
);
