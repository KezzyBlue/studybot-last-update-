import re
from datetime import datetime

def validate_date(date_str, format="%d-%m-%Y %H:%M"):
    """Kiểm tra định dạng ngày tháng."""
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        return None

def format_duration(seconds):
    """Chuyển đổi số giây thành chuỗi dạng giờ, phút, giây."""
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours} giờ {minutes} phút {seconds} giây"