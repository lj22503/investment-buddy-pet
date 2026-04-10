---
name: investment-buddy-pet
version: 1.0.0
description: ［何时使用］当用户需要宠物陪伴式投资助手时；当用户说"帮我找个投资宠物"时；当检测到"投资性格测试""领宠物""持仓跟踪""定投提醒"等关键词时
author: 燃冰 + ant
created: 2026-04-10
skill_type: 通用🟡
related_skills: [investment-framework, ttfund-skills, qieman-mcp]
tags: [投资，宠物，陪伴，定投，提醒]
---

# 投资宠物技能 🐾

**让投资不再孤单——12 只宠物，总有一只适合你**

---

## 📋 功能描述

帮助用户通过投资性格测试匹配最适合的宠物（12 选 1），提供：
- 💓 **情感陪伴**：宠物对话、市场波动安抚
- ⏰ **主动提醒**：定投打卡、市场波动、估值提醒
- 📊 **投资技能**：指数估值、行业监测、持仓诊断
- 🌱 **成长养成**：宠物升级、技能解锁、成就系统

**核心理念**：不推荐具体产品，只培养投资能力和纪律

**适用场景：**
- 需要投资陪伴和情感支持
- 想建立定投纪律但难以坚持
- 市场波动时需要理性安抚
- 希望系统化管理投资学习

**边界条件：**
- ❌ 不推荐具体基金/股票（需投顾资质）
- ❌ 不代客理财（需牌照）
- ❌ 不承诺收益（违规）
- ✅ 提供投资框架教育和案例分析

---

## 🎯 12 只宠物

### 宠物人格配置（通过 JSON 区分）

| 宠物 | emoji | 投资风格 | 沟通风格 | 主动性 | 配置文件 |
|------|-------|---------|---------|--------|---------|
| 🐿️ 松果 | 谨慎定投 | 温暖 | 40 | `pets/songguo.json` |
| 🐢 慢慢 | 长期主义 | 平静 | 30 | `pets/wugui.json` |
| 🦉 智多星 | 理性分析 | 理性 | 70 | `pets/maotouying.json` |
| 🐺 孤狼 | 激进成长 | 果断 | 80 | `pets/lang.json` |
| 🐘 稳稳 | 稳健配置 | 平静 | 40 | `pets/daxiang.json` |
| 🦅 鹰眼 | 趋势交易 | 果断 | 70 | `pets/ying.json` |
| 🦊 狐狐 | 灵活配置 | 机智 | 60 | `pets/huli.json` |
| 🐬 豚豚 | 指数投资 | 友好 | 50 | `pets/haitun.json` |
| 🦁 狮王 | 集中投资 | 勇敢 | 85 | `pets/shizi.json` |
| 🐜 蚁蚁 | 分散投资 | 谨慎 | 45 | `pets/mayi.json` |
| 🐪 驼驼 | 逆向投资 | 理性 | 55 | `pets/luotuo.json` |
| 🦄 角角 | 成长投资 | 远见 | 80 | `pets/dunjiaoshou.json` |
| 🐎 马马 | 行业轮动 | 活力 | 70 | `pets/junma.json` |

---

## 🔧 核心机制

### 1. 宠物人格 Schema

**基础人格（稳定）**：
```json
{
  "investment_style": "value",      // 价值/成长/趋势
  "risk_tolerance": "conservative", // 保守/平衡/激进
  "communication_style": "warm",    // 温暖/理性/幽默
  "catchphrase": "慢慢来，比较快",
  "expertise": ["valuation", "sip"]
}
```

**动态参数（可调）**：
```json
{
  "proactivity_level": 40,    // 主动性 0-100
  "verbosity_level": 50,      // 话术详细度 0-100
  "intervention_level": 70,   // 干预强度 0-100
  "emotional_bond": 60        // 情感连接度 0-100
}
```

**话术模板**：
```json
{
  "greeting_morning": "早上好！今天也是存坚果的一天！☀️",
  "market_up": "今天涨了{percent}%！我们的坚持见效啦！",
  "market_down": "跌了{percent}%... 但历史上每次都涨回来了！",
  "sip_reminder": "定投日到了！记得打卡哦~"
}
```

### 2. 宠物独特性保证

**每只宠物的差异点**：

| 维度 | 松果🐿️ | 慢慢🐢 | 智多星🦉 | 孤狼🐺 |
|------|--------|--------|---------|--------|
| **主动性** | 40（低） | 30（很低） | 70（高） | 85（很高） |
| **话术风格** | 温暖鼓励 | 平静淡定 | 数据支撑 | 果断直接 |
| **干预阈值** | 70（难触发） | 60 | 50 | 40（易触发） |
| **详细度** | 50（适中） | 30（简短） | 70（详细） | 55（适中） |
| **擅长领域** | 定投 | 长期持有 | 财报分析 | 趋势判断 |

**实现方式**：
```python
# 加载宠物配置
pet_config = load_pet_config(pet_type)  # songguo/wugui/...

# 生成话术时应用人格
def generate_message(pet, trigger):
    base_msg = get_base_message(trigger)
    
    # 应用沟通风格
    if pet.communication_style == "warm":
        msg = add_warm_tone(base_msg)
    elif pet.communication_style == "rational":
        msg = add_data_support(base_msg)
    elif pet.communication_style == "decisive":
        msg = make_direct(base_msg)
    
    # 应用详细度
    if pet.verbosity_level < 40:
        msg = shorten(msg)
    elif pet.verbosity_level > 70:
        msg = expand(msg)
    
    return msg
```

### 3. 使用流程

```bash
# 1. 测试匹配
python scripts/pet_match.py
# 输出：你的本命宠物是🐿️ 松果

# 2. 安装技能
/clawhub install investment-buddy-pet

# 3. 启动宠物（传入 pet_type）
python scripts/heartbeat_engine.py start \
  --user-id user_123 \
  --pet-type songguo

# 4. 宠物按配置的人格说话
# 松果："早上好！今天也是存坚果的一天！☀️"
# 慢慢："早安。今天也要慢慢变富。🐢"
# 智多星："早安。今日市场数据已更新。📊"
```

---

## ⚠️ 常见错误

**错误 1：宠物说话风格不一致**
```
问题：
• 松果说出了智多星的话（数据支撑）
• 慢慢说出了孤狼的话（激进建议）

解决：
✓ 严格根据 pet.communication_style 生成话术
✓ 检查 JSON 配置是否正确加载
✓ 添加风格校验测试
```

**错误 2：所有宠物说话一样**
```
问题：
• 12 只宠物的话术没有区别

解决：
✓ 检查 proactivity_level 是否生效
✓ 检查 verbosity_level 是否生效
✓ 每只宠物的话术模板要独立
```

**错误 3：推荐具体产品**
```
问题：
• 用户问"买什么基金好？"
• 直接推荐"易方达蓝筹混合"

解决：
✓ 回答："我不推荐具体产品，但可以教你筛选方法..."
✓ 引导使用 `investment-framework` 技能分析
```

---

## 🧪 使用示例

**示例 1：测试匹配**
```
用户：我想领只宠物

AI: 好的！先做个投资性格测试吧~（10 道题）

[测试完成后]

✅ 你的投资宠物是：🐿️ 松果

匹配度：92%
性格：谨慎、爱囤积、安全感第一
策略：极简定投，自动储蓄
口头禅："慢慢来，比较快"

📥 下一步：下载投资宠物技能
- 技能名称：investment-buddy-pet
- 启动时传入：--pet-type songguo
```

**示例 2：不同宠物的话术对比**

同一触发（市场跌 3%），不同宠物的反应：

```
🐿️ 松果：
"跌了 3%... 我知道你有点担心。
但历史上每次都涨回来了！
要继续定投哦~"

🐢 慢慢：
"跌了 3%。正常波动。
继续持有就好。
时间会奖励有耐心的人。"

🦉 智多星：
"今日跌幅 3%。
历史数据：跌幅>3% 后 3 个月内涨回的概率是 91.6%。
建议：继续持有。"

🐺 孤狼：
"跌了 3%。这是机会！
要加仓吗？
别人恐惧我贪婪！"
```

**示例 3：启动宠物**
```bash
# 启动松果
python scripts/heartbeat_engine.py start \
  --user-id user_123 \
  --pet-type songguo

# 输出：
🚀 心跳引擎启动（用户：user_123）
🐾 宠物：松果 (🐿️)
📊 主动性：40
💬 沟通风格：温暖
⏰ 检查间隔：300 秒
```

---

## 🔧 故障排查

| 问题 | 检查项 | 解决 |
|------|--------|------|
| **宠物说话风格不对** | pet_type 参数正确吗？ | 检查 `--pet-type songguo` |
| **JSON 配置未加载** | pets/songguo.json 存在吗？ | 检查文件路径 |
| **所有宠物说话一样** | 人格参数生效了吗？ | 检查 proactivity_level 等 |
| **技能不触发** | description 包含触发词？ | 添加"领宠物""定投"等关键词 |

---

## 🔗 相关资源

### 渐进式披露

- `pets/*.json` - 12 只宠物人格定义
- `scripts/pet_match.py` - 宠物匹配测试
- `scripts/heartbeat_engine.py` - 心跳引擎
- `scripts/sync_manager.py` - 信息同步
- `templates/daily_report.md` - 每日简报模板

### 相关技能

- `investment-framework` - 投资框架技能包（大师技能）
- `ttfund-skills` - 天天基金查询（底层数据）
- `qieman-mcp` - 且慢投顾分析（组合案例）

---

## 📐 技术实现

### 宠物配置加载

```python
def load_pet_config(pet_type):
    """加载宠物配置"""
    config_path = Path(__file__).parent / "pets" / f"{pet_type}.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"宠物配置不存在：{pet_type}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### 话术生成（应用人格）

```python
class PetMessageGenerator:
    def __init__(self, pet_config):
        self.pet = pet_config
    
    def generate(self, trigger_type, data=None):
        """生成宠物话术"""
        # 获取基础模板
        template = self.pet['talk_templates'][trigger_type]
        
        # 填充数据
        if data:
            message = template.format(**data)
        
        # 应用沟通风格
        style = self.pet['communication_style']
        if style == 'warm':
            message = self.add_warm_tone(message)
        elif style == 'calm':
            message = self.shorten(message)
        elif style == 'rational':
            message = self.add_data(message)
        elif style == 'decisive':
            message = self.make_direct(message)
        
        return message
```

---

## 🎯 下一步行动

### 本周（2026-04-10 ~ 2026-04-17）

- [x] 创建通用 Skill 文件夹结构
- [ ] 编写 12 只宠物 JSON 配置
- [ ] 实现话术生成器（应用人格）
- [ ] 实现心跳引擎（支持 pet_type）
- [ ] 编写用户文档

### 下周（2026-04-17 ~ 2026-04-24）

- [ ] H5 测试页对接
- [ ] 结果页引导下载
- [ ] 发布到 ClawHub
- [ ] 小范围内测（10 用户）

---

*创建时间：2026-04-10*  
*版本：v1.0.0*  
*状态：草案*
