CREATE TABLE MATCH_PARTICIPANTS(
    MATCH_ID TEXT,
    TOPB TEXT,
    JUNGB TEXT,
    MIDB TEXT,
    ADCB TEXT,
    SUPPORTB TEXT,
    TOPR TEXT,
    JUNGR TEXT,
    MIDR TEXT,
    ADCR TEXT,
    SUPPORTR TEXT,
    FOREIGN KEY (MATCH_ID) REFERENCES MATCHES (MATCH_ID)
)