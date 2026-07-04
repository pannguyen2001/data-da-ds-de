import datetime
import shutil
from pathlib import Path

import pandas as pd

from src.common.logger import logger


def cleanup_file_or_folder(
    report_dir: str = "report",
    days: int = 0,
    hours: int = 0,
    minutes: int = 30,
    dry_run: bool = True,
    name_format: str = "%Y-%m-%d",
) -> None:
    """Clean up old files and folders.
    Args:
        report_dir (str): Directory to clean up.
        days (int): Number of days to keep files.
        hours (int): Number of hours to keep files.
        minutes (int): Number of minutes to keep files.
        dry_run (bool): If True, don't delete anything.
        name_format (str): Format of the file/folder name.
    """

    report_path = Path(report_dir)
    logger.info(f"Cleanup started: '{report_path.resolve()}' | dry_run={dry_run}")

    if not report_path.exists():
        logger.warning(f"Directory '{report_dir}' not found.")
        return

    if days == 0 and hours == 0 and minutes == 0:
        logger.warning("All time deltas are 0 — skipping to avoid deleting everything.")
        return

    cutoff_date = datetime.datetime.now(
        tz=datetime.timezone(datetime.timedelta(hours=7))
    ) - datetime.timedelta(days=days, hours=hours, minutes=minutes)
    deleted, skipped, invalid = [], [], []

    for item in report_path.iterdir():
        try:
            # Use stem for files (strips .log, .csv, etc.), name for folders
            item_stem = item.stem if item.is_file() else item.name
            item_date = datetime.datetime.strptime(item_stem, name_format).replace(
                tzinfo=datetime.timezone(datetime.timedelta(hours=7))
            )

            if item_date < cutoff_date:
                if not dry_run:
                    try:
                        shutil.rmtree(item) if item.is_dir() else item.unlink()
                    except PermissionError as e:
                        logger.warning(f"Permission denied: {item.name} — {e}")
                        invalid.append(f"{item.name} (permission denied)")
                        continue
                deleted.append(item.name)
            else:
                skipped.append(item.name)
        except ValueError:
            invalid.append(item.name)

    mode = "DRY RUN 🧪" if dry_run else "LIVE 🗑️ "
    df_result = pd.DataFrame(
        [
            {
                "Action": "Deleted",
                "Count": len(deleted),
                "Items": "\n".join(deleted) or "-",
            },
            {
                "Action": "Skipped",
                "Count": len(skipped),
                "Items": "\n".join(skipped) or "-",
            },
            {
                "Action": "Warning",
                "Count": len(invalid),
                "Items": "\n".join(invalid) or "-",
            },
        ]
    )
    logger.success(
        f"[{mode}] Cutoff datetime: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{df_result.to_markdown(index=False)}"
    )
