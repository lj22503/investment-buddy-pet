# Investment Buddy Pet - 投资宠物技能

**12 只宠物，1 个通用 Skill，通过配置文件区分宠物人格**

---

## 🎯 架构设计

```
investment-buddy-pet/           # 1 个通用 Skill
├── SKILL.md                    # 通用技能文档
├── pets/                       # 12 个宠物配置文件
│   ├── songguo.json           # 🐿️ 松果
│   ├── wugui.json             # 🐢 慢慢
│   ├── maotouying.json        # 🦉 智多星
│   └── ... (12 个)
├── scripts/                    # 通用脚本
│   ├── pet_match.py           # 宠物匹配测试
│   ├── heartbeat_engine.py    # 心跳引擎（支持 pet_type）
│   ├── sync_manager.py        # 同步管理
│   └── viral_growth.py        # 病毒传播
├── templates/                  # 模板
├── data/                       # 用户数据
└── assets/                     # 素材
```

---

## 🐾 12 只宠物

| 宠物 | emoji | 投资风格 | 沟通风格 | 主动性 | 适合人群 |
|------|-------|---------|---------|--------|---------|
| 🐿️ 松果 | 谨慎定投 | 温暖 | 40 | 保守型新手 |
| 🐢 慢慢 | 长期主义 | 平静 | 30 | 超长期投资者 |
| 🦉 智多星 | 理性分析 | 理性 | 70 | 理性分析派 |
| 🐺 孤狼 | 激进成长 | 果断 | 85 | 追求高收益 |
| 🐘 稳稳 | 稳健配置 | 平静 | 40 | 平衡型投资者 |
| 🦅 鹰眼 | 趋势交易 | 果断 | 70 | 趋势交易者 |
| 🦊 狐狐 | 灵活配置 | 机智 | 60 | 资产配置者 |
| 🐬 豚豚 | 指数投资 | 友好 | 50 | 被动投资者 |
| 🦁 狮王 | 集中投资 | 勇敢 | 85 | 集中持仓者 |
| 🐜 蚁蚁 | 分散投资 | 谨慎 | 45 | 风险厌恶者 |
| 🐪 驼驼 | 逆向投资 | 理性 | 55 | 逆向投资者 |
| 🦄 角角 | 成长投资 | 远见 | 80 | 科技成长派 |
| 🐎 马马 | 行业轮动 | 活力 | 70 | 行业轮动者 |

---

## 🚀 快速开始

### 方式 1：ClawHub 安装

```bash
/clawhub install investment-buddy-pet
```

### 方式 2：Git 安装

```bash
git clone https://github.com/lj22503/investment-buddy-pet.git
cd investment-buddy-pet
pip install -r requirements.txt
```

### 启动宠物

```bash
# 测试匹配
python scripts/pet_match.py
# 输出：你的本命宠物是🐿️ 松果

# 启动松果
python scripts/heartbeat_engine.py start \
  --user-id user_123 \
  --pet-type songguo

# 启动慢慢
python scripts/heartbeat_engine.py start \
  --user-id user_123 \
  --pet-type wugui
```

---

## 🎮 用户流程

```
H5 测试页（mangofolio.vercel.app）
    ↓
10 道测试题
    ↓
匹配结果：🐿️ 松果（92%）
    ↓
引导下载：investment-buddy-pet
    ↓
安装技能
    ↓
启动：--pet-type songguo
    ↓
松果开始陪伴
```

---

## 🔧 宠物独特性保证

### 1. 人格参数差异

```json
// 松果 (songguo.json)
{
  "proactivity_level": 40,    // 低主动性
  "communication_style": "warm",  // 温暖风格
  "verbosity_level": 50,      // 适中详细度
  "intervention_level": 70    // 难触发干预
}

// 慢慢 (wugui.json)
{
  "proactivity_level": 30,    // 很低主动性
  "communication_style": "calm",  // 平静风格
  "verbosity_level": 30,      // 简短
  "intervention_level": 60
}

// 智多星 (maotouying.json)
{
  "proactivity_level": 70,    // 高主动性
  "communication_style": "rational",  // 理性风格
  "verbosity_level": 70,      // 详细
  "intervention_level": 50
}
```

### 2. 话术模板差异

```json
// 松果的话术
{
  "greeting_morning": "早上好！今天也是存坚果的一天！☀️",
  "market_down": "跌了{percent}%... 我知道你有点担心。但历史上每次都涨回来了！"
}

// 慢慢的话术
{
  "greeting_morning": "早安。今天也要慢慢变富。🐢",
  "market_down": "跌了{percent}%。正常波动，继续持有就好。"
}

// 智多星的话术
{
  "greeting_morning": "早安。今日市场数据已更新，请查看。📊",
  "market_down": "今日跌幅{percent}%。历史数据：{history_data}"
}
```

### 3. 话术生成器（应用人格）

```python
class PetMessageGenerator:
    def __init__(self, pet_config):
        self.pet = pet_config
    
    def generate(self, trigger_type, data=None):
        # 获取基础模板
        template = self.pet['talk_templates'][trigger_type]
        
        # 填充数据
        message = template.format(**data) if data else template
        
        # 应用沟通风格
        style = self.pet['communication_style']
        if style == 'warm':
            message = self.add_warm_tone(message)
        elif style == 'calm':
            message = self.shorten(message)
        elif style == 'rational':
            message = self.add_data_support(message)
        elif style == 'decisive':
            message = self.make_direct(message)
        
        # 应用详细度
        verbosity = self.pet['verbosity_level']
        if verbosity < 40:
            message = self.shorten(message)
        elif verbosity > 70:
            message = self.expand(message)
        
        return message
```

---

## 📊 完成状态

| 模块 | 状态 | 说明 |
|------|------|------|
| SKILL.md | ✅ 完成 | 通用技能文档 |
| 12 个宠物 JSON | ✅ 完成 | 人格配置文件 |
| pet_match.py | ✅ 完成 | 测试匹配脚本 |
| heartbeat_engine.py | ✅ 完成 | 心跳引擎（支持 pet_type） |
| sync_manager.py | ✅ 完成 | 同步管理 |
| viral_growth.py | ✅ 完成 | 病毒传播 |
| H5 对接 | ⏳ 待开始 | 结果页引导下载 |
| ClawHub 发布 | ⏳ 待开始 | 上架技能 |

---

## 📁 文件结构

```
investment-buddy-pet/
├── SKILL.md                    ✅ 通用技能文档
├── README.md                   ✅ 使用说明
├── pets/                       ✅ 12 个宠物配置
│   ├── songguo.json
│   ├── wugui.json
│   ├── maotouying.json
│   ├── lang.json
│   ├── daxiang.json
│   ├── ying.json
│   ├── huli.json
│   ├── haitun.json
│   ├── shizi.json
│   ├── mayi.json
│   ├── luotuo.json
│   ├── dunjiaoshou.json
│   └── junma.json
├── scripts/                    ✅ 4 个核心脚本
│   ├── pet_match.py
│   ├── heartbeat_engine.py
│   ├── sync_manager.py
│   └── viral_growth.py
├── templates/                  📁 目录
├── data/                       📁 目录
└── assets/                     📁 目录
```

---

## 🔗 相关项目

| 项目 | 说明 |
|------|------|
| `mangofolio-h5` | H5 测试页（引流入口） |
| `investment-buddy` | 原始宠物系统设计 |
| `investment-framework-skill` | 投资框架技能（大师技能） |
| `ttfund-skills` | 天天基金数据 |
| `qieman-mcp` | 且慢投顾策略 |

---

**创建时间**：2026-04-10  
**版本**：v1.0.0  
**架构**：1 个通用 Skill + 12 个宠物配置
