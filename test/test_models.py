import pytest
from datetime import timedelta, datetime

from assertpy import assert_that

from bookshelf.models import Chapter, Story
from test.utils.chapter_utils import create_chapter_from_delta

STORY_NAME = 'TEST_STORY'

SESSION_JSON = {
    'start_time': '2023-10-20T09:00:00',
    'end_time': '2023-10-20T10:30:00'
}

STORY_JSON = {
    'name': STORY_NAME,
    'start_date': '2023-10-20T08:00:00',
    'end_date': '2023-10-20T12:00:00',
    'tags': ['tag1', 'tag2'],
    'chapters': [SESSION_JSON]
}


@pytest.fixture
def sample_chapter():
    return Chapter.from_json(SESSION_JSON)


@pytest.fixture
def sample_story():
    return Story.from_json(STORY_JSON)


def test_elapsed_time(sample_chapter):
    elapsed = sample_chapter.elapsed_time()
    expected_elapsed = timedelta(hours=1, minutes=30, seconds=0)
    assert_that(elapsed).is_equal_to(expected_elapsed)


def test_chapter_to_dict(sample_chapter):
    chapter_dict = sample_chapter.to_json()
    assert_that(chapter_dict).is_equal_to(SESSION_JSON)


def test_story_to_dict(sample_story):
    story_dict = sample_story.to_json()
    assert_that(story_dict).is_equal_to(STORY_JSON)
    assert story_dict == STORY_JSON


def test_story_from_dict():
    story = Story.from_json(STORY_JSON)
    assert story.name == STORY_NAME
    assert story.start_date == datetime(2023, 10, 20, 8, 0, 0)
    assert story.end_date == datetime(2023, 10, 20, 12, 0, 0)
    assert story.tags == ['tag1', 'tag2']
    assert len(story.chapters) == 1
    assert story.chapters[0].start_time == datetime(2023, 10, 20, 9, 0, 0)
    assert story.chapters[0].end_time == datetime(2023, 10, 20, 10, 30, 0)


def test_compute_duration_from_chapters():
    chapter1 = create_chapter_from_delta(timedelta(hours=1))
    chapter2 = create_chapter_from_delta(timedelta(hours=1))
    chapters = [chapter1, chapter2]
    story = Story(STORY_NAME, datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 14, 0), chapters)

    assert story.compute_elapsed_time_from_chapters() == timedelta(hours=2)
