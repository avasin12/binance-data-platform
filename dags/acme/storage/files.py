#/home/avasin/airflow/dags/acme/storage/files.py
import logging
from pathlib import Path
logger = logging.getLogger(__name__)


def delete_local_files(file_info):
    """
    Args:
        filepath: str | list[str]
    """
    filepath = file_info["filepath"]


    if isinstance(filepath, str):
        files=[filepath]
    elif isinstance(filepath, list):
        files=filepath
    else:
        raise TypeError(
            "filepath must be str or list[str]"
        )

    for file in files:


        path = Path(file)
        if not path.exists():
            logger.warning("File does not exist: %s", path)
            continue
        try:
            path.unlink()
            logger.info(f'File successfully deleted {path}')


        except FileNotFoundError:
            logger.warning("File already deleted: %s", path)
        except Exception:
            logger.exception("Can not delete files")
            raise
