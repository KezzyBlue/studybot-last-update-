from datetime import datetime, timedelta
import asyncio

async def schedule_task(delay, callback, *args, **kwargs):
    """Hỗ trợ lập lịch chạy một tác vụ sau một khoảng thời gian."""
    await asyncio.sleep(delay)
    await callback(*args, **kwargs)