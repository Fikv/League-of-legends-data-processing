CREATE TABLE PLAYER_LP_GAINS(
    PLAYER_ID VARCHAR(100),
    DATE_OF_UPDATE TIMESTAMP,
    AMOUNT_OF_LPS INTEGER,
	FOREIGN KEY (PLAYER_ID) REFERENCES PLAYER (PLAYER_ID)
)