import logging
import tarfile
from datetime import datetime, timedelta
from config import BASE_DIR


class Logger:
    def __init__(self, folder_name: str):
        self.folder_name = folder_name

    @property
    def log_folder(self):
        log_folder = BASE_DIR / self.folder_name / datetime.now().strftime('%Y-%m-%d')
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        return log_folder

    def _rotate_log_file(self):
        current_log_folder = self.log_folder
        current_log_file = current_log_folder / datetime.now().strftime('%H-%M-%S.log')

        if current_log_file.exists():
            return

        logging.basicConfig(
            filename=current_log_file,
            format='%(asctime)s - [%(levelname)s] - %(funcName)s - %(message)s',
            level=logging.INFO,
            force=True
        )

    def _archive_old_logs(self, days: int = 7):
        old_logs_time = datetime.now() - timedelta(days=days)
        logs_folder = self.log_folder

        for log_folder in logs_folder.iterdir():
            if log_folder.is_dir() and datetime.strptime(log_folder.name, '%Y-%m-%d') < old_logs_time:
                archive_path = log_folder.with_suffix('.tar.gz')
                with tarfile.open(archive_path, 'w:gz') as archive:
                    archive.add(log_folder, arcname=log_folder.name)
                for log_file in log_folder.iterdir():
                    log_file.unlink()  # Delete individual log files
                log_folder.rmdir()  # Delete empty log folder

    def setup(self):
        self._archive_old_logs()
        self._rotate_log_file()

