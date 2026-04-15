"""
Orchestrator — Master process that ties watchers, Qwen Code, and the vault together.

The orchestrator:
1. Monitors the /Needs_Action folder for new action files.
2. When files are found, it triggers Qwen Code to process them.
3. Moves completed tasks to /Done.
4. Updates the Dashboard.
5. Manages watcher subprocesses (optional process manager).

Usage:
    python orchestrator.py [--vault /path/to/vault] [--dry-run]
"""

import os
import sys
import time
import json
import shutil
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


class Orchestrator:
    """Main orchestrator for the AI Employee system."""

    def __init__(self, vault_path: str, dry_run: bool = False):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'

        self.dry_run = dry_run

        # Ensure all directories exist
        for d in [self.needs_action, self.done, self.pending_approval,
                  self.approved, self.rejected, self.logs]:
            d.mkdir(parents=True, exist_ok=True)

        # Set up logging (handler is configured by the caller via basicConfig)
        self.logger = logging.getLogger('Orchestrator')
        self.logger.setLevel(logging.INFO)

        # Track processed files
        self.processed = set()

        # Watcher subprocesses (for future use)
        self.watcher_processes = {}

    def scan_needs_action(self) -> list:
        """Scan the /Needs_Action folder for new .md action files."""
        action_files = []
        for f in self.needs_action.glob('*.md'):
            if str(f) not in self.processed:
                action_files.append(f)
        return action_files

    def process_action_file(self, filepath: Path):
        """
        Process a single action file.

        In Bronze tier, this logs the file and prepares it for Qwen Code.
        In higher tiers, this would trigger MCP servers, approval workflows, etc.
        """
        self.logger.info(f'Processing: {filepath.name}')

        # Read the action file
        content = filepath.read_text()

        # Log the action
        self._log_action(filepath.name, 'scan', 'success')

        # In Bronze tier, we just log and prepare for Qwen Code
        # In higher tiers, this would:
        # - Parse the action type from frontmatter
        # - Route to appropriate handler (email, payment, etc.)
        # - Create a Plan.md file
        # - Request approval if needed

        if self.dry_run:
            self.logger.info(f'[DRY RUN] Would process: {filepath.name}')
            return

        # Move to Done after processing (Bronze tier behavior)
        # In production, Qwen Code would handle this after completing the task
        dest = self.done / filepath.name
        shutil.move(str(filepath), str(dest))
        self.processed.add(str(filepath))
        self.logger.info(f'Moved to Done: {filepath.name}')

    def check_approvals(self):
        """Check the /Approved folder for approved actions to execute."""
        for f in self.approved.glob('*.md'):
            self.logger.info(f'Approved action found: {f.name}')
            # In higher tiers, this would trigger MCP execution
            # For Bronze tier, just log
            self._log_action(f.name, 'approval_check', 'approved')

            # Move to Done
            dest = self.done / f.name
            shutil.move(str(f), str(dest))
            self.logger.info(f'Moved to Done: {f.name}')

    def _log_action(self, filename: str, action_type: str, result: str):
        """Log an action to /Logs/YYYY-MM-DD.json."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'file': filename,
            'action_type': action_type,
            'result': result,
            'dry_run': self.dry_run
        }

        # Load existing log or create new
        if log_file.exists():
            logs = json.loads(log_file.read_text())
        else:
            logs = []

        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))

    def update_dashboard(self, pending_count: int, done_count: int):
        """Update the Dashboard.md with current status."""
        if not self.dashboard.exists():
            return

        content = self.dashboard.read_text()

        # Update pending count
        content = content.replace(
            '- **Pending Actions**: 0',
            f'- **Pending Actions**: {pending_count}'
        )

        # Update timestamp
        content = content.replace(
            f'last_updated: {content.split("last_updated: ")[1].split(chr(10))[0]}',
            f'last_updated: {datetime.now().isoformat()}'
        )

        if not self.dry_run:
            self.dashboard.write_text(content)

    def run(self, interval: int = 10):
        """Main orchestrator loop."""
        self.logger.info(f'Starting Orchestrator')
        self.logger.info(f'Vault: {self.vault_path}')
        self.logger.info(f'Dry run: {self.dry_run}')
        self.logger.info(f'Check interval: {interval}s')

        if self.dry_run:
            self.logger.warning('*** DRY RUN MODE — No files will be modified ***')

        while True:
            try:
                # Scan for new action files
                action_files = self.scan_needs_action()

                if action_files:
                    self.logger.info(f'Found {len(action_files)} action file(s)')
                    for f in action_files:
                        self.process_action_file(f)

                # Check for approved actions
                self.check_approvals()

                # Update dashboard
                pending = len(list(self.needs_action.glob('*.md')))
                done = len(list(self.done.glob('*.md')))
                self.update_dashboard(pending, done)

                # Log cycle
                self.logger.debug(f'Cycle complete — Pending: {pending}, Done: {done}')

            except Exception as e:
                self.logger.error(f'Error in orchestrator loop: {e}', exc_info=True)

            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument(
        '--vault', '-v',
        type=str,
        default=str(Path(__file__).parent),
        help='Path to the Obsidian vault directory'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=10,
        help='Check interval in seconds (default: 10)'
    )
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Log actions without modifying files'
    )
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    orchestrator = Orchestrator(
        vault_path=args.vault,
        dry_run=args.dry_run
    )
    orchestrator.run(interval=args.interval)


if __name__ == '__main__':
    main()
