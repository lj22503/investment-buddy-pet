#!/usr/bin/env python3
"""
心跳引擎 - 主动提醒系统
定期检查市场/用户状态，触发宠物主动提醒
"""

import json
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import requests

class HeartbeatEngine:
    """心跳引擎"""
    
    def __init__(self, user_id, db_path=None):
        self.user_id = user_id
        self.db_path = db_path or Path(__file__).parent.parent / "data" / "pet_data.db"
        self.config = self.load_config()
        self.pet = self.load_pet()
        self.init_db()
    
    def load_config(self):
        """加载配置"""
        return {
            "heartbeat_interval": 300,  # 5 分钟检查一次
            "market_check_url": "http://qt.gtimg.cn/q=s_sh000001,s_sz399001",
            "notification_channels": ["local", "email"],  # 本地通知/邮件
            "quiet_hours": {"start": 22, "end": 8}  # 安静时间（22:00-8:00）
        }
    
    def load_pet(self):
        """加载宠物信息"""
        # 从数据库读取用户宠物
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT pet_type FROM pets WHERE user_id = ?",
            (self.user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        pet_type = result[0]
        pet_path = Path(__file__).parent.parent / "pets" / f"{pet_type}.json"
        
        if pet_path.exists():
            with open(pet_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建提醒记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                trigger_type TEXT,
                message TEXT,
                priority TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT FALSE
            )
        """)
        
        conn.commit()
        conn.close()
    
    def check_market(self):
        """检查市场状态"""
        try:
            response = requests.get(self.config["market_check_url"], timeout=5)
            data = response.text
            
            # 解析腾讯 API 返回（非 JSON 格式）
            # 格式：v_s_sh000001="51~上证指数~3052.14~..."
            parts = data.split('~')
            if len(parts) > 3:
                current_price = float(parts[3])
                # 计算涨跌幅（需要昨日收盘价，简化处理）
                change_percent = float(parts[32]) if len(parts) > 32 else 0
                
                return {
                    "index": "上证指数",
                    "price": current_price,
                    "change_percent": change_percent,
                    "timestamp": datetime.now()
                }
        except Exception as e:
            print(f"市场数据获取失败：{e}")
        
        return None
    
    def check_user_status(self):
        """检查用户状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查定投日
        cursor.execute(
            "SELECT sip_day FROM users WHERE id = ?",
            (self.user_id,)
        )
        result = cursor.fetchone()
        sip_day = result[0] if result else None
        
        today = datetime.now().day
        is_sip_day = (sip_day == today) if sip_day else False
        
        # 检查最近互动时间
        cursor.execute(
            "SELECT MAX(created_at) FROM interactions WHERE user_id = ?",
            (self.user_id,)
        )
        last_interaction = cursor.fetchone()[0]
        
        days_since_interaction = None
        if last_interaction:
            last_dt = datetime.fromisoformat(last_interaction)
            days_since_interaction = (datetime.now() - last_dt).days
        
        conn.close()
        
        return {
            "is_sip_day": is_sip_day,
            "last_interaction_days": days_since_interaction
        }
    
    def is_quiet_hours(self):
        """检查是否在安静时间"""
        current_hour = datetime.now().hour
        quiet_start = self.config["quiet_hours"]["start"]
        quiet_end = self.config["quiet_hours"]["end"]
        
        if quiet_start > quiet_end:  # 跨天情况（如 22:00-8:00）
            return current_hour >= quiet_start or current_hour < quiet_end
        else:
            return quiet_start <= current_hour < quiet_end
    
    def generate_trigger(self, market_data, user_status):
        """生成触发"""
        triggers = []
        
        if not self.pet:
            return triggers
        
        # 1. 市场波动触发
        if market_data:
            change = market_data["change_percent"]
            
            if change < -5 and self.pet["personality_traits"]["intervention_level"] > 50:
                triggers.append({
                    "type": "market_drop",
                    "priority": "high",
                    "message": f"主人，今天跌了{change}%... 我知道你有点担心。但历史上每次都涨回来了！",
                    "pet_id": self.pet["pet_id"]
                })
            elif change > 5 and self.pet["personality_traits"]["proactivity_level"] > 60:
                triggers.append({
                    "type": "market_rise",
                    "priority": "medium",
                    "message": f"今天涨了{change}%！我们的坚持见效啦！🎉",
                    "pet_id": self.pet["pet_id"]
                })
        
        # 2. 定投日触发
        if user_status["is_sip_day"] and self.pet["personality_traits"]["proactivity_level"] > 60:
            triggers.append({
                "type": "sip_reminder",
                "priority": "medium",
                "message": "定投日到了！记得打卡哦~ 我已经准备好存坚果啦！🌰",
                "pet_id": self.pet["pet_id"]
            })
        
        # 3. 长时间未互动触发
        if user_status["last_interaction_days"] and user_status["last_interaction_days"] > 7:
            triggers.append({
                "type": "inactive_reminder",
                "priority": "low",
                "message": "主人，好久不见！我有点想你了... 来看看最近的市场吧？",
                "pet_id": self.pet["pet_id"]
            })
        
        return triggers
    
    def send_notification(self, trigger):
        """发送通知"""
        # 检查安静时间
        if self.is_quiet_hours() and trigger["priority"] == "low":
            print(f"安静时间，跳过低优先级通知：{trigger['type']}")
            return False
        
        # 保存到数据库
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO notifications 
               (user_id, trigger_type, message, priority) 
               VALUES (?, ?, ?, ?)""",
            (self.user_id, trigger["type"], trigger["message"], trigger["priority"])
        )
        
        conn.commit()
        conn.close()
        
        # 打印通知（实际应推送到用户设备）
        print(f"\n🔔 [{trigger['priority'].upper()}] {trigger['pet_id']}: {trigger['message']}")
        
        return True
    
    def tick(self):
        """执行一次心跳检查"""
        print(f"\n[{datetime.now().isoformat()}] 心跳检查...")
        
        # 1. 检查市场
        market_data = self.check_market()
        if market_data:
            print(f"市场：{market_data['index']} {market_data['price']} ({market_data['change_percent']}%)")
        
        # 2. 检查用户状态
        user_status = self.check_user_status()
        print(f"用户状态：定投日={user_status['is_sip_day']}, 最近互动={user_status['last_interaction_days']}天前")
        
        # 3. 生成触发
        triggers = self.generate_trigger(market_data, user_status)
        
        # 4. 发送通知
        for trigger in triggers:
            self.send_notification(trigger)
        
        return triggers
    
    def start(self):
        """启动心跳引擎"""
        print(f"🚀 心跳引擎启动（用户：{self.user_id}）")
        print(f"宠物：{self.pet['name'] if self.pet else '未加载'}")
        print(f"检查间隔：{self.config['heartbeat_interval']}秒")
        print(f"安静时间：{self.config['quiet_hours']['start']}:00 - {self.config['quiet_hours']['end']}:00")
        
        try:
            while True:
                self.tick()
                time.sleep(self.config["heartbeat_interval"])
        except KeyboardInterrupt:
            print("\n⏹️ 心跳引擎停止")


def main():
    """测试心跳引擎"""
    import argparse
    
    parser = argparse.ArgumentParser(description="心跳引擎 - 主动提醒系统")
    parser.add_argument("--user-id", required=True, help="用户 ID")
    parser.add_argument("--once", action="store_true", help="只执行一次（测试用）")
    
    args = parser.parse_args()
    
    engine = HeartbeatEngine(user_id=args.user_id)
    
    if args.once:
        # 只执行一次
        engine.tick()
    else:
        # 持续运行
        engine.start()


if __name__ == "__main__":
    main()
