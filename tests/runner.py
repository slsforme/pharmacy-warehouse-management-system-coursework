import subprocess
import sys
import re

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def parse_results(output: str) -> list[dict]:
    """Парсит вывод pytest и возвращает список результатов"""
    results = []
    lines = output.split("\n")

    for line in lines:
        if "::" in line and any(s in line for s in ["PASSED", "FAILED", "SKIPPED", "ERROR"]):
            parts = line.split("::")
            if len(parts) >= 2:
                test_class = parts[1] if len(parts) > 2 else ""
                test_name = parts[-1].split(" ")[0]

                if "PASSED" in line:
                    status = "PASSED"
                elif "FAILED" in line:
                    status = "FAILED"
                elif "SKIPPED" in line:
                    status = "SKIPPED"
                else:
                    status = "ERROR"

                results.append({
                    "class": test_class,
                    "name": test_name,
                    "status": status,
                })

    return results


def parse_summary(output: str) -> dict:
    """Парсит итоговую строку pytest"""
    summary = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}
    for line in output.split("\n"):
        if re.search(r"\d+ passed", line):
            if m := re.search(r"(\d+) passed", line):
                summary["passed"] = int(m.group(1))
            if m := re.search(r"(\d+) failed", line):
                summary["failed"] = int(m.group(1))
            if m := re.search(r"(\d+) skipped", line):
                summary["skipped"] = int(m.group(1))
            if m := re.search(r"(\d+) error", line):
                summary["errors"] = int(m.group(1))
    return summary


def print_results(results: list[dict], summary: dict):
    """Выводит результаты в виде таблицы"""

    # Таблица результатов
    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        expand=True,
    )
    table.add_column("Класс",       style="cyan",  no_wrap=True)
    table.add_column("Тест",        style="white", no_wrap=True)
    table.add_column("Результат",   justify="center", no_wrap=True)

    for result in results:
        if result["status"] == "PASSED":
            status_text = "[green]PASSED[/green]"
        elif result["status"] == "FAILED":
            status_text = "[red]FAILED[/red]"
        elif result["status"] == "SKIPPED":
            status_text = "[yellow]SKIPPED[/yellow]"
        else:
            status_text = "[red]ERROR[/red]"

        table.add_row(
            result["class"],
            result["name"],
            status_text,
        )

    console.print()
    console.print(table)
    console.print()

    # Итоговая панель
    has_failures = summary["failed"] > 0 or summary["errors"] > 0

    summary_text = (
        f"[green]Пройдено:   {summary['passed']}[/green]\n"
        f"[red]Упало:      {summary['failed']}[/red]\n"
        f"[yellow]Пропущено:  {summary['skipped']}[/yellow]\n"
        f"[red]Ошибок:     {summary['errors']}[/red]"
    )

    console.print(Panel(
        summary_text,
        title="[bold]Итого[/bold]",
        border_style="red" if has_failures else "green",
        expand=False,
    ))

    console.print()

    if has_failures:
        console.print(Panel(
            "[bold red]ТЕСТЫ НЕ ПРОШЛИ[/bold red]",
            border_style="red",
            expand=False,
        ))
    else:
        console.print(Panel(
            "[bold green]ВСЕ ТЕСТЫ ПРОШЛИ[/bold green]",
            border_style="green",
            expand=False,
        ))

    console.print()


def print_errors(output: str):
    """Выводит детали упавших тестов"""
    lines = output.split("\n")
    in_failure = False
    failure_lines = []

    for line in lines:
        if line.startswith("FAILED") or "_ FAILED _" in line:
            in_failure = True
            failure_lines = [line]
        elif in_failure:
            if line.startswith("=") and failure_lines:
                console.print(Panel(
                    "\n".join(failure_lines),
                    title="[bold red]Детали ошибки[/bold red]",
                    border_style="red",
                ))
                failure_lines = []
                in_failure = False
            else:
                failure_lines.append(line)


def run_tests():
    console.print(Panel(
        "[bold cyan]Запуск тестов[/bold cyan]",
        border_style="cyan",
        expand=False,
    ))

    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_all.py",
            "-v",
            "--tb=short",
            "--no-header",
            "--color=no",
        ],
        capture_output=True,
        text=True,
    )

    results = parse_results(result.stdout)
    summary = parse_summary(result.stdout)

    print_results(results, summary)

    if result.returncode != 0:
        print_errors(result.stdout)

    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
