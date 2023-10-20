import pytest
from assertpy import assert_that

from bookshelf.exceptions import (
    StoryNotFoundException,
    StoryAlreadyExistsException,
    StoryAlreadyFinishedException,
    ChapterInProgressException,
    ChapterNotInProgressException,
)


def test_story_not_found_exception():
    story_name = 'my_story_name'
    with pytest.raises(StoryNotFoundException) as exc_info:
        raise StoryNotFoundException(story_name)
    assert_that(str(exc_info.value)).is_equal_to('Could not find story with name [bold]my_story_name[/bold].')
    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌Could not find story with name [bold]{story_name}[/bold].\n'
        f'💡You can create one with [bold]bookshelf create {story_name}[/bold].')


# Test cases for StoryAlreadyExistsException
def test_story_already_exists_exception():
    story_name = 'existing_story'
    with pytest.raises(StoryAlreadyExistsException) as exc_info:
        raise StoryAlreadyExistsException('existing_story')
    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌The story [bold]{story_name}[/bold] already exists.\n'
        f'💡Use [bold]bookshelf create {story_name} --force [/bold] to override.')


def test_story_already_finished_exception():
    story_name = 'finished_story'
    with pytest.raises(StoryAlreadyFinishedException) as exc_info:
        raise StoryAlreadyFinishedException('finished_story')
    assert_that(str(exc_info.value)).is_equal_to('The story [bold]finished_story[/bold] is already finished.')
    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌The story [bold]{story_name}[/bold] is already finished.\n'
        f'💡Use [bold]bookshelf create {story_name} [/bold] a new story.')


def test_chapter_in_progress_exception():
    story_name = 'story_with_in_progress_chapter'
    with pytest.raises(ChapterInProgressException) as exc_info:
        raise ChapterInProgressException('story_with_in_progress_chapter')
    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌The current chapter in [bold]{story_name}[/bold] is in progress.\n'
        f'💡Use [bold]bookshelf stop {story_name}[/bold] before starting a new one.')


# Test cases for ChapterNotInProgressException
def test_chapter_not_in_progress_exception():
    story_name = 'story_without_in_progress_chapter'
    with pytest.raises(ChapterNotInProgressException) as exc_info:
        raise ChapterNotInProgressException('story_without_in_progress_chapter')
    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌The current chapter in {story_name} is not in progress.\n'
        f'💡Use [bold]bookshelf start {story_name}[/bold] to start one.')
