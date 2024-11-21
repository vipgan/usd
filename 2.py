import tushare as ts
from datetime import datetime
import pytz
import telebot
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 使用环境变量
TS_TOKEN = os.getenv("API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 初始化 Tushare 和电报机器人
ts.set_token(TS_TOKEN)
pro = ts.pro_api()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# 设置上海时区
shanghai_tz = pytz.timezone('Asia/Shanghai')

# 安全获取第一行数据
def safe_get_first_row(data, source):
    if data is None or data.empty:
        print(f"[DEBUG] {source} 数据为空或不可用，返回值: {data}")
        return None
    print(f"[DEBUG] {source} 获取成功: {data.iloc[0]}")
    return data.iloc[0]

# 格式化消息内容
def format_message(data, label):
    try:
        if data is None or data.empty:
            return f"{label}: 数据缺失"
        if 'close' not in data:
            print(f"[DEBUG] {label} 数据格式不正确: {data}")
            return f"{label}: 数据格式错误"
        # 去掉小数点，仅保留整数部分
        close_value = int(float(data['close']))
        return f"{label}: {close_value}"
    except Exception as e:
        print(f"[DEBUG] {label} 数据处理异常: {e}")
        return f"{label}: 数据处理失败"

# 获取数据并推送
def get_tushare_data():
    try:
        # 获取指数数据
        sse_index = safe_get_first_row(pro.index_daily(ts_code='000001.SH'), "上证指数")
        szse_index = safe_get_first_row(pro.index_daily(ts_code='399001.SZ'), "深证指数")
        
        # 获取股票和 ETF 数据
        boe_stock = safe_get_first_row(pro.daily(ts_code='000725.SZ'), "京东方A")
        east_money_stock = safe_get_first_row(pro.daily(ts_code='300059.SZ'), "东方财富")
        gold_etf = safe_get_first_row(pro.daily(ts_code='518800.SH'), "黄金ETF")
        hs300_etf = safe_get_first_row(pro.daily(ts_code='510300.SH'), "沪深300ETF")
        pharma_etf = safe_get_first_row(pro.daily(ts_code='512660.SH'), "军工ETF")
    except Exception as e:
        print(f"[ERROR] 数据获取失败: {e}")
        return
    
    # 获取上海时间
    shanghai_time = datetime.now(shanghai_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成消息内容
    message = "\n".join([
        format_message(sse_index, "上证指数"),
        format_message(szse_index, "深证指数"),
        format_message(boe_stock, "京东方A"),
        format_message(east_money_stock, "东方财富"),
        format_message(gold_etf, "黄金ETF"),
        format_message(hs300_etf, "沪深300ETF"),
        format_message(pharma_etf, "军工ETF"),
        f"数据获取时间: {shanghai_time}"
    ])
    
    # 若数据全部缺失，提示统一信息
    if all(["数据缺失" in msg for msg in message.split("\n")[:-1]]):
        message = f"今日所有数据获取失败，请检查数据源。获取时间: {shanghai_time}"

    # 推送消息
    try:
        bot.send_message(CHAT_ID, message)
        print("[INFO] 消息发送成功")
    except telebot.apihelper.ApiException as e:
        print(f"[ERROR] 消息发送失败，API 错误: {e}")
    except Exception as e:
        print(f"[ERROR] 消息发送失败，未知错误: {e}")

if __name__ == "__main__":
    get_tushare_data()
