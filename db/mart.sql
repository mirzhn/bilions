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

-- Представление client_perfomance_view
DROP VIEW IF EXISTS client_perfomance_view;
CREATE VIEW client_perfomance_view AS 
SELECT 
    c.ClientID AS ClientID, 
    c.Name AS Name, 
    c.Country AS Country, 
    t.ProfitLoss AS ProfitLoss, 
    t.TradeDate AS TradeDate,
    a.Balance AS Balance, 
    c.RegistrationDate, 
    toStartOfMonth(c.RegistrationDate) AS RegistrationMonth, 
    toStartOfMonth(t.TradeDate) AS TradeMonth
FROM default.trades t 
JOIN default.orders o ON o.OrderID = t.OrderID
JOIN default.accounts a ON a.AccountID = o.AccountID
JOIN default.clients c ON c.ClientID = a.ClientID
;

-- Представление risk_management_view
DROP VIEW IF EXISTS risk_management_view;
CREATE VIEW risk_management_view AS 
SELECT 
    rm.AccountID AS AccountID, 
    rm.MaxLeverage AS MaxLeverage,
    rm.MarginCallLevel AS MarginCallLevel,
    rm.StopOutLevel AS StopOutLevel, 
    rm.MaxDailyLoss AS MaxDailyLoss, 
    rm.MaxTradeSize AS MaxTradeSize, 
    rm.RiskLevel AS RiskLevel, 
    rm.CreatedAt AS CreatedAt, 
    a.Balance AS Balance, 
    a.Equity AS Equity
FROM risk_management rm
JOIN default.accounts a ON a.AccountID = rm.AccountID
;

-- Представление account_exceeding_limits_view
DROP VIEW IF EXISTS account_exceeding_limits_view;
CREATE VIEW account_exceeding_limits_view AS 
SELECT 
    t.TradeDate AS TradeDate,
    rm.AccountID AS AccountID, 
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
;
