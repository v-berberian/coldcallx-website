-- One row per promo code. claimed_at is set, once, by /claim.
CREATE TABLE IF NOT EXISTS codes (
  slot INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  claimed_at TEXT
);
