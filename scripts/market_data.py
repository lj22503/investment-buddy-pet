#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场数据获取脚本

**数据源**：
- 新浪财经：http://hq.sinajs.cn/（实时行情）
- 东方财富：https://push2.eastmoney.com/（大盘指数、个股行情）
- 天天基金：http://fund.eastmoney.com/（基金净值）

**使用示例**：
```python
from market_data import get_index_quotes, get_stock_quote, get_fund_nav

# 获取大盘指数
quotes = get_index_quotes(['000001.SZ', '399001.SZ', '399006.SZ'])
print(quotes)

# 获取个股行情
quote = get_stock_quote('600519.SZ')
print(quote)

# 获取基金净值
nav = get_fund_nav('510300')
print(nav)
```
"""

import requests
import re
from datetime import datetime
from typing import Dict, List, Optional


class MarketDataFetcher:
    """市场数据获取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}  # 简单缓存
        self.cache_time = {}  # 缓存时间
    
    def get_index_quotes(self, index_codes: List[str]) -> Dict:
        """
        获取指数行情
        
        Args:
            index_codes: 指数代码列表
                - 000001.SZ: 上证指数
                - 399001.SZ: 深证成指
                - 399006.SZ: 创业板指
                - 000300.SZ: 沪深 300
        
        Returns:
            {
                "000001.SZ": {
                    "name": "上证指数",
                    "current": 3050.50,
                    "change_percent": -1.2,
                    "change": -37.00,
                    "high": 3080.00,
                    "low": 3040.00,
                    "volume": 125000000,
                    "turnover": 15000000000,
                    "updated_at": "2026-04-14T15:00:00Z"
                }
            }
        """
        results = {}
        
        for code in index_codes:
            # 检查缓存（1 分钟内）
            if code in self.cache and (datetime.now() - self.cache_time[code]).seconds < 60:
                results[code] = self.cache[code]
                continue
            
            # 新浪财经 API
            url = f"http://hq.sinajs.cn/list={code.replace('.', '')}"
            try:
                resp = self.session.get(url, timeout=5)
                resp.raise_for_status()
                
                # 解析数据
                # 格式：var hq_str_sh000001="名称，当前，开盘，昨收，最高，最低，..."
                match = re.search(r'="([^"]+)"', resp.text)
                if match:
                    data = match.group(1).split(',')
                    
                    quote = {
                        "name": data[0],
                        "current": float(data[1]) if data[1] else 0,
                        "open": float(data[2]) if data[2] else 0,
                        "prev_close": float(data[3]) if data[3] else 0,
                        "high": float(data[4]) if data[4] else 0,
                        "low": float(data[5]) if data[5] else 0,
                        "change": float(data[1]) - float(data[3]) if data[1] and data[3] else 0,
                        "change_percent": ((float(data[1]) - float(data[3])) / float(data[3]) * 100) if data[3] else 0,
                        "volume": float(data[6]) if len(data) > 6 and data[6] else 0,
                        "turnover": float(data[7]) if len(data) > 7 and data[7] else 0,
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    # 缓存
                    self.cache[code] = quote
                    self.cache_time[code] = datetime.now()
                    
                    results[code] = quote
            except Exception as e:
                print(f"获取指数 {code} 失败：{e}")
                # 返回缓存或空数据
                if code in self.cache:
                    results[code] = self.cache[code]
                else:
                    results[code] = {"name": code, "current": 0, "change_percent": 0}
        
        return results
    
    def get_stock_quote(self, stock_code: str) -> Dict:
        """
        获取个股行情
        
        Args:
            stock_code: 股票代码（如 600519.SZ）
        
        Returns:
            {
                "code": "600519.SZ",
                "name": "贵州茅台",
                "current": 1850.00,
                "change_percent": 2.5,
                "pe": 30.5,
                "pb": 8.2,
                "market_cap": 2300000000000,
                "updated_at": "2026-04-14T15:00:00Z"
            }
        """
        # 检查缓存
        if stock_code in self.cache and (datetime.now() - self.cache_time[stock_code]).seconds < 60:
            return self.cache[stock_code]
        
        # 新浪财经 API
        url = f"http://hq.sinajs.cn/list={stock_code.replace('.', '')}"
        try:
            resp = self.session.get(url, timeout=5)
            resp.raise_for_status()
            
            match = re.search(r'="([^"]+)"', resp.text)
            if match:
                data = match.group(1).split(',')
                
                quote = {
                    "code": stock_code,
                    "name": data[0],
                    "current": float(data[1]) if data[1] else 0,
                    "open": float(data[2]) if data[2] else 0,
                    "prev_close": float(data[3]) if data[3] else 0,
                    "high": float(data[4]) if data[4] else 0,
                    "low": float(data[5]) if data[5] else 0,
                    "change": float(data[1]) - float(data[3]) if data[1] and data[3] else 0,
                    "change_percent": ((float(data[1]) - float(data[3])) / float(data[3]) * 100) if data[3] else 0,
                    "volume": float(data[6]) if len(data) > 6 and data[6] else 0,
                    "turnover": float(data[7]) if len(data) > 7 and data[7] else 0,
                    # 以下字段需要从其他 API 获取
                    "pe": 0,  # 需要东方财富 API
                    "pb": 0,
                    "market_cap": 0,
                    "updated_at": datetime.now().isoformat()
                }
                
                self.cache[stock_code] = quote
                self.cache_time[stock_code] = datetime.now()
                
                return quote
        except Exception as e:
            print(f"获取个股 {stock_code} 失败：{e}")
        
        return {"code": stock_code, "name": "", "current": 0, "change_percent": 0}
    
    def get_fund_nav(self, fund_code: str) -> Dict:
        """
        获取基金净值
        
        Args:
            fund_code: 基金代码（如 510300）
        
        Returns:
            {
                "code": "510300",
                "name": "沪深 300ETF",
                "nav": 4.35,
                "nav_date": "2026-04-14",
                "change_percent": 0.8,
                "updated_at": "2026-04-14T15:00:00Z"
            }
        """
        # 检查缓存（24 小时）
        if fund_code in self.cache and (datetime.now() - self.cache_time[fund_code]).seconds < 86400:
            return self.cache[fund_code]
        
        # 天天基金 API
        url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
        try:
            resp = self.session.get(url, timeout=5)
            resp.raise_for_status()
            
            # 解析 JS 数据（简化版）
            # 实际应该解析 fS_jjzl 等字段
            nav = 0
            nav_date = ""
            change_percent = 0
            
            # 从 HTML 中提取净值
            match = re.search(r'Data_netValue growth="([^"]+)"', resp.text)
            if match:
                nav = float(match.group(1))
            
            fund_info = {
                "code": fund_code,
                "name": "",  # 需要从其他字段提取
                "nav": nav,
                "nav_date": nav_date,
                "change_percent": change_percent,
                "updated_at": datetime.now().isoformat()
            }
            
            self.cache[fund_code] = fund_info
            self.cache_time[fund_code] = datetime.now()
            
            return fund_info
        except Exception as e:
            print(f"获取基金 {fund_code} 净值失败：{e}")
        
        return {"code": fund_code, "name": "", "nav": 0, "change_percent": 0}
    
    def get_market_brief(self) -> str:
        """
        获取市场简报（用于宠物消息）
        
        Returns:
            "沪深 300 +0.5%，上证指数 -1.2%，创业板指 +2.3%"
        """
        quotes = self.get_index_quotes(['000300.SZ', '000001.SZ', '399006.SZ'])
        
        parts = []
        for code, quote in quotes.items():
            name = quote.get('name', code)
            change = quote.get('change_percent', 0)
            sign = '+' if change >= 0 else ''
            parts.append(f"{name} {sign}{change:.1f}%")
        
        return "，".join(parts)


# 快捷函数
_market_fetcher = MarketDataFetcher()

def get_index_quotes(index_codes: List[str]) -> Dict:
    return _market_fetcher.get_index_quotes(index_codes)

def get_stock_quote(stock_code: str) -> Dict:
    return _market_fetcher.get_stock_quote(stock_code)

def get_fund_nav(fund_code: str) -> Dict:
    return _market_fetcher.get_fund_nav(fund_code)

def get_market_brief() -> str:
    return _market_fetcher.get_market_brief()


if __name__ == '__main__':
    # 测试
    print("测试市场数据获取...")
    
    # 获取大盘指数
    quotes = get_index_quotes(['000001.SZ', '399001.SZ', '399006.SZ'])
    print("\n大盘指数:")
    for code, quote in quotes.items():
        print(f"  {quote['name']}: {quote['current']} ({quote['change_percent']:+.2f}%)")
    
    # 获取市场简报
    brief = get_market_brief()
    print(f"\n市场简报：{brief}")
