---
name: company-researcher
description: Research and analyze companies globally, both listed and private. First determine if the company is listed, then apply the appropriate analytical framework. For listed companies: use SEC EDGAR, financial statements, market data. For private companies: use融资数据、用户数据、行业报告. Use when you need to understand a company's business model, financial health, ownership structure, or investment merits.
---

# Company Research Method (Listed & Private)

## Step 0: First - Determine If Listed

**Before researching, answer this question first:**

| Question | If YES → | If NO → |
|----------|----------|---------|
| Is the company publicly traded? | Use **Part A** (Listed Company) | Use **Part B** (Private Company) |

**How to check:**
- Search "[公司名] stock code" or "[公司名] 股票代码"
- Check major exchanges: SEC, 港交所, 巨潮
- Look for: ticker symbols (AAPL), stock codes (600519), IPO dates

---

## Part A: Listed Company Analysis

**Use this for companies on major exchanges (NYSE, NASDAQ, 港交所, A股, etc.)**

### Step A1: Find Financial Data

| Market | Source | Key Documents |
|--------|--------|---------------|
| **US** | SEC EDGAR (https://www.sec.gov/edgar/) | 10-K (annual), 10-Q (quarterly), 8-K (events) |
| **China A-Share** | 巨潮资讯 (http://www.cninfo.com.cn/) | 年报、季报、公告 |
| **Hong Kong** | HKEXnews (https://www.hkexnews.hk/) | 年报、财报摘要、股东通函 |
| **Taiwan** | TPEx (https://www.tpex.org.tw/) | 财务报表、年报 |

Quick access:
- Yahoo Finance: `https://finance.yahoo.com/quote/{TICKER}`
- 东方财富: `https://www.eastmoney.com/`

### Step A2: Analyze Three Financial Statements

**Balance Sheet**:
```
Assets = Liabilities + Equity
```
Key ratios:
- Debt ratio = Total Liabilities / Total Assets (<60% healthy)
- Current ratio = Current Assets / Current Liabilities (>1.5 healthy)

**Income Statement**:
```
Revenue - Costs = Gross Profit
Gross Profit - Expenses = Operating Profit
Operating Profit - Interest/Tax = Net Income
```
Key metrics:
- Revenue growth rate (should be >10%)
- Net profit margin (>10% healthy)
- Gross margin (>50% for software)

**Cash Flow Statement**:
```
Operating CF + Investing CF + Financing CF = Net Cash Change
```
Key indicators:
- Operating CF positive = healthy
- Free cash flow = Operating CF - CapEx

### Step A3: Key Ratios for Listed Companies

| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| Debt ratio | Liabilities / Assets | <60% |
| Current ratio | Current Assets / Current Liabilities | >1.5 |
| Gross margin | Gross Profit / Revenue | Software >50% |
| Net margin | Net Income / Revenue | >10% |
| Revenue growth | (This Year - Last Year) / Last Year | >10% |
| PE ratio | Price / EPS | Industry dependent |
| ROE | Net Income / Shareholders' Equity | >15% |

### Step A4: Ownership Analysis

Check in annual report/proxy statement:
- Major shareholders (institutions, founders, state-owned)
- Management compensation and stock ownership
- Related party transactions
- Shareholder rights, voting power

### Step A5: Stock Performance

| Metric | Where to Find |
|--------|---------------|
| Historical price | Yahoo Finance, Bloomberg |
| Market cap | SEC filings, Yahoo Finance |
| Trading volume | Exchange websites |
| Analyst ratings | Seeking Alpha, Morningstar |

---

## Part B: Private Company Analysis

**Use this for startups, pre-IPO companies, unlisted businesses**

### Step B1: Find Alternative Data Sources

**For Chinese private companies:**

| Information Type | Sources |
|-----------------|---------|
| **融资信息** | 36氪 (https://36kr.com/), 虎嗅 (https://www.huxiu.com/), 天眼查 (https://www.tianyancha.com/), 企查查 (https://www.qcc.com/) |
| **用户数据** | QuestMobile, 艾瑞咨询, SimilarWeb, 七麦数据 |
| **行业报告** | 艾瑞咨询, 易观分析, 麦肯锡, 波士顿咨询 |
| **创始人背景** | LinkedIn, 知乎, 36氪人物专访 |

**For global private companies:**

| Information Type | Sources |
|-----------------|---------|
| **融资信息** | Crunchbase (https://www.crunchbase.com/), PitchBook, CB Insights |
| **用户/增长** | SimilarWeb, App Annie, Sensor Tower |
| **媒体报道** | TechCrunch, 36Kr, The Information |

### Step B2: Product & Business Analysis

**Core questions (no financial statements needed):**

| Question | What to Look For |
|----------|------------------|
| What does the product do? | Download app, experience firsthand |
| Who are the customers? | B2B, B2C, government? |
| What's the revenue model? | Subscription, transaction fee, advertising? |
| What's the market position? | Leader, follower, niche player? |
| What's the differentiation? | Technology, brand, network effects? |

### Step B3: Growth Metrics (Instead of Financials)

| Metric | What It Tells You |
|--------|-------------------|
| **User growth rate** | Product-market fit |
| **DAU/MAU ratio** | User engagement |
| **Revenue growth** | Business traction (if available) |
| **GMV** | E-commerce scale |
| **Retention rate** | Product stickiness |

**Where to find:**
- 融资公告（通常披露关键指标）
- 媒体报道（引用官方数据）
- 第三方数据（QuestMobile, SimilarWeb）

### Step B4: Funding Analysis

**Key questions:**

| Question | Why It Matters |
|----------|----------------|
| How much raised? | Runway, ability to execute |
| Who invested? | Signal from smart money |
| At what valuation? | Deal terms, investor confidence |
| How many rounds? | Stage of company |
| When last raised? | Burn rate, next funding need |

**Funding data sources:**
- 36氪、虎嗅融资报道
- 天眼查/企查查融资信息
- Crunchbase、PitchBook

### Step B5: Team Analysis

**For private companies, team matters more:**

| Factor | What to Assess |
|--------|----------------|
| **Founder background** | Education, previous companies, track record |
| **Core team** | Technical vs business balance |
| **Advisory board** | Industry connections, credibility |
| **Team size & structure** | Execution capability |
| **Key hires** | Senior talent acquisition |

**Sources:** LinkedIn, 36Kr interviews, news articles

### Step B6: Competitive Landscape

**Analysis framework:**

```
Market Size
├── Total Addressable Market (TAM)
├── Serviceable Available Market (SAM)
└── Serviceable Obtainable Market (SOM)

Competition
├── Direct competitors
├── Indirect competitors
├── Potential entrants (big tech)
└── This company → Position? Differentiation?
```

---

## Quick Comparison: Listed vs Private

| Dimension | Listed Company | Private Company |
|-----------|---------------|-----------------|
| **Primary data** | Financial statements | Growth metrics, funding |
| **Data source** | SEC/监管文件 | 媒体报道, 第三方数据 |
| **Financial health** | Quantitative (ratios) | Qualitative (burn rate, runway) |
| **Ownership** | Public filings | 融资公告, 天眼查 |
| **Valuation** | Market cap (public) | Last round valuation |
| **Key risk** | Financial distress | Funding dry-up, execution |

---

## The 6-Question Checklist (Both Types)

Answer these for any company:

1. **What does the company do?** (Product, customers, model)
2. **Who controls it?** (Owners, investors, governance)
3. **Is it performing well?** (Financials OR growth metrics)
4. **What's the recent news?** (Funding, product, scandal)
5. **What's the competitive position?** (Market share, differentiation)
6. **Why is the current situation happening?** (Root cause analysis)

---

## Key Ratios Quick Reference

| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| Debt ratio | Liabilities / Assets | <60% |
| Current ratio | Current Assets / Current Liabilities | >1.5 |
| Gross margin | Gross Profit / Revenue | Software >50% |
| Net margin | Net Income / Revenue | >10% |
| Revenue growth | YoY growth rate | >10% |
| CAC | Sales & Marketing / New Customers | < LTV |
| LTV | (ARPU × Gross Margin) / Churn | > 3× CAC |

---

## Data Sources Reference

### Listed Company Data

See [DATA_SOURCES.md](DATA_SOURCES.md) for:
- SEC EDGAR search guide
- 巨潮资讯 search guide
- HKEXnews search guide
- Financial data aggregators

### Private Company Data

See [PRIVATE_COMPANY_DATA.md](PRIVATE_COMPANY_DATA.md) for:
- Chinese startup data sources
- Global startup data sources
- Team research methods
- Competitive analysis frameworks

---

## Case Studies

For practical examples, see:
- [GRIDSUM_CASE_STUDY.md](GRIDSUM_CASE_STUDY.md) - Listed company going private analysis
- Kimi/Moonshot AI - Private company analysis (in your notes)

