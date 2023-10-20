from datetime import datetime

import rich_click as click

from bookshelf.console import BookshelfConsole
from bookshelf.storage import BookshelfStorage
from bookshelf.models import Chapter, Story
from bookshelf.exceptions import StoryAlreadyExistsException, StoryNotFoundException, ChapterInProgressException, \
    StoryAlreadyFinishedException

bookshelf_storage = BookshelfStorage()
bookshelf_console = BookshelfConsole(bookshelf_storage)


def entry_point():
    try:
        bookshelf()
    except (Exception, KeyboardInterrupt) as exception:
        bookshelf_console.print(exception.terminal_message, style='red')
        exit(0)


@click.group()
def bookshelf():
    """📚 Bookshelf - A CLI tool to tracking your stories in the SDLC"""


@bookshelf.command(name='create')
@click.argument('story_name')
@click.option('-f',
              '--force',
              type=str,
              is_flag=True,
              help='Usually, the command will not start a story that already exists. '
                   'This flag disables these checks, use it with care.')
@click.option('-t',
              '--tags',
              type=str,
              help='Comma-separated list of tags that you want to apply to the story.')
@click.option('--start-chapter',
              type=bool,
              is_flag=True,
              show_default=True,
              default=False,
              help='Optionally start the first chapter of the story you are creating right away.')
def create_story_entry(story_name: str, force: bool, tags: str, start_chapter: bool):
    """Create a new story for your bookshelf"""
    try:
        tags_list = [tag.strip() for tag in tags.split(',')] if tags is not None else []

        if bookshelf_storage.story_exists(story_name) and not force:
            raise StoryAlreadyExistsException(story_name)

        start_time = datetime.now()
        story = Story(story_name, start_time, tags=tags_list)
        if start_chapter:
            story.add_chapter(Chapter(start_time))

        bookshelf_storage.save_story(story)

        bookshelf_console.render_story_panel(story)
    except KeyboardInterrupt:
        pass


@bookshelf.command(name='start')
@click.argument('story_name')
def start_chapter_entry(story_name):
    """Start a new chapter for a story on your bookshelf"""
    try:
        if not bookshelf_storage.story_exists(story_name):
            raise StoryNotFoundException(story_name)

        story = bookshelf_storage.load_story(story_name)

        if story.in_progress():
            raise ChapterInProgressException(story_name)

        if story.is_finished():
            raise StoryAlreadyFinishedException(story_name)

        start_time = datetime.now()
        chapter = Chapter(start_time)
        story.add_chapter(chapter)

        bookshelf_storage.save_story(story)
        bookshelf_console.render_story_panel(story)
    except KeyboardInterrupt:
        pass


@bookshelf.command(name='stop')
@click.argument('story_name')
def stop_chapter_entry(story_name):
    """Stop the current chapter of a story on your bookshelf"""

    try:
        if not bookshelf_storage.story_exists(story_name):
            raise StoryNotFoundException(story_name)
        story = bookshelf_storage.load_story(story_name)
        story.finish_chapter()

        bookshelf_storage.save_story(story)

        bookshelf_console.render_story_panel(story)
    except KeyboardInterrupt:
        pass


@bookshelf.command(name='finish')
@click.argument('story_name')
def finish_story_entry(story_name):
    """Finish writing a story on your bookshelf"""
    try:
        if not bookshelf_storage.story_exists(story_name):
            raise StoryNotFoundException(story_name)
        story = bookshelf_storage.load_story(story_name)
        story.finish_story()

        bookshelf_storage.save_story(story)

        bookshelf_console.render_story_panel(story)
    except KeyboardInterrupt:
        pass


@bookshelf.command(name='ls')
@click.option('--with-tags', type=str, help='Comma-separated list of tags that you wish to filter in.')
def list_stories_entry(with_tags: str):
    """List all the current stories on your bookshelf"""
    try:
        tags_to_filter_by = [tag.strip() for tag in with_tags.split(',')] if with_tags is not None else []
        bookshelf_console.render_all_stories_table(tags_to_filter_by=tags_to_filter_by)
    except KeyboardInterrupt:
        pass


@bookshelf.command(name='rm')
@click.argument('story_name')
def remove_story_entry(story_name):
    """Remove a story from your bookshelf"""
    try:
        story = bookshelf_storage.load_story(story_name)
        exit_live_message = 'Press [bold]CTRL+C[/bold] to delete'
        bookshelf_console.render_story_panel(story, exit_live_message=exit_live_message)
    except KeyboardInterrupt:
        bookshelf_storage.delete_story(story_name)
        bookshelf_console.print(f'🗑️ Story \'{story_name}\' has been deleted!')


@bookshelf.command(name='info')
@click.argument('story_name')
def story_info_entry(story_name: str):
    """Displays the information for a given story on your bookshelf"""
    try:
        story = bookshelf_storage.load_story(story_name)
        bookshelf_console.render_story_panel(story)
    except KeyboardInterrupt:
        pass
