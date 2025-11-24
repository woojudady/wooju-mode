"""Utility to create daily Wooju session markdown files on Windows/Google Drive.

Adjust BASE_DIR to match your local Google Drive path before running.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Dict

# TODO: Update this path to your local Google Drive root (the folder that contains
# "wooju-sessions"). For example, Path("G:/내 드라이브"). Use a raw string if your
# path contains backslashes (e.g., Path(r"G:\\My Drive")).
BASE_DIR = Path("G:/내 드라이브")

LLM_DEFAULT_MODELS: Dict[str, str] = {
    "gpt": "gpt-5.1",
    "claude": "claude-3.5",
    "gemini": "gemini-1.5-pro",
    "grok": "grok-2",
}


def choose_llm() -> str:
    """Prompt the user to select an LLM from the supported list."""
    valid_choices = set(LLM_DEFAULT_MODELS.keys())
    prompt_lines = [
        "어떤 LLM 세션을 생성할까요?",
        "  - gpt",
        "  - claude",
        "  - gemini",
        "  - grok",
    ]
    print("\n".join(prompt_lines))

    while True:
        choice = input("LLM을 입력하세요 (예: gpt): ").strip().lower()
        if choice in valid_choices:
            return choice
        print("지원하지 않는 LLM입니다. gpt / claude / gemini / grok 중에서 선택하세요.\n")


def prompt_model(llm: str) -> str:
    """Ask for a model name with a sensible default based on the LLM."""
    default_model = LLM_DEFAULT_MODELS[llm]
    user_value = input(
        f"{llm} 모델명을 입력하세요 [기본값: {default_model}]: "
    ).strip()
    return user_value or default_model


def build_session_content(llm: str, model: str, today: date) -> str:
    """Generate the markdown content for the session file."""
    date_iso = today.isoformat()
    date_compact = today.strftime("%Y%m%d")
    folder_hint = f"{llm}/{today.year}/{today.strftime('%m')}"

    metadata_block = (
        "---\n"
        f"date_iso: {date_iso}\n"
        f"date_compact: {date_compact}\n"
        f"year: {today.year}\n"
        f"month: {today.strftime('%m')}\n"
        f"day: {today.strftime('%d')}\n"
        f"llm: {llm}\n"
        f"model: {model}\n"
        "platform: chat.openai.com\n"
        f"folder_hint: {folder_hint}\n"
        "session_title:\n"
        "---\n"
    )

    body = (
        "\n"
        "## 1. 오늘 세션의 최종 목표\n"
        "- \n"
        "\n"
        "## 2. 주제별 기록\n"
        "\n"
        "> 여기에서 VSCode 스니펫(`wtopic`)으로 개별 주제를 추가할 거야.\n"
        "> 각 주제는 \"하나의 큰 질문/이슈\" 단위로 기록.\n"
    )

    return metadata_block + body


def create_session_file(llm: str, model: str) -> Path:
    """Create the daily session file with a unique name and return its path."""
    today = date.today()
    year_str = str(today.year)
    month_str = today.strftime("%m")
    base_folder = BASE_DIR / "wooju-sessions" / llm / year_str / month_str

    if not BASE_DIR.exists():
        raise FileNotFoundError(
            f"BASE_DIR가 존재하지 않습니다. Google Drive 동기화 경로를 확인하세요: {BASE_DIR}"
        )

    try:
        base_folder.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(
            f"세션 폴더를 생성할 수 없습니다: {base_folder}\n에러: {exc}"
        ) from exc

    stem = f"{today.strftime('%Y%m%d')}_{llm}_session"
    candidate = base_folder / f"{stem}.md"
    counter = 1
    while candidate.exists():
        candidate = base_folder / f"{stem}_{counter}.md"
        counter += 1

    content = build_session_content(llm, model, today)
    try:
        candidate.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise OSError(
            f"세션 파일을 작성할 수 없습니다: {candidate}\n에러: {exc}"
        ) from exc

    return candidate


def main() -> None:
    print("Wooju 세션 생성기를 시작합니다.\n")
    llm = choose_llm()
    model = prompt_model(llm)

    try:
        session_path = create_session_file(llm, model)
    except Exception as exc:  # noqa: BLE001 - show friendly message for any failure
        print(f"\n⚠️ 세션 생성 중 문제가 발생했습니다: {exc}")
        return

    print("\n✅ 세션 파일이 준비되었습니다!")
    print(f"경로: {session_path}")
    print("\n이 파일을 VSCode에서 열어 `wtopic` 스니펫으로 주제를 추가하세요.")


if __name__ == "__main__":
    main()
