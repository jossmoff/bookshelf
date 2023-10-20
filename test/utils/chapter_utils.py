from datetime import datetime, timedelta
from typing import Optional

from bookshelf.models import Chapter


def create_chapter_from_delta(delta: timedelta, start_time: Optional[datetime] = None) -> Chapter:
    if start_time is None:
        start_time = datetime.now()
    end_time = start_time + delta
    return Chapter(start_time, end_time)
