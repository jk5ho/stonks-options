CREATE DATABASE IF NOT EXISTS project_stonk;
CREATE USER IF NOT EXISTS 'hobin'@'localhost' IDENTIFIED BY 'rood';
GRANT ALL PRIVILEGES ON project_stonk.* TO 'hobin'@'localhost';
USE project_stonk;

DROP TABLE IF EXISTS Stocks;
DROP TABLE IF EXISTS Options;

CREATE TABLE Stocks (
    symbol          VARCHAR(8)      NOT NULL,
    date            DATE            NOT NULL,
    high            DECIMAL(8, 2)   NOT NULL,
    low             DECIMAL(8, 2)   NOT NULL,
    open            DECIMAL(8, 2)   NOT NULL,
    close           DECIMAL(8, 2)   NOT NULL,
    volume          INT             NOT NULL
);

CREATE TABLE Options (
    id              VARCHAR(255)    NOT NULL,
    symbol          VARCHAR(8)      NOT NULL,
    expiry          DATE            NOT NULL,
    contractSize    INT             NOT NULL,
    strikePrice     INT             NOT NULL,
    closingPrice    DECIMAL(16, 8)  NOT NULL,
    side            VARCHAR(8)      NOT NULL,
    type            VARCHAR(8)      NOT NULL,
    volume          INT             NOT NULL,
    openInterest    INT             NOT NULL,
    bid             DECIMAL(16, 8)  NOT NULL,
    ask             DECIMAL(16, 8)  NOT NULL,
    lastUpdated     DATE            NOT NULL,
    isAdjusted      BOOLEAN         NOT NULL
);
