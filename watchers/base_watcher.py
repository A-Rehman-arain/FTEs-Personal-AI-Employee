"""
Base Watcher — Abstract template for all watcher scripts.

All watchers follow this pattern:
1. Initialize with vault path and check interval.
2. Periodically check for new items (emails, messages, files, etc.).
3. Create .md action files in the /Needs_Action folder.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod


class BaseWatcher(ABC):
    """Abstract base class for all watcher scripts."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval

        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)

        # Set up logging
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.

        Returns:
            list: A list of items (dicts or objects) that need processing.
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file in the Needs_Action folder.

        Args:
            item: An item returned by check_for_updates().

        Returns:
            Path: The path to the created file.
        """
        pass

    def run(self):
        """Main loop — runs indefinitely, checking for updates periodically."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Watching vault: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')

        while True:
            try:
                items = self.check_for_updates()
                if items:
                    self.logger.info(f'Found {len(items)} new item(s)')
                    for item in items:
                        filepath = self.create_action_file(item)
                        self.logger.info(f'Created action file: {filepath.name}')
                else:
                    self.logger.debug('No new items found')
            except Exception as e:
                self.logger.error(f'Error in watcher loop: {e}', exc_info=True)

            time.sleep(self.check_interval)


if __name__ == '__main__':
    # This base class cannot be instantiated directly.
    # See filesystem_watcher.py or gmail_watcher.py for concrete implementations.
    print("This is a base class. Use a concrete watcher implementation.")
    print("Examples: filesystem_watcher.py, gmail_watcher.py")
