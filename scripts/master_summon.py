#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大师召唤脚本 - 召唤投资大师提供建议

使用方法:
    python master_summon.py --user-id user_001 --pet-type songguo --master buffett --question "现在能买贵州茅台吗？"
"""

import argparse
import json
import random
from pathlib import Path
from datetime import datetime


class MasterSummoner:
    """大师召唤器"""
    
    def __init__(self, masters_dir: str = "masters"):
        self.masters_dir = Path(masters_dir)
        self.masters = self._load_masters()
    
    def _load_masters(self) -> dict:
        """加载所有大师配置"""
        masters = {}
        for file in self.masters_dir.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                master = json.load(f)
                masters[master['master_id']] = master
        return masters
    
    def list_masters(self) -> list:
        """列出所有可用大师"""
        return [
            {
                "id": m['master_id'],
                "name": m['name'],
                "emoji": m['emoji'],
                "philosophy": m['investment_philosophy']
            }
            for m in self.masters.values()
        ]
    
    def get_master(self, master_id: str) -> dict:
        """获取大师配置"""
        if master_id not in self.masters:
            raise ValueError(f"未知的大师：{master_id}")
        return self.masters[master_id]
    
    def generate_advice(self, master_id: str, question: str, context: dict = None) -> dict:
        """
        生成大师建议
        
        Args:
            master_id: 大师 ID
            question: 用户问题
            context: 上下文（用户画像、持仓等）
        
        Returns:
            {
                "master": {...},
                "advice": {...},
                "pet_supplement": {...}
            }
        """
        master = self.get_master(master_id)
        
        # 选择最相关的 2-3 条核心原则
        principles = master['core_principles']
        selected_principles = random.sample(principles, min(3, len(principles)))
        
        # 生成建议内容
        advice_content = self._generate_advice_content(master, question, context)
        
        # 生成宠物补充建议
        pet_supplement = self._generate_pet_supplement(master, context)
        
        return {
            "status": "success",
            "master": {
                "id": master['master_id'],
                "name": master['name'],
                "emoji": master['emoji']
            },
            "advice": {
                "principles": selected_principles,
                "content": advice_content,
                "confidence": 0.85,
                "risk_warning": self._generate_risk_warning(question, context)
            },
            "pet_supplement": pet_supplement,
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_advice_content(self, master: dict, question: str, context: dict) -> str:
        """生成大师建议内容（简化版，实际应该调用 LLM）"""
        master_name = master['name']
        greeting = master['talk_templates']['greeting']
        suffix = master['talk_templates']['advice_suffix']
        
        # 根据大师类型生成不同风格的建议
        if master['master_id'] == 'buffett':
            content = f"{master_name}认为，投资的关键是理解你所投资的东西。"
            content += "如果这是一家好公司，并且价格合理，那么长期持有是明智的选择。"
        elif master['master_id'] == 'dalio':
            content = f"{master_name}建议从系统角度思考这个问题。"
            content += "考虑经济周期、资产配置和风险分散，而不是单一决策。"
        elif master['master_id'] == 'lynch':
            content = f"{master_name}会说：从你了解的领域开始。"
            content += "如果你能理解这个公司的业务，并且它在你生活中随处可见，那可能是个好机会。"
        else:
            content = f"{master_name}的建议是：深入分析，谨慎决策。"
        
        return f"{greeting}\n\n{content}\n\n{suffix}"
    
    def _generate_pet_supplement(self, master: dict, context: dict) -> dict:
        """生成宠物补充建议"""
        pet_type = context.get('pet_type', 'songguo') if context else 'songguo'
        user_profile = context.get('user_profile', {}) if context else {}
        
        risk_tolerance = user_profile.get('risk_tolerance', 'balanced')
        
        # 根据用户风险偏好生成补充建议
        if risk_tolerance == 'conservative':
            supplement_text = "大师的建议很有智慧！结合你的保守型风格，我建议先用小仓位（5-10%）尝试，用定投方式分批建仓。"
        elif risk_tolerance == 'aggressive':
            supplement_text = "大师的建议很有智慧！结合你的进取型风格，可以在控制仓位的前提下更积极地执行。"
        else:
            supplement_text = "大师的建议很有智慧！结合你的平衡型风格，建议适度配置，动态调整。"
        
        return {
            "text": supplement_text,
            "action_suggestion": "create_sip_plan" if risk_tolerance == 'conservative' else "monitor_position"
        }
    
    def _generate_risk_warning(self, question: str, context: dict) -> str:
        """生成风险提示"""
        warnings = [
            "市场有风险，投资需谨慎。",
            "以上建议仅供参考，不构成投资建议。",
            "请根据自身情况独立判断，自行承担风险。",
            "过往表现不代表未来收益。"
        ]
        return random.choice(warnings)


def main():
    parser = argparse.ArgumentParser(description='召唤投资大师')
    parser.add_argument('--user-id', type=str, required=True, help='用户 ID')
    parser.add_argument('--pet-type', type=str, default='songguo', help='宠物类型')
    parser.add_argument('--master', type=str, required=True, help='大师 ID')
    parser.add_argument('--question', type=str, required=True, help='用户问题')
    parser.add_argument('--list-masters', action='store_true', help='列出所有大师')
    
    args = parser.parse_args()
    
    summoner = MasterSummoner()
    
    if args.list_masters:
        masters = summoner.list_masters()
        print("可用大师列表：\n")
        for m in masters:
            print(f"{m['emoji']} {m['name']} - {m['philosophy']}")
        return
    
    # 召唤大师
    context = {
        'user_id': args.user_id,
        'pet_type': args.pet_type,
        'user_profile': {
            'risk_tolerance': 'conservative'  # 示例
        }
    }
    
    result = summoner.generate_advice(args.master, args.question, context)
    
    # 输出结果
    print("\n" + "="*60)
    print(f"{result['master']['emoji']} {result['master']['name']} 的建议")
    print("="*60)
    
    print("\n【核心原则】")
    for i, principle in enumerate(result['advice']['principles'], 1):
        print(f"{i}. {principle}")
    
    print("\n【建议内容】")
    print(result['advice']['content'])
    
    print("\n【风险提示】")
    print(result['advice']['risk_warning'])
    
    print("\n【宠物补充】")
    print(result['pet_supplement']['text'])
    print(f"建议操作：{result['pet_supplement']['action_suggestion']}")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
