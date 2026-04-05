# 数据来源获取指南

> 本文档分析产品发现流程中各阶段所需的数据来源、获取方式以及实现方案。
> 状态：分析阶段，待实现具体工具

---

## 问题陈述

产品发现流程需要数据支撑，但各阶段的数据来源分散、获取方式不一、格式各异。本文档旨在：
1. 明确每个阶段需要什么数据
2. 分析现实可行的数据来源
3. 提出分层实现方案
4. 定义标准数据格式

---

## 各阶段数据需求分析

### 阶段 1：机会发现 - 用户摩擦信号

**需要什么数据？**
- 用户投诉、差评、讨论（原始文本）
- 情感强度评分（处理后的数据）
- 聚类后的主题（分析结果）

**现实数据源分析：**

| 数据源 | 获取方式 | 难度 | 可靠性 | 备注 |
|--------|---------|------|--------|------|
| Reddit | API (PRAW) / 爬虫 | 中等 | 高 | 有官方 API，但有频率限制 |
| Twitter/X | API (付费) / 爬虫 | 高 | 高 | API 付费且严格，爬虫反爬强 |
| App Store | 第三方服务 / 爬虫 | 中等 | 高 | Sensor Tower 付费，有开源爬虫 |
| Google Play | 开源爬虫工具 | 低 | 高 | 有多个开源项目可用 |
| 知乎 | 爬虫 | 高 | 中 | 反爬严格，需要 Cookie |
| 小红书 | 爬虫 | 高 | 中 | 反爬严格 |
| 亚马逊评论 | 开源工具 | 低 | 高 | 有成熟的开源解决方案 |
| Discord | Bot API | 中等 | 高 | 需要服务器权限 |

**核心难点：**
- 爬取需要代码，反爬策略经常变化
- 情感分析需要 NLP 模型（可用 Hugging Face 开源模型）
- 聚类分析需要算法支持

---

### 阶段 2：机会评估 - 市场规模

**需要什么数据？**
- TAM/SAM/SOM（市场规模估算）
- 竞品数据（定价、用户量、融资情况）
- 行业报告数据

**现实数据源分析：**

| 数据类型 | 来源 | 可行性 | 成本 |
|---------|------|--------|------|
| 市场规模 | 艾瑞、易观、Statista | 部分免费 | 报告大多付费 |
| 竞品融资 | Crunchbase API | 有限免费 | 免费版有额度限制 |
| 竞品定价 | 官网直接查看 | 容易 | 免费 |
| 竞品用户量 | SimilarWeb、App Annie | 需要付费 | 付费工具 |
| 搜索趋势 | Google Trends API | 免费 | 免费 |
| 行业报告 | 36氪、虎嗅、晚点 | 部分免费 | 需人工整理 |

**核心难点：**
- 高质量数据大多付费
- 需要人工整合多个来源
- 数据更新频率不一

---

### 阶段 3：用户研究 - Persona & JTBD

**需要什么数据？**
- 用户访谈记录（定性）
- 问卷数据（定量）
- 行为数据（热力图、埋点）

**现实数据源分析：**

| 数据类型 | 获取方式 | 自动化程度 |
|---------|---------|-----------|
| 用户访谈 | 招募用户进行访谈 | 无法自动化 |
| 问卷 | 问卷星、腾讯问卷、Google Forms | 半自动（可分发，需人工分析）|
| 行为数据 | 热力图工具（Hotjar）、埋点 | 需产品上线后 |
| 可用性测试 | Maze、UserTesting | 半自动 |

**核心难点：**
- 最难自动化，必须人工参与
- 但可以提供访谈提纲、问卷模板辅助

---

### 阶段 4-6：解决方案设计 & 文档编写

这些阶段主要是方法论应用，对外部数据依赖较少。

---

## 实现方案讨论

### 方案 A：提供真实可用的代码工具

**做法：**
- 为每个数据源编写 Python 脚本（Reddit API、App Store 爬虫等）
- 提供情感分析模型（Hugging Face 开源模型）
- 提供聚类分析代码（scikit-learn）

**优点：**
- 真实可用，AI 可以直接运行
- 数据质量高

**缺点：**
- 需要配置 API Key、处理反爬
- 代码可能很快过时（平台政策变化）
- 需要安装依赖（Python 环境）
- 维护成本高

---

### 方案 B：模拟数据 + 人工补充

**做法：**
- AI 生成"模拟的用户反馈数据"（基于公开信息）
- 用户补充真实数据（手动贴几条关键差评）
- AI 基于混合数据进行分析

**优点：**
- 门槛低，不需要配置
- 快速体验完整流程

**缺点：**
- 模拟数据可能不够真实
- 分析结果可信度降低

---

### 方案 C：集成第三方数据服务

**做法：**
- 推荐可用的数据服务（Sensor Tower、Crunchbase 等）
- 提供数据导入模板
- 用户导出数据后，AI 帮助分析

**优点：**
- 数据质量高
- 专业可靠

**缺点：**
- 大多需要付费
- 需要人工导出和导入

---

### 方案 D：分层处理（推荐）

**做法：**
- **全自动层**：提供代码工具，能跑就跑
- **半自动层**：提供数据抓取指导，用户手动获取后导入
- **手动层**：提供模板，用户填写数据
- **模拟层**：提供 mock 数据用于快速体验

**优点：**
- 灵活适应不同用户需求
- 渐进式实现，降低门槛

---

## 标准数据格式定义

### 用户摩擦信号数据格式

```json
{
  "feedback_items": [
    {
      "id": "uuid",
      "source": "reddit|app_store|twitter|google_play|manual",
      "platform": "productivity|smallbusiness|...",
      "original_text": "原始文本内容",
      "translated_text": "中文翻译（可选）",
      "emotion_score": 4.3,
      "emotion_label": "frustrated|angry|confused|satisfied",
      "topics": ["knowledge_management", "search_difficulty"],
      "timestamp": "2024-01-15T10:30:00Z",
      "url": "原始链接（可选）",
      "metadata": {
        "upvotes": 342,
        "replies": 15
      }
    }
  ],
  "summary": {
    "total_count": 1247,
    "avg_emotion_score": 4.1,
    "top_topics": [
      {"topic": "knowledge_scattered", "count": 247, "avg_score": 4.3},
      {"topic": "search_difficult", "count": 189, "avg_score": 4.1}
    ]
  }
}
```

### 竞品数据格式

```json
{
  "competitors": [
    {
      "name": "Notion",
      "website": "https://notion.so",
      "pricing": {
        "free_tier": true,
        "monthly": 8,
        "currency": "USD",
        "notes": "个人 Pro 版"
      },
      "user_count": "30M+",
      "funding": {
        "total": "343M",
        "last_round": "Series C"
      },
      "pain_points": [
        {"text": "太灵活反而不知如何组织", "frequency": "high"},
        {"text": "搜索功能不好用", "frequency": "high"},
        {"text": "移动端体验差", "frequency": "medium"}
      ],
      "strengths": ["功能强大", "模板丰富"],
      "data_source": "crunchbase|app_store|manual",
      "last_updated": "2024-01-15"
    }
  ]
}
```

### 市场规模数据格式

```json
{
  "market_analysis": {
    "tam": {
      "value": "1200B",
      "currency": "USD",
      "year": 2024,
      "cagr": "12%",
      "source": "statista|report_name"
    },
    "sam": {
      "value": "80B",
      "currency": "USD",
      "calculation": "基于细分市场估算"
    },
    "som": {
      "value": "1M",
      "currency": "USD",
      "year_1_users": 10000,
      "arp": 100,
      "calculation": "第一年获得 1% 市场份额"
    }
  }
}
```

### 用户访谈数据格式

```json
{
  "interviews": [
    {
      "id": "I001",
      "persona": "researcher_li",
      "date": "2024-01-10",
      "method": "video_call|in_person",
      "duration_minutes": 45,
      "key_quotes": [
        {
          "quote": "我在 Notion 里存了 300 多页笔记，但找东西时根本不知道在哪",
          "topic": "search_difficulty",
          "context": "描述当前痛点"
        }
      ],
      "pain_points": ["搜索困难", "知识分散"],
      "goals": ["快速找到需要的信息", "自动整理知识"],
      "insights": ["用户愿意付费解决搜索问题"]
    }
  ]
}
```

---

## 分层实现建议

### 第一层：全自动（Python 脚本）

**工具清单：**

1. **Reddit 数据抓取**
   - 工具：PRAW (Python Reddit API Wrapper)
   - 需求：Reddit API Key
   - 输出：标准 feedback_items JSON

2. **Google Play 评论抓取**
   - 工具：google-play-scraper (开源)
   - 需求：无需 API Key
   - 输出：标准 feedback_items JSON

3. **情感分析**
   - 工具：Hugging Face transformers
   - 模型：distilbert-base-uncased-finetuned-sst-2-english 或中文情感分析模型
   - 输出：emotion_score + emotion_label

4. **主题聚类**
   - 工具：scikit-learn (K-means) 或 BERTopic
   - 输入：feedback_items
   - 输出：topics 标签

5. **竞品数据抓取**
   - 工具：Crunchbase API (有限免费)
   - 需求：API Key
   - 输出：competitors JSON

**实施难点：**
- 需要维护依赖环境
- 反爬策略变化需要更新
- API 限制需要处理

---

### 第二层：半自动（浏览器插件/导出工具）

**工具清单：**

1. **App Store 评论导出**
   - 方法：使用 App Store 的 RSS feed + 解析工具
   - 或使用开源工具如 app-store-scraper
   - 用户操作：运行脚本或导出 CSV

2. **网页数据抓取**
   - 工具：浏览器插件如 Web Scraper
   - 或 Chrome DevTools 的 Network 面板
   - 用户操作：手动抓取后导入

3. **数据清洗脚本**
   - 输入：各种格式的原始数据
   - 输出：标准 JSON 格式
   - 功能：去重、翻译、格式化

---

### 第三层：全手动（模板填写）

**工具清单：**

1. **用户反馈收集模板**
   - Markdown 表格模板
   - 用户手动粘贴关键反馈

2. **竞品分析模板**
   - 结构化问卷
   - 引导用户填写关键信息

3. **访谈记录模板**
   - 标准化访谈提纲
   - 记录格式指南

---

### 第四层：模拟数据（快速体验）

**用途：**
- 让用户快速体验完整流程
- 培训和学习
- 演示 Skill 能力

**数据特征：**
- 基于真实模式生成
- 有合理的情感分布
- 覆盖典型主题

---

## RICE 评分的数据来源

### Reach（触达人数）

**数据来源：**
- 行业报告中的用户规模数据
- 搜索指数（百度指数、Google Trends）
- 竞品公开的用户数量
- 社交媒体相关话题的讨论量

**估算方法：**
```
Reach = 目标用户群体规模 × 预期渗透率
```

### Impact（影响深度）

**数据来源：**
- 用户反馈的情感强度
- 用户访谈中的痛点描述
- 竞品差评中的高频词汇

**评分标准：**
- 5 分：解决生存级痛点（如支付失败）
- 4 分：解决重要痛点（如搜索困难）
- 3 分：明显改进体验
- 2 分：小幅提升
- 1 分：锦上添花

### Confidence（信心度）

**数据来源：**
- 数据样本量大小
- 数据质量（一手 vs 二手）
- 假设验证程度

**评分标准：**
- 10 分：有大量一手数据验证
- 7 分：有行业数据支撑
- 5 分：部分数据，部分假设
- 3 分：主要是假设

### Effort（工作量）

**数据来源：**
- 技术方案评估
- 类似功能的历史开发时间
- 团队能力评估

**评估维度：**
- 人月数
- 技术复杂度
- 依赖风险

---

## 下一步行动建议

### 短期（MVP）

1. **实现模拟数据生成器**
   - 基于行业模板生成逼真的用户反馈
   - 让用户快速体验完整流程

2. **提供手动填写模板**
   - 用户反馈收集表
   - 竞品分析表
   - 市场规模估算表

3. **定义标准数据接口**
   - 确保后续工具可以无缝接入

### 中期

1. **开发 Reddit/Google Play 抓取脚本**
   - 提供即用型 Python 脚本
   - 包含安装和配置指南

2. **集成情感分析模型**
   - 使用 Hugging Face 开源模型
   - 支持中英文

3. **数据清洗和转换工具**
   - 将各种格式转换为标准 JSON

### 长期

1. **浏览器插件**
   - 一键抓取当前页面数据
   - 自动填充分析模板

2. **数据可视化**
   - 自动生成分析报告图表
   - 趋势分析和对比

3. **自动化报告生成**
   - 基于数据自动生成 PRD 初稿
   - 智能推荐功能优先级

---

## 参考资源

### 开源工具

- **PRAW**: Reddit API 的 Python 封装
- **google-play-scraper**: Google Play 应用数据抓取
- **app-store-scraper**: App Store 应用数据抓取
- **transformers**: Hugging Face 的 NLP 模型库
- **BERTopic**: 基于 BERT 的主题建模

### 数据服务

- **Crunchbase**: 公司融资和竞品数据
- **Sensor Tower**: 移动应用市场数据
- **SimilarWeb**: 网站流量分析
- **Statista**: 行业统计数据

### 中文数据源

- **百度指数**: 搜索趋势
- **微信指数**: 社交媒体热度
- **微博数据中心**: 社交讨论趋势
- **艾瑞咨询**: 行业报告
- **易观分析**: 行业报告

---

## 文档更新记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v0.1 | 2024-01-15 | 初始版本，分析数据需求和来源 |

---

**注意：** 本文档为分析阶段产物，具体代码工具待后续实现。
