from unittest.mock import MagicMock
from assertpy import assert_that
from click.shell_completion import CompletionItem

from bookshelf.param_types import StoryType
from test.utils.storage_utils import create_test_story


def test_story_type_init():
    # Create a MagicMock object for BookshelfStorage
    bookshelf_storage = MagicMock()
    story_type = StoryType(bookshelf_storage)
    assert_that(story_type.name).is_equal_to('story')
    assert_that(story_type.bookshelf_storage).is_equal_to(bookshelf_storage)


def test_story_type_shell_complete_filters_stories():
    # Create a MagicMock object for BookshelfStorage
    bookshelf_storage = MagicMock()
    story_type = StoryType(bookshelf_storage)

    # Mock the behavior of bookshelf_storage.get_all_stories_matching_incomplete_name
    bookshelf_storage.get_all_stories_matching_incomplete_name.return_value = [
        create_test_story('SampleStory1'),
        create_test_story('SampleStory2')
    ]

    # Create MagicMock objects for ctx, param, and incomplete
    ctx = MagicMock()
    param = MagicMock()
    incomplete = 'Sam'

    # Call the shell_complete method
    completions = story_type.shell_complete(ctx, param, incomplete)

    # Assert that the completions are as expected
    expected_completion_1 = CompletionItem('SampleStory1')
    expected_completion_2 = CompletionItem('SampleStory2')

    assert_that(len(completions)).is_equal_to(2)

    for completion in completions:
        assert_that(completion).is_instance_of(CompletionItem)
        assert_that(completion.value).is_in(expected_completion_1.value, expected_completion_2.value)
