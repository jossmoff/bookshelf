from datetime import datetime, timedelta
from typing import Optional

from bookshelf.models import Chapter, Story
from .chapter_utils import create_chapter_from_delta


def create_test_story_dict(name: Optional[str] = None,
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None,
                           chapters: Optional[list[Chapter]] = None,
                           tags: Optional[list[str]] = None) -> dict:
    if name is None:
        name = 'TEST_TASK'
    if start_date is None:
        start_date = datetime.now()
    if end_date is None:
        end_date = datetime.now() + timedelta(hours=3)
    if chapters is None:
        chapters = [
            create_chapter_from_delta(timedelta(hours=1)),
            create_chapter_from_delta(timedelta(hours=1)),
            create_chapter_from_delta(timedelta(hours=1))
        ]
    if tags is None:
        tags = ['tag1', 'tag2']
    return {
        'name': name,
        'start_date': start_date,
        'end_date': end_date,
        'chapters': chapters,
        'tags': tags
    }


def create_test_story(name: Optional[str] = None,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      chapters: Optional[list[Chapter]] = None,
                      tags: Optional[list[str]] = None) -> Story:
    return Story(**create_test_story_dict(name, start_date, end_date, chapters, tags))


def create_story_json_string(name: str, start_date: datetime, end_date: Optional[datetime] = None,
                             chapters: Optional[list[Chapter]] = None,
                             tags: Optional[list[str]] = None) -> str:
    if chapters is None:
        chapters = []
    if tags is None:
        tags = []
    return str({
        'name': name,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat() if end_date else None,
        'tags': tags,
        'chapters': [chapter.to_json() for chapter in chapters]
    }).replace('\'', '"')
