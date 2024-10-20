-- Представление financial_overview_1_transactions
DROP VIEW IF EXISTS financial_overview_1_transactions;
CREATE VIEW financial_overview_1_transactions AS 
SELECT 
    t.TransactionDate AS TransactionDate,
    t.Status AS Status, 
    t.TransactionType AS TransactionType, 
    cm.CommissionType AS CommissionType,
    cl.Country AS Country,
    cm.CommissionAmount * c.ExchangeRate AS CommissionAmount,
    t.Amount * c.ExchangeRate AS Amount
FROM transactions t 
JOIN currency c ON c.`Date` = t.TransactionDateOnly
    AND c.TargetCurrency = t.Currency 
JOIN accounts a ON a.AccountID = t.AccountID
JOIN clients cl ON cl.ClientID = a.ClientID
LEFT JOIN commissions cm ON cm.TransactionID = t.TransactionID
;

-- Представление financial_overview_1_transactions_net_deposit
DROP VIEW IF EXISTS financial_overview_1_transactions_net_deposit;
CREATE VIEW financial_overview_1_transactions_net_deposit AS 
SELECT 
    toStartOfMinute(t.TransactionDate) AS TransactionDate,
    cl.Country AS Country,
    SUM(CASE WHEN t.TransactionType = 'Deposit' THEN t.Amount * c.ExchangeRate ELSE -t.Amount * c.ExchangeRate END) AS Amount
FROM transactions t
JOIN currency c ON c.`Date` = t.TransactionDateOnly
    AND c.TargetCurrency = t.Currency
JOIN accounts a ON a.AccountID = t.AccountID
JOIN clients cl ON cl.ClientID = a.ClientID
WHERE t.Status = 'Completed'
    AND t.TransactionType IN ('Deposit', 'Withdrawal')
GROUP BY toStartOfMinute(t.TransactionDate), cl.Country
;

-- Представление trading_activity_1_trades
DROP VIEW IF EXISTS trading_activity_1_trades;
CREATE VIEW trading_activity_1_trades AS 
SELECT 
    t.TradeID AS TradeID, 
    t.Instrument AS Instrument, 
    t.TradeDate AS TradeDate,
    t.Volume AS Volume, 
    t.Price * c.ExchangeRate AS Price, 
    t.TradeType AS TradeType, 
    t.ProfitLoss * c.ExchangeRate AS ProfitLoss, 
    t.Commission * c.ExchangeRate AS Commission, 
    t.Swap AS Swap,
    o.OrderDate AS OrderDate,
    o.ExecutionDate AS ExecutionDate, 
    o.AccountID AS AccountID, 
    a.AccountType AS AccountType, 
    a.Currency AS Currency, 
    cl.Country AS Country, 
    o.Status AS Status
FROM trades t 
JOIN orders o ON o.OrderID = t.OrderID
JOIN accounts a ON a.AccountID = o.AccountID
JOIN clients cl ON cl.ClientID = a.ClientID
JOIN currency c ON c.`Date` = t.TradeDateOnly
    AND c.TargetCurrency = a.Currency
;

DROP VIEW IF EXISTS client_Performance_1_trades;
CREATE VIEW client_Performance_1_trades AS 
SELECT 
    c.ClientID AS ClientID, 
    c.Name AS Name, 
    c.Country AS Country, 
    t.ProfitLoss * cur.ExchangeRate AS ProfitLoss, 
    t.TradeDate AS TradeDate,
    a.Balance * cur.ExchangeRate AS Balance, 
    c.RegistrationDate, 
    toStartOfMonth(c.RegistrationDate) AS RegistrationMonth, 
    toStartOfMonth(t.TradeDate) AS TradeMonth, 
    t.Instrument AS Instrument, 
    a.Equity * cur.ExchangeRate AS Equity, 
    rm.MaxLeverage AS MaxLeverage,
    rm.MarginCallLevel AS MarginCallLevel,
    rm.StopOutLevel AS StopOutLevel, 
    rm.MaxDailyLoss AS MaxDailyLoss, 
    rm.MaxTradeSize AS MaxTradeSize, 
    rm.RiskLevel AS RiskLevel, 
    rm.CreatedAt AS CreatedAt
FROM trades t 
	JOIN orders o ON o.OrderID = t.OrderID
	JOIN accounts a ON a.AccountID = o.AccountID
	JOIN clients c ON c.ClientID = a.ClientID
	JOIN currency cur ON cur.`Date` = t.TradeDateOnly
    	AND cur.TargetCurrency = a.Currency
    JOIN risk_management rm on rm.AccountID = a.AccountID
;


DROP VIEW IF EXISTS client_Performance_1_trades;
CREATE VIEW client_Performance_1_trades AS 
SELECT 
    c.ClientID AS ClientID, 
    c.Name AS Name, 
    c.Country AS Country, 
    a.Balance * cur.ExchangeRate AS Balance, 
    c.RegistrationDate, 
    toStartOfMonth(c.RegistrationDate) AS RegistrationMonth, 
    a.Equity * cur.ExchangeRate AS Equity, 
    rm.MaxLeverage AS MaxLeverage,
    rm.MarginCallLevel AS MarginCallLevel,
    rm.StopOutLevel AS StopOutLevel, 
    rm.MaxDailyLoss AS MaxDailyLoss, 
    rm.MaxTradeSize AS MaxTradeSize, 
    rm.RiskLevel AS RiskLevel, 
    rm.CreatedAt AS CreatedAt
FROM risk_management rm
	JOIN accounts a ON rm.AccountID = a.AccountID
	JOIN clients c ON c.ClientID = a.ClientID
	JOIN currency cur ON cur.`Date` = toDate(NOW())
    	AND cur.TargetCurrency = a.Currency
;



DROP VIEW IF EXISTS risk_management_1_risk_management;
CREATE VIEW risk_management_1_risk_management AS 
SELECT 
    c.ClientID AS ClientID,
    a.AccountID AS AccountID,
    c.Name AS Name, 
    c.Country AS Country, 
    a.Balance * cur.ExchangeRate AS Balance, 
    c.RegistrationDate, 
    toStartOfMonth(c.RegistrationDate) AS RegistrationMonth, 
    a.Equity * cur.ExchangeRate AS Equity, 
    rm.MaxLeverage AS MaxLeverage,
    rm.MarginCallLevel AS MarginCallLevel,
    rm.StopOutLevel AS StopOutLevel, 
    rm.MaxDailyLoss AS MaxDailyLoss, 
    rm.MaxTradeSize AS MaxTradeSize, 
    rm.RiskLevel AS RiskLevel, 
    rm.CreatedAt AS CreatedAt
FROM risk_management rm
	JOIN accounts a ON rm.AccountID = a.AccountID
	JOIN clients c ON c.ClientID = a.ClientID
	JOIN currency cur ON cur.`Date` = toDate(NOW())
    	AND cur.TargetCurrency = a.Currency
;

DROP VIEW IF EXISTS risk_management_2_account_exceeding;
CREATE VIEW risk_management_2_account_exceeding AS 
SELECT 
    t.TradeDate AS TradeDate,
    rm.AccountID AS AccountID, 
    c.Country AS Country, 
    rm.RiskLevel AS RiskLevel, 
    (t.Volume > rm.MaxTradeSize 
    OR t.ProfitLoss < -rm.MaxDailyLoss 
    OR a.Leverage > rm.MaxLeverage) AS is_exceeding_limits, 
    NOT (t.Volume > rm.MaxTradeSize 
    OR t.ProfitLoss < -rm.MaxDailyLoss 
    OR a.Leverage > rm.MaxLeverage) AS is_not_exceeding_limits
FROM risk_management rm
    JOIN accounts a ON rm.AccountID = a.AccountID
    JOIN orders o ON o.AccountID = a.AccountID
    JOIN trades t ON t.OrderID = o.OrderID
    JOIN clients c ON c.ClientID = a.ClientID
;