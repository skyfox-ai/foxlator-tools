
import os
from typing import Any, Dict, List, Tuple
import pandas as pd
import json
import logging
from .stt_providers.ISTTBase import STTResult


def _get_all_reports_from_dir(dir: str):
    files = os.listdir(dir)
    reports_paths = [os.path.join(dir, file) for file in files if file.startswith(
        "report_") and file.endswith(".json")]
    reports: Dict[str, List[STTResult]] = {}
    for report_path in reports_paths:
        with open(report_path) as user_file:
            stt_results: List[STTResult] = json.loads(user_file.read())
            report_name = os.path.basename(report_path).split(
                "report_")[1].split(".json")[0]
            reports[report_name] = stt_results
    if not reports:
        raise Exception(f"No reports in {dir}")
    return reports


def create_general_report(reports_dir: str):
    logging.info("Creating general report...")
    all_reports = _get_all_reports_from_dir(reports_dir)
    general_report = pd.DataFrame()
    multi_indexes: List[Tuple[str, str]] = [('Transciption', 'Oryginal')]
    general_report[multi_indexes[0]] = [
        trans["trans"] for trans in next(iter(all_reports.values()))]
    for key in STTResult.__annotations__:
        if key == "trans":
            continue
        for report_name, stt_results in all_reports.items():
            values: List[Any] = [result[key] for result in stt_results]
            index = (key, report_name)
            multi_indexes.append(index)
            general_report[index] = values
    general_report.columns = pd.MultiIndex.from_tuples(  # type: ignore
        multi_indexes)
    report_path = os.path.join(reports_dir, "general_report.xlsx")
    general_report.to_excel(report_path)  # type: ignore
    logging.info("Report path: %s", report_path)
