-- Core table
DROP TABLE IF EXISTS crises;
DROP TABLE IF EXISTS monthly_coverage;
DROP TABLE IF EXISTS coverage_by_outlet;
DROP TABLE IF EXISTS framing;
DROP TABLE IF EXISTS sentiment ;
DROP TABLE IF EXISTS victim_causor;

CREATE TABLE crises (
    crisis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crisis_name TEXT UNIQUE,
    start_date TEXT,
    fund_required REAL,
    people_affected REAL,
    crisis_days INTEGER,
    raw_coverage INTEGER,
    coverage_per_day REAL,
    coverage_per_funding REAL,
    coverage_per_people REAL
);

-- Monthly coverage
CREATE TABLE monthly_coverage (
    monthly_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crisis_id INTEGER,
    year_month TEXT,
    coverage_count INTEGER,
    FOREIGN KEY (crisis_id) REFERENCES crises(crisis_id)
);


-- Coverage by outlet
CREATE TABLE coverage_by_outlet (
    coverage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crisis_id INTEGER,
    outlet_name TEXT,
    coverage_count INTEGER,
    coverage_per_day REAL,
    coverage_per_funding REAL,
    coverage_per_people REAL,
    FOREIGN KEY (crisis_id) REFERENCES crises(crisis_id)
);

-- Framing
CREATE TABLE framing (
    framing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crisis_id INTEGER,
    outlet_name TEXT,
    framing_type TEXT,
    raw_count INTEGER,
    article_count INTEGER,
    mentions_per_article REAL,
    FOREIGN KEY (crisis_id) REFERENCES crises(crisis_id)
);

-- Sentiment
CREATE TABLE sentiment (
    sentiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crisis_id INTEGER,
    outlet_name TEXT,
    entity TEXT,
    sentiment TEXT,
    raw_count INTEGER,
    mentions_per_article REAL,
    FOREIGN KEY (crisis_id) REFERENCES crises(crisis_id)
);

-- Victim/Causor
CREATE TABLE victim_causor (
    vc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crisis_id INTEGER,
    outlet_name TEXT,
    "group" TEXT,
    framing_type TEXT,
    raw_count INTEGER,
    mentions_per_article REAL,
    FOREIGN KEY (crisis_id) REFERENCES crises(crisis_id)
);
