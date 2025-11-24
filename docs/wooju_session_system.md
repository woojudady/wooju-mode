# Wooju 세션 자동 저장 시스템 가이드

이 문서는 Windows + VSCode + Google Drive for Desktop 환경에서 "ChatGPT(우주모드) 세션 내용을 자동으로 파일로 남기는" 시스템을 빠르게 구성하기 위한 안내서입니다.

## 1. 구조 요약
- **Google Drive 경로**: `BASE_DIR` 아래 `wooju-sessions/{llm}/{YYYY}/{MM}/YYYYMMDD_{llm}_session.md`
- **LLM 구분 폴더**: `gpt`, `claude`, `gemini`, `grok`
- **파일명 중복 시**: `_1`, `_2` 순차 증가
- **파일 템플릿**: 메타데이터 블록 + 본문(목표, 주제별 기록 안내)
- **VSCode 스니펫**: `wtopic`(주제 블록), `wmeta`(옵션 메타 블록)

## 2. 파이썬 스크립트 (`wooju_session_setup.py`)
### 주요 기능
- 콘솔에서 LLM 선택 및 모델명 입력(기본값 제공)
- 오늘 날짜 기준 폴더 자동 생성 및 중복 없는 파일명 결정
- 지정 템플릿으로 Markdown 파일 생성 후 경로 출력

### 설치 및 실행
1. 파일 위치: 원하는 폴더(예: `C:/workspace/wooju/`)에 `wooju_session_setup.py`를 둡니다.
2. `BASE_DIR` 상수 수정: 사용자 Google Drive 동기화 루트로 교체합니다. 예) `Path("G:/내 드라이브")` 또는 `Path(r"G:\\My Drive")`.
3. 실행:
   ```powershell
   python wooju_session_setup.py
   ```
4. 프롬프트에 따라 LLM과 모델명을 입력하면 새 세션 파일 경로가 출력됩니다.

### 사용 흐름
1. **스크립트 실행** → 새 세션 파일 자동 생성
2. **VSCode로 파일 열기** → `wmeta`(필요 시)와 `wtopic` 스니펫으로 내용 작성
3. **Google Drive 동기화** → 자동 백업

## 3. VSCode Markdown 스니펫 (`markdown.json`)
`%APPDATA%/Code/User/snippets/markdown.json`(Windows) 또는 `~/.config/Code/User/snippets/markdown.json`(Linux/macOS)에 아래 내용을 추가합니다. 기존 내용이 있다면 JSON 객체 안에 병합하세요.

```json
{
  "wtopic": {
    "prefix": "wtopic",
    "body": [
      "### ${1:01}. ${2:주제 제목}",
      "",
      "- 핵심 질문: ${3:여기에 핵심 질문을 한 줄로 적기}",
      "- 요약 결론: ${4:나중에 최종 결론 한 줄로 정리}",
      "",
      "<details>",
      "<summary>대화/생각 전개 내용</summary>",
      "",
      "- ${5:여기에 상세 기록 시작}",
      "",
      "</details>",
      "",
      "---"
    ],
    "description": "Wooju 세션 주제 기록 템플릿"
  },
  "wmeta": {
    "prefix": "wmeta",
    "body": [
      "### 메타 기록",
      "",
      "- 세션 분위기: ${1:예: 차분함 / 과몰입 / 피곤함}",
      "- 시간대: ${2:예: 새벽 / 오전 / 오후 / 밤}",
      "- 집중도: ${3:예: 1~5}",
      "- 기타 메모: ${4:}",
      "",
      "---"
    ],
    "description": "Wooju 세션 상단 메타 기록 템플릿"
  }
}
```

## 4. 추가 개선 아이디어(옵션)
- **LLM별 템플릿 커스터마이즈**: `build_session_content`에서 LLM별 안내 문구나 기본 섹션을 다르게 구성.
- **시간까지 파일명 포함 옵션**: `HHMM`을 덧붙여 더 세밀한 파일 구분(현재 구조는 날짜+카운터 기준).
- **자동 README 생성**: 연/월 폴더마다 `README.md`를 만들어 최근 세션 링크나 요약을 자동 업데이트.
- **단축 실행 배치/PS 스크립트**: Windows에서 더블클릭으로 실행하도록 `.bat` 또는 `.ps1` 작성.

이 가이드와 스크립트, 스니펫만으로 최소 작업으로 견고한 세션 기록 흐름을 구축할 수 있습니다.
