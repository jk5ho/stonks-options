USE project_stonk;

-- Populates database with stock prices
DROP PROCEDURE IF EXISTS parseStocks;
DELIMITER $$
CREATE PROCEDURE parseStocks(
    IN symbol  VARCHAR(8),
    IN date    DATE,
    IN high    DECIMAL(8, 2),
    IN low     DECIMAL(8, 2),
    IN open    DECIMAL(8, 2),
    IN close   DECIMAL(8, 2),
    IN volume  INT
)
BEGIN
    START TRANSACTION;
    INSERT INTO Stocks VALUES (symbol, date, high, low, open, close, volume);
    COMMIT;
END $$
DELIMITER ;

-- Populates database with option prices
DROP PROCEDURE IF EXISTS parseOptions;
DELIMITER $$
CREATE PROCEDURE parseOptions(
    IN id              VARCHAR(255),
    IN symbol          VARCHAR(8),
    IN expiry          DATE,
    IN contractSize    INT,
    IN strikePrice     INT,
    IN closingPrice    DECIMAL(16, 8),
    IN side            VARCHAR(8),
    IN type            VARCHAR(8),
    IN volume          INT,
    IN openInterest    INT,
    IN bid             DECIMAL(16, 8),
    IN ask             DECIMAL(16, 8),
    IN lastUpdated     DATE,
    IN isAdjusted      BOOLEAN
)
BEGIN
    START TRANSACTION;
    INSERT INTO Options VALUES (id, symbol, expiry, contractSize, strikePrice, closingPrice, side, type, volume, openInterest, bid, ask, lastUpdated, isAdjusted);
    COMMIT;
END $$
DELIMITER ;

-- Removes options that are expired
DROP PROCEDURE IF EXISTS cleanOptions;
DELIMITER $$
CREATE PROCEDURE cleanOptions()
BEGIN 
    DECLARE currDate DATE DEFAULT NULL;
    SET currDate = CURRENT_DATE();

    DELETE FROM Options WHERE expiry < currDate; 
END $$
DELIMITER ;
