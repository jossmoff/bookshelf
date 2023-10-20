class BookshelfBaseException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class BookshelfStoryException(BookshelfBaseException):

    def __init__(self, story_name: str, message_template: str, hint_template: str):
        self.terminal_message = self._construct_exception_message(story_name, message_template, hint_template)
        super().__init__(message_template.format(story_name))

    @staticmethod
    def _construct_exception_message(story_name: str, message_template: str, hint_template: str) -> str:
        return f'❌{message_template}\n💡{hint_template}'.format(story_name, story_name)


class StoryNotFoundException(BookshelfStoryException):
    MESSAGE_TEMPLATE = 'Could not find story with name [bold]{}[/bold].'
    HINT_TEMPLATE = 'You can create one with [bold]bookshelf create {}[/bold].'

    def __init__(self, story_name):
        super().__init__(story_name, self.MESSAGE_TEMPLATE, self.HINT_TEMPLATE)


class StoryAlreadyExistsException(BookshelfStoryException):
    MESSAGE_TEMPLATE = 'The story [bold]{}[/bold] already exists.'
    HINT_TEMPLATE = 'Use [bold]bookshelf create {} --force [/bold] to override.'

    def __init__(self, story_name):
        super().__init__(story_name, self.MESSAGE_TEMPLATE, self.HINT_TEMPLATE)


class StoryAlreadyFinishedException(BookshelfStoryException):
    MESSAGE_TEMPLATE = 'The story [bold]{}[/bold] is already finished.'
    HINT_TEMPLATE = 'Use [bold]bookshelf create {} [/bold] a new story.'

    def __init__(self, story_name):
        super().__init__(story_name, self.MESSAGE_TEMPLATE, self.HINT_TEMPLATE)


class ChapterInProgressException(BookshelfStoryException):
    MESSAGE_TEMPLATE = 'The current chapter in [bold]{}[/bold] is in progress.'
    HINT_TEMPLATE = 'Use [bold]bookshelf stop {}[/bold] before starting a new one.'

    def __init__(self, story_name):
        super().__init__(story_name, self.MESSAGE_TEMPLATE, self.HINT_TEMPLATE)


class ChapterNotInProgressException(BookshelfStoryException):
    MESSAGE_TEMPLATE = 'The current chapter in {} is not in progress.'
    HINT_TEMPLATE = 'Use [bold]bookshelf start {}[/bold] to start one.'

    def __init__(self, story_name):
        super().__init__(story_name, self.MESSAGE_TEMPLATE, self.HINT_TEMPLATE)
