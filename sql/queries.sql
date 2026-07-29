-- =====================================================
-- NIFTY100 FINANCIAL INTELLIGENCE PLATFORM
-- Sprint 1 Day 6 - SQL Verification Queries
-- =====================================================


-- =====================================================
-- 1. CHECK ALL TABLES
-- =====================================================

SELECT name AS table_name
FROM sqlite_master
WHERE type='table'
ORDER BY name;



-- =====================================================
-- 2. RECORD COUNT OF ALL TABLES
-- =====================================================

SELECT 'companies' AS table_name, COUNT(*) AS records FROM companies
UNION ALL
SELECT 'market_cap', COUNT(*) FROM market_cap
UNION ALL
SELECT 'financial_ratios', COUNT(*) FROM financial_ratios
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices;



-- =====================================================
-- 3. COMPANY MASTER DATA
-- =====================================================

SELECT
    id,
    company_name,
    website,
    face_value,
    book_value,
    roce_percentage,
    roe_percentage
FROM companies
LIMIT 10;



-- =====================================================
-- 4. MARKET CAP DATA
-- =====================================================

SELECT
    company_id,
    year,
    market_cap_crore,
    enterprise_value_crore,
    pe_ratio,
    pb_ratio,
    ev_ebitda,
    dividend_yield_pct
FROM market_cap
LIMIT 10;



-- =====================================================
-- 5. FINANCIAL RATIOS DATA
-- =====================================================

SELECT
    company_id,
    year,
    net_profit_margin_pct,
    operating_profit_margin_pct,
    return_on_equity_pct,
    debt_to_equity,
    interest_coverage,
    free_cash_flow_cr,
    total_debt_cr
FROM financial_ratios
LIMIT 10;



-- =====================================================
-- 6. PROFIT AND LOSS DATA
-- =====================================================

SELECT
    company_id,
    year,
    sales,
    expenses,
    operating_profit,
    opm_percentage,
    profit_before_tax,
    net_profit,
    eps
FROM profitandloss
LIMIT 10;



-- =====================================================
-- 7. STOCK PRICE DATA
-- =====================================================

SELECT
    company_id,
    date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    adjusted_close
FROM stock_prices
LIMIT 10;



-- =====================================================
-- 8. CHECK DUPLICATE COMPANY YEAR RECORDS
-- DQ-02
-- =====================================================

SELECT
    company_id,
    year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;



-- =====================================================
-- 9. CHECK MISSING COMPANY IDs
-- =====================================================

SELECT DISTINCT company_id
FROM financial_ratios
WHERE company_id NOT IN
(
    SELECT id
    FROM companies
);



-- =====================================================
-- 10. COMPANY DETAILS WITH MARKET CAP
-- =====================================================

SELECT
    c.company_name,
    m.year,
    m.market_cap_crore
FROM companies c
JOIN market_cap m
ON c.id = m.company_id
ORDER BY m.market_cap_crore DESC
LIMIT 10;



-- =====================================================
-- 11. TOP PROFIT MAKING COMPANIES
-- =====================================================

SELECT
    c.company_name,
    p.year,
    p.net_profit
FROM companies c
JOIN profitandloss p
ON c.id = p.company_id
ORDER BY p.net_profit DESC
LIMIT 10;



-- =====================================================
-- 12. SALES GROWTH ANALYSIS
-- =====================================================

SELECT
    c.company_name,
    p.year,
    p.sales
FROM companies c
JOIN profitandloss p
ON c.id = p.company_id
ORDER BY c.company_name, p.year;



-- =====================================================
-- 13. ROE ANALYSIS
-- =====================================================

SELECT
    c.company_name,
    f.year,
    f.return_on_equity_pct
FROM companies c
JOIN financial_ratios f
ON c.id = f.company_id
ORDER BY f.return_on_equity_pct DESC;



-- =====================================================
-- 14. STOCK PRICE DATE RANGE
-- =====================================================

SELECT
    MIN(date) AS start_date,
    MAX(date) AS end_date
FROM stock_prices;



-- =====================================================
-- 15. AVERAGE CLOSING PRICE
-- =====================================================

SELECT
    company_id,
    AVG(close_price) AS average_close_price
FROM stock_prices
GROUP BY company_id;



-- =====================================================
-- 16. HIGHEST STOCK PRICE
-- =====================================================

SELECT
    company_id,
    MAX(high_price) AS highest_price
FROM stock_prices
GROUP BY company_id;



-- =====================================================
-- 17. CHECK NULL VALUES IN COMPANIES
-- =====================================================

SELECT *
FROM companies
WHERE id IS NULL
OR company_name IS NULL;



-- =====================================================
-- 18. ENABLE FOREIGN KEY CHECK
-- =====================================================

PRAGMA foreign_keys;



-- =====================================================
-- 19. DATABASE STRUCTURE
-- =====================================================

SELECT
    name,
    sql
FROM sqlite_master
WHERE type='table';


-- =====================================================
-- ADVANCED SQL ANALYTICS QUERIES
-- NIFTY100 FINANCIAL INTELLIGENCE PLATFORM
-- =====================================================



-- =====================================================
-- 20. COMPANY FINANCIAL PERFORMANCE SUMMARY
-- =====================================================

SELECT
    c.company_name,
    p.year,
    p.sales,
    p.operating_profit,
    p.net_profit,
    f.return_on_equity_pct,
    m.market_cap_crore
FROM companies c

JOIN profitandloss p
ON c.id = p.company_id

JOIN financial_ratios f
ON c.id = f.company_id
AND p.year = f.year

JOIN market_cap m
ON c.id = m.company_id
AND p.year = m.year

ORDER BY m.market_cap_crore DESC;



-- =====================================================
-- 21. TOP 10 COMPANIES BY MARKET CAPITALIZATION
-- =====================================================

SELECT
    c.company_name,
    m.market_cap_crore,
    m.enterprise_value_crore
FROM companies c

JOIN market_cap m
ON c.id = m.company_id

ORDER BY market_cap_crore DESC
LIMIT 10;



-- =====================================================
-- 22. LOW PE RATIO VALUE STOCKS
-- =====================================================

SELECT
    c.company_name,
    m.pe_ratio,
    m.market_cap_crore
FROM companies c

JOIN market_cap m
ON c.id = m.company_id

WHERE m.pe_ratio > 0

ORDER BY m.pe_ratio ASC
LIMIT 20;



-- =====================================================
-- 23. HIGH ROE COMPANIES
-- =====================================================

SELECT
    c.company_name,
    f.year,
    f.return_on_equity_pct
FROM companies c

JOIN financial_ratios f
ON c.id = f.company_id

WHERE f.return_on_equity_pct IS NOT NULL

ORDER BY f.return_on_equity_pct DESC
LIMIT 20;



-- =====================================================
-- 24. HIGH PROFIT MARGIN COMPANIES
-- =====================================================

SELECT
    c.company_name,
    f.net_profit_margin_pct,
    f.operating_profit_margin_pct
FROM companies c

JOIN financial_ratios f
ON c.id = f.company_id

ORDER BY f.net_profit_margin_pct DESC
LIMIT 20;



-- =====================================================
-- 25. DEBT RISK ANALYSIS
-- =====================================================

SELECT
    c.company_name,
    f.debt_to_equity,
    f.total_debt_cr
FROM companies c

JOIN financial_ratios f
ON c.id = f.company_id

WHERE f.debt_to_equity IS NOT NULL

ORDER BY f.debt_to_equity DESC
LIMIT 20;



-- =====================================================
-- 26. YEARLY PROFIT GROWTH
-- =====================================================

SELECT
    company_id,
    year,
    net_profit,

    net_profit -
    LAG(net_profit)
    OVER(
        PARTITION BY company_id
        ORDER BY year
    ) AS profit_growth

FROM profitandloss;



-- =====================================================
-- 27. SALES GROWTH PERCENTAGE
-- =====================================================

SELECT
    company_id,
    year,
    sales,

    ROUND(
    (
    sales -
    LAG(sales)
    OVER(
        PARTITION BY company_id
        ORDER BY year
    )
    )
    /
    LAG(sales)
    OVER(
        PARTITION BY company_id
        ORDER BY year
    ) * 100,
    2
    ) AS sales_growth_pct

FROM profitandloss;



-- =====================================================
-- 28. STOCK PRICE PERFORMANCE
-- =====================================================

SELECT
    company_id,

    MIN(close_price) AS lowest_price,

    MAX(close_price) AS highest_price,

    ROUND(
    (
    MAX(close_price)-MIN(close_price)
    )
    /
    MIN(close_price)*100,
    2
    )
    AS return_percentage

FROM stock_prices

GROUP BY company_id;



-- =====================================================
-- 29. DAILY PRICE CHANGE
-- =====================================================

SELECT

company_id,
date,
close_price,

close_price -

LAG(close_price)
OVER(
PARTITION BY company_id
ORDER BY date
)

AS daily_change

FROM stock_prices;



-- =====================================================
-- 30. 52 WEEK HIGH STOCKS
-- =====================================================

SELECT

company_id,

MAX(high_price)
AS one_year_high

FROM stock_prices

GROUP BY company_id;



-- =====================================================
-- 31. MARKET CAP RANKING
-- =====================================================

SELECT

c.company_name,

m.market_cap_crore,

RANK()
OVER(
ORDER BY m.market_cap_crore DESC
)
AS market_rank

FROM companies c

JOIN market_cap m

ON c.id=m.company_id;



-- =====================================================
-- 32. FINANCIAL HEALTH SCORE
-- =====================================================

SELECT

c.company_name,

(
COALESCE(f.return_on_equity_pct,0)
+
COALESCE(f.net_profit_margin_pct,0)
-
COALESCE(f.debt_to_equity,0)

)
AS financial_score


FROM companies c

JOIN financial_ratios f

ON c.id=f.company_id


ORDER BY financial_score DESC;



-- =====================================================
-- 33. COMPANY COMPLETE PROFILE
-- =====================================================

SELECT

c.company_name,

m.market_cap_crore,

p.sales,

p.net_profit,

f.return_on_equity_pct,

f.debt_to_equity


FROM companies c


LEFT JOIN market_cap m

ON c.id=m.company_id


LEFT JOIN profitandloss p

ON c.id=p.company_id


LEFT JOIN financial_ratios f

ON c.id=f.company_id;


-- =====================================================
-- 34. COMPANY VALUATION + FUNDAMENTAL SUMMARY
-- =====================================================

SELECT
    c.company_name,
    c.roce_percentage,
    c.roe_percentage,
    c.book_value,
    m.market_cap_crore,
    m.pe_ratio,
    m.pb_ratio
FROM companies c

LEFT JOIN market_cap m
ON c.id = m.company_id

ORDER BY m.market_cap_crore DESC;



-- =====================================================
-- 35. HIGH ROCE + HIGH ROE COMPANIES
-- =====================================================

SELECT
    company_name,
    roce_percentage,
    roe_percentage
FROM companies

WHERE 
    roce_percentage > 15
    AND roe_percentage > 15

ORDER BY roe_percentage DESC;



-- =====================================================
-- 36. COMPANY FUNDAMENTAL RANKING
-- =====================================================

SELECT

company_name,

(
COALESCE(roce_percentage,0)
+
COALESCE(roe_percentage,0)
+
COALESCE(book_value,0)

)

AS fundamental_score

FROM companies

ORDER BY fundamental_score DESC;



-- =====================================================
-- 37. MARKET CAP VS ROE ANALYSIS
-- =====================================================

SELECT

c.company_name,

m.market_cap_crore,

c.roe_percentage

FROM companies c

JOIN market_cap m

ON c.id = m.company_id

ORDER BY c.roe_percentage DESC;



-- =====================================================
-- 38. LOW PE + HIGH ROE VALUE SCREENING
-- =====================================================

SELECT

c.company_name,

m.pe_ratio,

c.roe_percentage,

m.market_cap_crore

FROM companies c

JOIN market_cap m

ON c.id=m.company_id


WHERE

m.pe_ratio < 25

AND c.roe_percentage > 15


ORDER BY c.roe_percentage DESC;



-- =====================================================
-- 39. COMPANY PROFILE WITH FINANCIAL METRICS
-- =====================================================

SELECT

c.company_name,

c.website,

c.about_company,

c.roce_percentage,

c.roe_percentage,

f.net_profit_margin_pct,

f.debt_to_equity,

p.sales,

p.net_profit


FROM companies c


LEFT JOIN financial_ratios f

ON c.id=f.company_id


LEFT JOIN profitandloss p

ON c.id=p.company_id;



-- =====================================================
-- 40. TOP PROFITABLE COMPANIES WITH MARKET VALUE
-- =====================================================

SELECT

c.company_name,

p.net_profit,

m.market_cap_crore

FROM companies c


JOIN profitandloss p

ON c.id=p.company_id


JOIN market_cap m

ON c.id=m.company_id


ORDER BY p.net_profit DESC

LIMIT 20;



-- =====================================================
-- 41. ROCE VS ROE COMPARISON
-- =====================================================

SELECT

company_name,

roce_percentage,

roe_percentage,

(roce_percentage - roe_percentage)

AS difference

FROM companies

ORDER BY difference DESC;



-- =====================================================
-- 42. COMPANY COUNT
-- =====================================================

SELECT

COUNT(*) AS total_companies

FROM companies;



-- =====================================================
-- 43. DATA COMPLETENESS CHECK
-- =====================================================

SELECT

COUNT(*) AS total_records,

COUNT(company_name) AS company_names_available,

COUNT(website) AS websites_available,

COUNT(roe_percentage) AS roe_available,

COUNT(roce_percentage) AS roce_available

FROM companies;



-- =====================================================
-- END UPDATED ADVANCED QUERIES
-- =====================================================




-- Check duplicate company/year records

SELECT
    company_id,
    year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;


-- Step 3: Backup profitandloss table

CREATE TABLE profitandloss_backup AS
SELECT *
FROM profitandloss;

SELECT name
FROM sqlite_master
WHERE type='table';



SELECT COUNT(*) AS original_count
FROM profitandloss;


SELECT COUNT(*) AS backup_count
FROM profitandloss_backup;




-- Step 4: Remove duplicate company/year records

DELETE FROM profitandloss
WHERE id NOT IN
(
    SELECT MIN(id)
    FROM profitandloss
    GROUP BY company_id, year
);


SELECT
    company_id,
    year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS remaining_records
FROM profitandloss;




-- Verify duplicate company/year records after cleaning

SELECT
    company_id,
    year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;


SELECT
    company_id,
    year,
    sales,
    net_profit
FROM profitandloss
WHERE company_id='ADANIPORTS';


-- Check missing companies

SELECT id, company_name
FROM companies
WHERE id IN
(
'ULTRACEMCO',
'UNIONBANK',
'UNITDSPR',
'VBL',
'VEDL',
'WIPRO',
'ZOMATO',
'ZYDUSLIFE'
);


SELECT DISTINCT company_id
FROM financial_ratios
WHERE company_id IN
(
'ULTRACEMCO',
'UNIONBANK',
'UNITDSPR',
'VBL',
'VEDL',
'WIPRO',
'ZOMATO',
'ZYDUSLIFE'
);


-- Find all company IDs used in financial tables
-- but missing from companies table

SELECT DISTINCT company_id

FROM financial_ratios

WHERE company_id NOT IN
(
    SELECT id
    FROM companies
)

ORDER BY company_id;




SELECT DISTINCT company_id
FROM financial_ratios
WHERE company_id NOT IN
(
SELECT id FROM companies
);

SELECT DISTINCT company_id

FROM profitandloss

WHERE company_id IN
(
'ULTRACEMCO',
'UNIONBANK',
'UNITDSPR',
'VBL',
'VEDL',
'WIPRO',
'ZOMATO',
'ZYDUSLIFE'
);


-- Find remaining missing companies

SELECT DISTINCT company_id
FROM profitandloss
WHERE company_id NOT IN
(
    SELECT id
    FROM companies
);

SELECT DISTINCT company_id
FROM financial_ratios
WHERE company_id NOT IN
(
SELECT id FROM companies
);


SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;


SELECT 'companies' AS table_name, COUNT(*) FROM companies
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow
UNION ALL
SELECT 'analysis', COUNT(*) FROM analysis
UNION ALL
SELECT 'documents', COUNT(*) FROM documents
UNION ALL
SELECT 'prosandcons', COUNT(*) FROM prosandcons
UNION ALL
SELECT 'financial_ratios', COUNT(*) FROM financial_ratios
UNION ALL
SELECT 'market_cap', COUNT(*) FROM market_cap
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices;

SELECT company_id,
       year,
       COUNT(*)
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT company_id,
       year,
       COUNT(*)
FROM balancesheet
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT company_id,
       year,
       COUNT(*)
FROM cashflow
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT company_id,
       year,
       COUNT(*)
FROM analysis
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT *
FROM companies
WHERE company_id IS NULL;


SELECT *
FROM profitandloss
WHERE company_id='ASIANPAINT'
AND year='Mar 2013';


SELECT *
FROM balancesheet
WHERE company_id='ABB'
AND year='Mar 2014';

PRAGMA database_list;

SELECT COUNT(*)
FROM profitandloss
WHERE company_id='ASIANPAINT'
AND year='Mar 2013';


SELECT rowid, *
FROM profitandloss
WHERE company_id='ASIANPAINT'
AND year='Mar 2013';

SELECT COUNT(*)
FROM balancesheet
WHERE company_id='ABB'
AND year='Mar 2014';


SELECT company_id,
       year,
       COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT company_id,
       year,
       COUNT(*) AS duplicate_count
FROM balancesheet
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT company_id,
       year,
       COUNT(*) AS duplicate_count
FROM cashflow
GROUP BY company_id, year
HAVING COUNT(*) > 1;


SELECT
    id,
    '[' || company_id || ']' AS company_id,
    LENGTH(company_id) AS company_length,
    '[' || year || ']' AS year,
    LENGTH(year) AS year_length
FROM profitandloss
WHERE company_id LIKE 'ASIANPAINT%';

SELECT
    TRIM(company_id) AS company_id,
    TRIM(year) AS year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY TRIM(company_id), TRIM(year)
HAVING COUNT(*) > 1;

SELECT
    id,
    company_id,
    year
FROM profitandloss
WHERE TRIM(company_id) = 'ASIANPAINT'
AND TRIM(year) = 'Mar 2013';


SELECT
    company_id,
    year,
    COUNT(*) AS cnt
FROM profitandloss
GROUP BY company_id, year
HAVING cnt > 1
ORDER BY company_id, year;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT company_id || '|' || year) AS unique_company_year
FROM profitandloss;


ALTER TABLE financial_ratios
ADD COLUMN revenue_cagr_5yr REAL;

ALTER TABLE financial_ratios
ADD COLUMN pat_cagr_5yr REAL;

ALTER TABLE financial_ratios
ADD COLUMN eps_cagr_5yr REAL;

ALTER TABLE financial_ratios
ADD COLUMN composite_quality_score REAL;

PRAGMA table_info(financial_ratios);

SELECT COUNT(*)
FROM financial_ratios;

SELECT
company_id,
year,
COUNT(*) AS total
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT
company_id,
year,
net_profit_margin_pct,
operating_profit_margin_pct,
return_on_equity_pct,
debt_to_equity,
interest_coverage,
asset_turnover,
free_cash_flow_cr,
capex_cr
FROM financial_ratios
LIMIT 10;


PRAGMA table_info(financial_ratios);

SELECT sql
FROM sqlite_master
WHERE name='financial_ratios';


SELECT
company_id,
year,
COUNT(*) AS total
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT
COUNT(*)
FROM profitandloss;

DELETE FROM financial_ratios;

INSERT INTO financial_ratios (company_id, year)
SELECT DISTINCT
    company_id,
    year
FROM profitandloss;

SELECT COUNT(*)
FROM financial_ratios;

SELECT
company_id,
year,
COUNT(*)
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1;

DELETE FROM financial_ratios;

INSERT INTO financial_ratios (company_id, year)
SELECT
    company_id,
    year
FROM profitandloss;

SELECT COUNT(*)
FROM financial_ratios;

SELECT
    company_id,
    year,
    COUNT(*) AS total
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT
    company_id,
    year,
    net_profit_margin_pct,
    return_on_equity_pct,
    debt_to_equity,
    free_cash_flow_cr
FROM financial_ratios
LIMIT 10;

PRAGMA table_info(companies);

SELECT *
FROM companies
LIMIT 1;


SELECT COUNT(*)
FROM financial_ratios;

SELECT
COUNT(net_profit_margin_pct) AS net_profit_margin,
COUNT(operating_profit_margin_pct) AS opm,
COUNT(return_on_equity_pct) AS roe,
COUNT(debt_to_equity) AS debt_equity,
COUNT(asset_turnover) AS asset_turnover,
COUNT(free_cash_flow_cr) AS free_cash_flow
FROM financial_ratios;

SELECT
company_id,
year,
COUNT(*)
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1;

SELECT
company_id,
year,
return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;

SELECT
company_id,
year,
debt_to_equity
FROM financial_ratios
ORDER BY debt_to_equity DESC
LIMIT 10;

SELECT
company_id,
year,
return_on_equity_pct,
debt_to_equity
FROM financial_ratios
WHERE
return_on_equity_pct > 15
AND debt_to_equity < 1
ORDER BY return_on_equity_pct DESC;



SELECT
COUNT(*) AS total_rows,
COUNT(revenue_cagr_5yr) AS revenue_cagr_not_null,
COUNT(pat_cagr_5yr) AS pat_cagr_not_null
FROM financial_ratios;

SELECT
company_id,
year,
revenue_cagr_5yr,
pat_cagr_5yr
FROM financial_ratios
LIMIT 20;

SELECT
COUNT(revenue_cagr_5yr),
COUNT(pat_cagr_5yr),
COUNT(eps_cagr_5yr)
FROM financial_ratios;


SELECT
COUNT(revenue_cagr_5yr) AS revenue,
COUNT(pat_cagr_5yr) AS pat,
COUNT(eps_cagr_5yr) AS eps
FROM financial_ratios;

SELECT
company_id,
year,
revenue_cagr_5yr,
pat_cagr_5yr,
eps_cagr_5yr
FROM financial_ratios
WHERE revenue_cagr_5yr IS NOT NULL
LIMIT 10;

SELECT
company_id,
year,
revenue_cagr_5yr,
pat_cagr_5yr,
eps_cagr_5yr
FROM financial_ratios
WHERE company_id='ABB';

SELECT name
FROM sqlite_master
WHERE type='table';



PRAGMA table_info(companies);

PRAGMA table_info(market_cap);

SELECT * FROM companies LIMIT 5;

SELECT * FROM market_cap LIMIT 5;

SELECT COUNT(*) FROM sectors;
SELECT * FROM sectors LIMIT 5;
SELECT
    company_id,
    broad_sector
FROM sectors

PRAGMA table_info(financial_ratios);

SELECT *
FROM financial_ratios
LIMIT 1;

SELECT name
FROM sqlite_master
WHERE type='table';

SELECT *
FROM peer_groups;

SELECT *
FROM peer_groups
LIMIT 10;

PRAGMA table_info(companies);

PRAGMA table_info(peer_groups);

SELECT COUNT(*)
FROM peer_percentiles;

SELECT name
FROM sqlite_master
WHERE type='table';

SELECT *
FROM analysis
LIMIT 5;

SELECT name
FROM sqlite_master
WHERE type='table';

PRAGMA table_info(market_cap);


SELECT DISTINCT year
FROM financial_ratios
ORDER BY year;

SELECT DISTINCT year
FROM market_cap
ORDER BY year;

SELECT company_id, year, pe_ratio
FROM market_cap
LIMIT 10;


SELECT
COUNT(*) AS TotalRows,
COUNT(composite_quality_score) AS ScoreAvailable
FROM financial_ratios
WHERE year='Mar 2024';

SELECT
company_id,
year,
composite_quality_score
FROM financial_ratios
WHERE year='Mar 2024'
LIMIT 10;

SELECT
    year,
    COUNT(composite_quality_score) AS ScoreCount
FROM financial_ratios
GROUP BY year
ORDER BY year;

PRAGMA table_info(documents);

PRAGMA table_info(companies);
PRAGMA table_info(documents);
PRAGMA table_info(sectors);

PRAGMA table_info(financial_ratios);

SELECT
    year,
    return_on_equity_pct,
    net_profit_margin_pct,
    debt_to_equity,
    revenue_cagr_5yr,
    free_cash_flow_cr
FROM financial_ratios
WHERE company_id = 'ABB';

PRAGMA table_info(profitandloss);
SELECT *
FROM profitandloss
WHERE company_id='ABB'
LIMIT 5;

SELECT
    id,
    company_name,
    roce_percentage,
    roe_percentage
FROM companies
WHERE id='ABB';

PRAGMA table_info(prosandcons);
SELECT *
FROM prosandcons
WHERE company_id='ABB';

SELECT COUNT(*)
FROM prosandcons;
SELECT *
FROM prosandcons
LIMIT 10;

SELECT name FROM sqlite_master WHERE type='table';

PRAGMA table_info(financial_ratios);
PRAGMA table_info(peer_percentiles);

PRAGMA table_info(companies);

PRAGMA table_info(sectors);

PRAGMA table_info(market_cap);

PRAGMA table_info(analysis);

PRAGMA table_info(documents);