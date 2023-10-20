import os
import json
from pathlib import Path
from typing import Generator

from bookshelf.exceptions import StoryNotFoundException
from bookshelf.models import Story


class BookshelfStorage:
    BOOKSHELF_DIR = f'{Path.home()}/.bookshelf'
    BOOKSHELF_TASK_DIR = f'{BOOKSHELF_DIR}/tasks'

    def __init__(self):
        # TODO: Doesn't need to be a class but will probably want to in the future
        pass

    def save_story(self, story: Story) -> None:
        if not os.path.exists(self.BOOKSHELF_DIR):
            os.makedirs(self.BOOKSHELF_TASK_DIR)
        filename = os.path.join(self.BOOKSHELF_TASK_DIR, f'{story.name}.json')
        with open(filename, 'w') as file:
            data = story.to_json()
            json.dump(data, file)

    def load_story(self, story_name: str) -> Story:
        story_path = self._get_story_path(story_name)
        if os.path.exists(story_path):
            with open(story_path, 'r') as file:
                data = json.load(file)
                return Story.from_json(data)
        raise StoryNotFoundException(story_name)

    def delete_story(self, story_name: str) -> None:
        story_path = self._get_story_path(story_name)
        if os.path.exists(story_path):
            os.remove(story_path)
        else:
            raise StoryNotFoundException(story_name)

    def _get_story_path(self, story_name: str) -> str:
        return os.path.join(self.BOOKSHELF_TASK_DIR, f'{story_name}.json')

    def story_exists(self, story_name: str) -> bool:
        file_path = os.path.join(self.BOOKSHELF_TASK_DIR, f'{story_name}.json')
        return os.path.exists(file_path)

    def get_all_stories(self) -> Generator[Story, None, None]:
        for root, _, files in os.walk(self.BOOKSHELF_TASK_DIR):
            for filename in files:
                if filename.endswith('.json'):
                    file_path = os.path.join(root, filename)

                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            yield Story.from_json(data)
                        except json.JSONDecodeError:
                            # TODO: Maybe add some logs here that can be enabled with --logs
                            pass
