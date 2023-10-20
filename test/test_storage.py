import json
from pathlib import Path

import pytest
import os

from assertpy import assert_that
from unittest.mock import MagicMock, patch, mock_open

from bookshelf.models import Story
from bookshelf.storage import BookshelfStorage
from bookshelf.exceptions import StoryNotFoundException
from test.utils.storage_utils import create_test_story_dict, create_story_json_string, create_test_story

BOOKSHELF_DIR = f'{Path.home()}/.bookshelf'
BOOKSHELF_TASK_DIR = f'{BOOKSHELF_DIR}/tasks'


@pytest.fixture(autouse=True)
def mock_home():
    with patch('pathlib.Path.home') as mock_home:
        mock_home.return_value = 'BOOKSHELF_DIR'
        yield mock_home


@pytest.fixture
def bookshelf_storage():
    return BookshelfStorage()


def test_delete_existing_story(bookshelf_storage, mock_home):
    os.remove = MagicMock()
    os.path.exists = MagicMock(return_value=True)

    story_name = 'my_story'
    story_path = os.path.join(f'{BOOKSHELF_TASK_DIR}/{story_name}.json')

    bookshelf_storage.delete_story(story_name)

    os.remove.assert_called_once_with(story_path)


def test_delete_nonexistent_story(bookshelf_storage, mock_home):
    os.path.exists = MagicMock(return_value=False)

    story_name = 'my_story'

    with pytest.raises(StoryNotFoundException) as exc_info:
        bookshelf_storage.delete_story(story_name)

    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌Could not find story with name [bold]{story_name}[/bold].\n'
        f'💡You can create one with [bold]bookshelf create {story_name}[/bold].')


def test_load_existing_story(bookshelf_storage, mock_home):
    os.path.exists = MagicMock(return_value=True)

    test_story_dict = create_test_story_dict()
    test_story = Story(**test_story_dict)
    # JSON expects double quotes instead of single
    test_story_json = create_story_json_string(**test_story_dict)

    story_path = os.path.join(f'{BOOKSHELF_TASK_DIR}/{test_story_dict["name"]}.json')

    m = mock_open(read_data=test_story_json)

    # Patch the open function to use the mock
    with patch('builtins.open', m):
        # Call the function that reads from the file
        story = bookshelf_storage.load_story(story_path)

    assert_that(story).is_equal_to(test_story)


def test_load_nonexistent_story(bookshelf_storage, mock_home):
    os.path.exists = MagicMock(return_value=False)

    story_name = 'my_story'

    with pytest.raises(StoryNotFoundException) as exc_info:
        bookshelf_storage.load_story(story_name)

    assert_that(exc_info.value.terminal_message).is_equal_to(
        f'❌Could not find story with name [bold]{story_name}[/bold].\n'
        f'💡You can create one with [bold]bookshelf create {story_name}[/bold].')


def test_save_non_existing_story(bookshelf_storage, mock_home):
    os.path.exists = MagicMock(return_value=False)
    os.makedirs = MagicMock()
    json.dump = MagicMock()

    test_story_dict = create_test_story_dict()
    test_story = Story(**test_story_dict)
    test_story_json_string = create_story_json_string(**test_story_dict)

    story_path = os.path.join(f'{BOOKSHELF_TASK_DIR}/{test_story_dict["name"]}.json')

    m_open = mock_open()

    with patch('builtins.open', m_open):
        bookshelf_storage.save_story(test_story)

    os.makedirs.assert_called_once_with(BOOKSHELF_TASK_DIR)
    m_open.assert_called_once_with(story_path, 'w')
    json.dump.assert_called_once_with(json.loads(test_story_json_string), m_open())


def test_get_all_stories(bookshelf_storage, mock_home):
    test_story_1 = create_test_story(name='Test1')
    test_story_2 = create_test_story(name='Test2')
    test_story_3 = create_test_story(name='Test3')
    test_stories = [test_story_1, test_story_2, test_story_3]

    os.walk = MagicMock()
    os.walk.return_value = [(BOOKSHELF_TASK_DIR,
                             [],
                             [f'{story.name}.json' for story in test_stories])]

    def side_effect(*args, **kwargs):
        # Use a generator to yield contents for each call
        for story in test_stories:
            yield str(story.to_json()).replace('\'', '"')

    m_open = mock_open()
    m_open().read.side_effect = side_effect()

    with patch('builtins.open', m_open):
        stories = list(bookshelf_storage.get_all_stories())

    assert_that(stories).contains_only(test_story_1, test_story_2, test_story_3)


def test_get_all_stories_with_invalid_json(bookshelf_storage):
    os.walk = MagicMock()
    os.walk.return_value = [(BOOKSHELF_TASK_DIR,
                             [],
                             ['a.json'])]
    m_open = mock_open()
    m_open().read.return_value = 'invalid json'

    with patch('builtins.open', m_open):
        stories = list(bookshelf_storage.get_all_stories())

    assert_that(stories).is_empty()


def test_get_all_stories_with_non_json(bookshelf_storage):
    os.walk = MagicMock()
    os.walk.return_value = [(BOOKSHELF_TASK_DIR,
                             [],
                             ['a.json'])]
    m_open = mock_open()
    m_open().read.return_value = 'invalid json'

    with patch('builtins.open', m_open):
        stories = list(bookshelf_storage.get_all_stories())

    assert_that(stories).is_empty()
