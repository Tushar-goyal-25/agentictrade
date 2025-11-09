CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS market_bars_raw (
    symbol TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    interval TEXT NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (symbol, ts, interval)
    
);

SELECT create_hypertable('market_bars_raw', 'ts', if_not_exists => TRUE);


CREATE TABLE IF NOT EXISTS news_raw (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMPTZ ,
    headline TEXT ,
    content TEXT ,
    url TEXT,
    sentiment_score DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS features_latetst (
    symbol TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    feature JSONB,
    PRIMARY KEY (symbol, ts)
);