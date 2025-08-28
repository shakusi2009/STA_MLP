from datetime import datetime
import pytz  # 需安装pytz库（pip install pytz）


def time_convert(utc_time_str):
    # 输入的UTC时间字符串（Z表示UTC时区）
    # utc_time_str = "2025-08-27T04:35:18Z"

    # 步骤1：解析UTC时间字符串为datetime对象（带UTC时区信息）
    # 注意：Python 3.11+的fromisoformat可直接处理'Z'，低版本需替换为'+00:00'
    utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))

    # 步骤2：指定UTC时区
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    # 步骤3：转换为北京时间（Asia/Shanghai时区，UTC+8）
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = utc_time.astimezone(beijing_tz)

    # 步骤4：格式化输出（可选，按需要调整格式）
    beijing_time_str = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

    # print(f"北京时间: {beijing_time_str}")

    return beijing_time_str
