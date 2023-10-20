import time
from typing import Optional

from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich import box

from bookshelf.storage import BookshelfStorage
from bookshelf.models import Story


class BookshelfConsole(Console):
    def __init__(self, bookshelf_storage: BookshelfStorage):
        super().__init__()
        self.bookshelf_storage = bookshelf_storage

    def render_all_stories_table(self, tags_to_filter_by: Optional[list[str]] = None) -> None:
        table = Table(title="📖 Stories 📖", box=box.DOUBLE_EDGE)
        table.add_column('✏️ Name', style="cyan", justify="center")
        table.add_column('🗓️ Start Date', style="white", justify="center")
        table.add_column('🏷️ Tags', style="yellow", justify="center")
        for story in self.bookshelf_storage.get_all_stories():
            if len(tags_to_filter_by) == 0 or any(tag in story.tags for tag in tags_to_filter_by):
                table.add_row(f'{story.name}',
                              f'{story.start_date.day}/{story.start_date.month}/{story.start_date.year}',
                              f'{story.tags}')

        self.print(table)

    def render_story_panel(self, story, exit_live_message: Optional[str] = None, should_clear: bool = True) -> None:
        if exit_live_message is None:
            exit_live_message = 'Press [bold]CTRL+C[/bold] to exit'

        with Live(self._get_story_panel(story, exit_live_message),
                  transient=should_clear,
                  refresh_per_second=1) as live_panel:
            while True:
                live_panel.update(self._get_story_panel(story, exit_live_message))
                time.sleep(0.4)

        if should_clear:
            self.clear()

    @staticmethod
    def _get_story_panel(story: Story, exit_live_message: str):
        panel = Panel(story.to_renderable(exit_live_message=exit_live_message), title='📖 Story 📖', expand=True)
        return Padding(panel, 1)
