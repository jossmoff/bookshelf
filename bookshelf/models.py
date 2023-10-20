from datetime import datetime, timedelta
from typing import Optional, List

from bookshelf.exceptions import ChapterNotInProgressException, StoryAlreadyFinishedException


class Chapter:

    def __init__(self, start_time: datetime, end_time: Optional[datetime] = None):
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time

    def elapsed_time(self) -> timedelta:
        if self.end_time is None:
            return datetime.now() - self.start_time
        return self.end_time - self.start_time

    def in_progress(self) -> bool:
        return self.end_time is None

    def to_json(self) -> dict:
        return {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time is not None else None
        }

    @classmethod
    def from_json(cls, data: dict) -> 'Chapter':
        start_time = datetime.fromisoformat(data['start_time']) if data['start_time'] is not None else None
        end_time = datetime.fromisoformat(data['end_time']) if data['end_time'] is not None else None
        return cls(start_time, end_time)

    def __eq__(self, other: 'Chapter') -> bool:
        if isinstance(other, Chapter):
            return self.start_time == other.start_time and self.end_time == other.end_time
        return False


class Story:

    def __init__(self, name: str, start_date: datetime,
                 end_date: Optional[datetime] = None,
                 chapters: Optional[list[Chapter]] = None,
                 tags: Optional[list[str]] = None):
        if chapters is None:
            chapters = []
        if tags is None:
            tags = []
        self.name: str = name
        self.chapters: List[Chapter] = chapters
        self.start_date: datetime = start_date
        self.end_date: Optional[datetime] = end_date
        self.tags: List[str] = tags

    def compute_elapsed_time_from_chapters(self) -> timedelta:
        return sum([chapter.elapsed_time() for chapter in self.chapters], timedelta())

    def add_chapter(self, chapter: Chapter) -> None:
        self.chapters.append(chapter)

    def get_last_chapter(self) -> Chapter:
        return self.chapters[-1]

    def finish_chapter(self) -> None:
        if self.in_progress():
            self.get_last_chapter().end_time = datetime.now()
        else:
            raise ChapterNotInProgressException(self.name)

    def finish_story(self) -> None:
        if self.is_finished():
            raise StoryAlreadyFinishedException(self.name)
        if self.in_progress():
            self.finish_chapter()
        self.end_date = self.get_last_chapter().end_time

    def is_finished(self) -> bool:
        return self.end_date is not None

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'tags': self.tags,
            'chapters': [chapter.to_json() for chapter in self.chapters]
        }

    @classmethod
    def from_json(cls, data: dict) -> 'Story':
        name = data['name']
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date']) if data['end_date'] else None
        tags = data['tags']
        chapters = [Chapter.from_json(chapter_data) for chapter_data in data['chapters']]
        return cls(name, start_date, end_date, chapters, tags)

    def in_progress(self) -> bool:
        return self.get_last_chapter().in_progress() if len(self.chapters) > 0 else False

    def to_renderable(self, exit_live_message: str) -> str:
        name_line = f'[bold]✏️ Name:[/bold] \n  {self.name}'
        start_date_line = (f'[bold]🗓️ Start Date:[/bold] \n'
                           f'  {self.start_date.day}/{self.start_date.month}/{self.start_date.year}')
        elapsed_time = self.compute_elapsed_time_from_chapters()
        elapsed_line = (f'[bold]⏱️ Elapsed Time:[/bold] \n'
                        f'  {elapsed_time.seconds // 3600} hours, '
                        f'{(elapsed_time.seconds // 60) % 60} minutes, '
                        f'{elapsed_time.seconds % 60} seconds')
        tags = f'[bold]🏷️ Tags:[/bold] \n  {str(self.tags)}'
        return '\n'.join((name_line, start_date_line, elapsed_line, tags, f'\n[{exit_live_message}]'))

    def __eq__(self, other):
        if isinstance(other, Story):
            return (
                    self.name == other.name and
                    self.start_date == other.start_date and
                    self.end_date == other.end_date and
                    self.chapters == other.chapters and
                    self.tags == other.tags
            )
        return False
