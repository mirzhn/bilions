-- Таблица клиентов
DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
    ClientID UUID,                          -- Уникальный идентификатор клиента
    Name String,                            -- Имя клиента
    Country String,                         -- Страна клиента
    RegistrationDate DateTime,              -- Дата регистрации клиента
    AccountStatus String,                   -- Статус аккаунта (активен, заморожен, закрыт)
    RiskLevel String                        -- Уровень риска (низкий, средний, высокий)
) ENGINE = MergeTree()
ORDER BY ClientID;

-- Таблица аккаунтов
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    AccountID UUID,                         -- Уникальный идентификатор аккаунта
    ClientID UUID,                          -- Ссылка на клиента (Foreign Key)
    AccountType String,                     -- Тип аккаунта (реальный, демо)
    Currency String,                        -- Валюта счета (USD, EUR и т.д.)
    Balance Decimal(18, 2),                 -- Текущий баланс счета
    Equity Decimal(18, 2),                  -- Текущая стоимость средств на счете
    Leverage Float32                        -- Плечо (например, 1:100)
) ENGINE = MergeTree()
ORDER BY AccountID;

-- Таблица ордеров
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    OrderID UUID,                           -- Уникальный идентификатор ордера
    AccountID UUID,                         -- Ссылка на аккаунт клиента
    Instrument String,                      -- Торговый инструмент (например, EUR/USD)
    OrderType String,                       -- Тип ордера (Buy, Sell, Limit, Stop)
    Volume Decimal(18, 2),                  -- Объем ордера
    Price Decimal(18, 5),                   -- Цена исполнения ордера
    Status String,                          -- Статус ордера (Pending, Executed, Partially Executed, Cancelled)
    OrderDate DateTime,                     -- Дата и время создания ордера
    ExecutionDate DateTime,                 -- Дата и время исполнения ордера
    Commission Decimal(18, 2),              -- Комиссия за исполнение ордера
    PositionId UUID                         -- Ссылка на позицию
) ENGINE = MergeTree()
ORDER BY OrderID;

-- Таблица сделок
DROP TABLE IF EXISTS trades;
CREATE TABLE trades (
    TradeID UUID,                           -- Уникальный идентификатор сделки
    OrderID UUID,                           -- Ссылка на связанный ордер
    Instrument String,                      -- Торговый инструмент (например, EUR/USD)
    TradeDate DateTime,                     -- Дата и время исполнения сделки
    Volume Decimal(18, 2),                  -- Объем сделки
    Price Decimal(18, 5),                   -- Цена сделки
    TradeType String,                       -- Тип сделки (Buy или Sell)
    ProfitLoss Decimal(18, 2),              -- Прибыль или убыток по сделке
    Commission Decimal(18, 2),              -- Комиссия за сделку
    Swap Decimal(18, 2),                    -- Своп за удержание позиции (если применимо)
    TradeDateOnly Date MATERIALIZED toDate(TradeDate)
) ENGINE = MergeTree()
ORDER BY TradeID
SETTINGS index_granularity = 64;

-- Индексы для trades
ALTER TABLE trades ADD INDEX idx_trades_Instrument (Instrument) TYPE set(0) GRANULARITY 64;
ALTER TABLE trades ADD INDEX idx_trades_TradeDate (TradeDate) TYPE set(0) GRANULARITY 64;

-- Таблица позиций
DROP TABLE IF EXISTS positions;
CREATE TABLE positions (
    PositionID UUID,                        -- Уникальный идентификатор позиции
    AccountID UUID,                         -- Ссылка на торговый счет клиента
    Instrument String,                      -- Торговый инструмент (например, EUR/USD)
    Volume Decimal(18, 2),                  -- Объем позиции
    OpenPrice Decimal(18, 5),               -- Цена открытия позиции
    ClosePrice Decimal(18, 5) NULL,         -- Цена закрытия позиции (если позиция закрыта)
    OpenDate DateTime,                      -- Дата и время открытия позиции
    CloseDate DateTime NULL,                -- Дата и время закрытия позиции (если позиция закрыта)
    PnL Decimal(18, 2) NULL,                -- Прибыль или убыток по позиции
    Status String,                          -- Статус позиции (open/closed)
    OpenOrderID UUID,                       -- Ссылка на ордер, который открыл позицию
    CloseOrderID UUID NULL                  -- Ссылка на ордер, который закрыл позицию (если закрыта)
) ENGINE = MergeTree()
ORDER BY PositionID;

-- Таблица комиссий
DROP TABLE IF EXISTS commissions;
CREATE TABLE commissions (
    CommissionID UUID,                      -- Уникальный идентификатор комиссии
    TransactionID UUID,                     -- Ссылка на транзакцию
    AccountID UUID,                         -- Ссылка на аккаунт
    CommissionType String,                  -- Тип комиссии (фиксированная, динамическая)
    CommissionAmount Decimal(18, 2),        -- Сумма комиссии
    CommissionDate DateTime                 -- Дата и время начисления комиссии
) ENGINE = MergeTree()
ORDER BY CommissionID;

-- Индекс для commissions
ALTER TABLE commissions ADD INDEX idx_transaction_id (TransactionID) TYPE set(0) GRANULARITY 64;

-- Таблица отчетов
DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    ReportID UUID,                          -- Уникальный идентификатор отчета
    AccountID UUID,                         -- Ссылка на аккаунт
    ReportType String,                      -- Тип отчета (Trade Report, PnL Report, Position Report)
    GeneratedDate DateTime,                 -- Дата и время генерации отчета
    ReportPeriodStart DateTime,             -- Начало отчетного периода
    ReportPeriodEnd DateTime,               -- Конец отчетного периода
    Status String,                          -- Статус отчета (сгенерирован, отправлен)
    DeliveryMethod String,                  -- Способ доставки (email, API, внутренняя система)
    ReportData String                       -- Данные отчета в формате JSON
) ENGINE = MergeTree()
ORDER BY ReportID;

-- Таблица транзакций
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    TransactionID UUID,                     -- Уникальный идентификатор транзакции
    AccountID UUID,                         -- Ссылка на торговый счет клиента
    TransactionType String,                 -- Тип транзакции (Deposit, Withdrawal, Bonus, Commission)
    Amount Decimal(18, 2),                  -- Сумма транзакции
    Currency String,                        -- Валюта транзакции (например, USD, EUR)
    TransactionDate DateTime,               -- Дата и время транзакции
    Status String,                          -- Статус транзакции (Completed, Pending, Failed)
    TransactionDateOnly Date MATERIALIZED toDate(TransactionDate)
) ENGINE = MergeTree()
ORDER BY TransactionID;

-- Индексы для transactions
ALTER TABLE transactions ADD INDEX idx_transaction_type (TransactionType) TYPE set(0) GRANULARITY 64;
ALTER TABLE transactions ADD INDEX idx_currency (Currency) TYPE set(0) GRANULARITY 64;
ALTER TABLE transactions ADD INDEX idx_transaction_date (TransactionDate) TYPE minmax GRANULARITY 64;
ALTER TABLE transactions ADD INDEX idx_account_id (AccountID) TYPE set(0) GRANULARITY 64;

-- Таблица управления рисками
DROP TABLE IF EXISTS risk_management;
CREATE TABLE risk_management (
    RiskID UUID,                            -- Уникальный идентификатор для каждой записи управления рисками
    AccountID UUID,                         -- Ссылка на торговый счет клиента
    MaxLeverage Decimal(5, 2),              -- Максимальное кредитное плечо для аккаунта
    MarginCallLevel Decimal(5, 2),          -- Уровень маржинального требования (%)
    StopOutLevel Decimal(5, 2),             -- Уровень Stop Out (%)
    MaxDailyLoss Decimal(18, 2),            -- Максимальные ежедневные потери для счета
    MaxTradeSize Decimal(18, 2),            -- Максимальный размер сделки
    RiskLevel String,                       -- Уровень риска (Low, Medium, High)
    CreatedAt DateTime,                     -- Дата создания настройки управления рисками
    UpdatedAt DateTime                      -- Дата последнего обновления настройки
) ENGINE = MergeTree()
ORDER BY RiskID;

-- Таблица валютных курсов
DROP TABLE IF EXISTS currency;
CREATE TABLE currency (
    Date Date,
    BaseCurrency String,
    TargetCurrency String,
    ExchangeRate Float32
) ENGINE = MergeTree()
ORDER BY Date;

-- Индекс для currency
ALTER TABLE currency ADD INDEX idx_date_target_currency (Date, TargetCurrency) TYPE set(0) GRANULARITY 64;
