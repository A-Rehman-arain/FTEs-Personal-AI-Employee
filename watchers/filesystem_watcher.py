"""
Filesystem Watcher — Monitors a drop folder for new files and creates action files.

This is the Bronze-tier working watcher. It watches the `/Inbox` folder for new files.
When a file is created, it copies it to `/Needs_Action` with a corresponding .md metadata file.

Usage:
    python filesystem_watcher.py [--vault /path/to/vault] [--inbox /path/to/inbox]
"""

import os
import sys
import time
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import base_watcher
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DropFolderHandler(FileSystemEventHandler):
    """Handles file creation events in the Inbox/drop folder."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.logger = logging.getLogger('DropFolderHandler')

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

        # Track processed files to avoid duplicates
        self.processed = set()

    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Skip if already processed
        if str(source) in self.processed:
            return

        # Skip hidden files and temp files
        if source.name.startswith('.') or source.name.endswith('.tmp'):
            return

        self.process_file(source)

    def process_file(self, source: Path):
        """Process a newly dropped file."""
        self.logger.info(f'New file detected: {source.name}')

        # Copy the file to Needs_Action
        dest_name = f'FILE_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{source.name}'
        dest = self.needs_action / dest_name

        try:
            shutil.copy2(source, dest)
            self.logger.info(f'Copied to: {dest.name}')

            # Create metadata sidecar file
            meta_path = self.needs_action / f'{dest_name}.md'
            meta_path.write_text(self._create_metadata(source))
            self.logger.info(f'Created metadata: {meta_path.name}')

            self.processed.add(str(source))

        except Exception as e:
            self.logger.error(f'Failed to process {source.name}: {e}')

    def _create_metadata(self, source: Path) -> str:
        """Create Markdown metadata for a dropped file."""
        stat = source.stat()
        content = f"""---
type: file_drop
original_name: {source.name}
size_bytes: {stat.st_size}
dropped_at: {datetime.now().isoformat()}
status: pending
---

# File Drop: {source.name}

## File Details
- **Original Name**: {source.name}
- **Size**: {stat.st_size} bytes
- **Dropped At**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Content
_File copied to Needs_Action folder for processing._

## Suggested Actions
- [ ] Review file content
- [ ] Process or archive
- [ ] Move to Done when complete
"""
        return content


class FilesystemWatcher(BaseWatcher):
    """Filesystem watcher using watchdog library."""

    def __init__(self, vault_path: str, check_interval: int = 5):
        super().__init__(vault_path, check_interval)
        self.inbox = self.vault_path / 'Inbox'
        self.inbox.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        """
        Not used directly — watchdog handles events asynchronously.
        This method is here to satisfy the BaseWatcher interface.
        """
        return []

    def create_action_file(self, item) -> Path:
        """
        Not used directly — handled by DropFolderHandler.
        This method is here to satisfy the BaseWatcher interface.
        """
        pass

    def run(self):
        """Override run() to use watchdog observer instead of polling loop."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Watching inbox: {self.inbox}')

        event_handler = DropFolderHandler(str(self.vault_path))
        observer = Observer()
        observer.schedule(event_handler, str(self.inbox), recursive=False)
        observer.start()

        self.logger.info('Filesystem watcher is running...')
        self.logger.info(f'Drop files into: {self.inbox}')

        try:
            while True:
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info('Stopping filesystem watcher...')
            observer.stop()

        observer.join()
        self.logger.info('Filesystem watcher stopped.')


def main():
    parser = argparse.ArgumentParser(description='Filesystem Watcher for AI Employee')
    parser.add_argument(
        '--vault', '-v',
        type=str,
        default=str(Path(__file__).parent.parent),
        help='Path to the Obsidian vault directory (default: project root)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=5,
        help='Check interval in seconds (default: 5)'
    )
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    watcher = FilesystemWatcher(
        vault_path=args.vault,
        check_interval=args.interval
    )
    watcher.run()


if __name__ == '__main__':
    main()
