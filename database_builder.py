import psycopg2
import os
from dotenv import load_dotenv

DB_PASSWORD = os.getenv('server_password')

conn = psycopg2.connect(
    dbname="postgres", user="postgres", password=DB_PASSWORD, host="localhost"
)
conn.autocommit = True
cur = conn.cursor()

# Step 2: Create database + user
cur.execute("CREATE DATABASE portfolio_db;")
cur.execute(f"CREATE USER portfolio_user WITH PASSWORD {DB_PASSWORD};")
cur.execute("GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;")

cur.close()
conn.close()

# Step 3: Connect to new DB and create tables
conn = psycopg2.connect(
    dbname="portfolio_db", user="portfolio_user", password="strongpassword", host="localhost"
)
cur = conn.cursor()

schema_sql = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  risk_profile JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS assets (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  name TEXT,
  asset_class TEXT,
  exchange TEXT,
  meta JSONB
);

CREATE TABLE IF NOT EXISTS prices (
  asset_id INT REFERENCES assets(id),
  ts TIMESTAMPTZ NOT NULL,
  open NUMERIC,
  high NUMERIC,
  low NUMERIC,
  close NUMERIC,
  volume BIGINT,
  PRIMARY KEY (asset_id, ts)
);

CREATE INDEX IF NOT EXISTS idx_prices_asset_ts ON prices (asset_id, ts DESC);

CREATE TABLE IF NOT EXISTS portfolios (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  name TEXT,
  constraints JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS portfolio_allocations (
  id SERIAL PRIMARY KEY,
  portfolio_id UUID REFERENCES portfolios(id),
  asset_id INT REFERENCES assets(id),
  weight NUMERIC,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_logs (
  id SERIAL PRIMARY KEY,
  agent_name TEXT,
  event_time TIMESTAMPTZ DEFAULT now(),
  payload JSONB
);
"""

cur.execute(schema_sql)
conn.commit()
cur.close()
conn.close()
