from click import ParamType
from click.shell_completion import CompletionItem

from bookshelf.storage import BookshelfStorage


class StoryType(ParamType):
    name = "story"

    def __init__(self, bookshelf_storage: BookshelfStorage) -> None:
        super().__init__()
        self.bookshelf_storage = bookshelf_storage

    def shell_complete(self, ctx, param, incomplete):
        return [
            CompletionItem(story.name, help=story.tags)
            for story in self.bookshelf_storage.get_all_stories_matching_incomplete_name(incomplete)
        ]
