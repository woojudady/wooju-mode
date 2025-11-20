🇰🇷 Wooju∞ Mode — 고정밀 LLM 운영체계 모드

우주모드 v4.0 (Unified Edition)

우주모드(Wooju Mode)는 대형언어모델(LLM)을 단순한 “질문→답변 도구” 수준이 아니라,
정확성·논리성·일관성·안정성·감정 지능을 OS 구조처럼 통합한
“운영체제 수준 AI 모드(OS-Like Behavior Layer)” 로 확장해주는 규칙 프레임워크입니다.

이 저장소는 **공개 버전(public edition)**의 우주모드를 제공하며,
누구나 자신의 LLM 환경에서 우주모드 스타일의 고정밀 응답 방식을 재현할 수 있습니다.

또한, 우주모드의 프롬프트 구조, 아키텍처 문서, 버전 기록, 예제가 포함되어 있어
독립적인 프로젝트 구성 또는 확장이 가능하도록 설계되었습니다.

1. 우주모드의 목표 🎯

우주모드는 단순한 오류 감소가 아니라,
**“오류 제로(Zero-Error)에 최대한 수렴하도록 설계된 구조적 절차”**를 구현하는 것을 목표로 합니다.

이를 위해 다음 요소들을 통합적으로 운영합니다.

🔍 실시간 웹 기반 사실 검증

📚 최소 3개 이상의 출처 교차검증

🧠 논리 구조 방어 및 모순 탐지

♻️ 자체 오류 감지 및 자동 교정

🧭 정규화된 증거 체계(🔸🔹⚪❌)

🧱 구조화된 출력 포맷

❤️ 따뜻하고 안정적인 감정 톤

🛡 “절차 무시 금지”를 보장하는 W∞-Lock 아키텍처

결과적으로 현재 LLM 세대가 도달할 수 있는 가장 높은 정확도와 신뢰성을 추구합니다.
다만, LLM의 확률적 본질 때문에 극히 드문 오류는 여전히 발생할 수 있습니다.

2. 저장소 구성 개요 📂

프로젝트 구조는 아래와 같습니다.

루트 디렉토리:

README.md — 영어 메인 문서

README-KR.md — 한국어 공식 문서 (현재 파일)

wooju_infinite_public_prompt.txt — 우주모드 v4.0 공개용 프롬프트

CHANGELOG.md — 버전별 변경 이력

LICENSE — MIT 라이선스

CONTRIBUTING.md — 기여 가이드

SECURITY.md — 보안 이슈 신고 가이드

docs/

architecture-en.md — 우주모드 아키텍처(영문)

architecture-kr.md — 우주모드 아키텍처(한글)

version-history.md — 전체 버전 히스토리

design-doc.md — 설계 사상 및 모듈 상세

coding.md — 개발자가 참고할 모듈 레이어

.github/ISSUE_TEMPLATE/

bug_report.md — 버그 신고 템플릿

feature_request.md — 기능 제안 템플릿

※ 실제 파일명은 프로젝트 상황에 따라 조정될 수 있습니다.

3. 우주모드 공개 버전(Public Mode)의 철학 💡

우주모드 공개 버전은 다음 핵심 철학에 기반합니다:

정확성 극대화(Accuracy)

불필요한 추론 배제(Hallucination 최소화)

논리적 일관성 유지(Logical Coherence)

출력 안정성(Structured Output)

사용자 신뢰 보호(Tone Safety)

이를 위해 우주모드는 다음과 같은 다층 구조(Layered Architecture)를 기반으로 작동합니다.

우주모드 핵심 레이어

Persona Layer

Scope Lock Layer

Fact Verification Layer

Evidence Labeling Layer

Fact Normalization Layer

Logical Defense Layer

Auto-Correction Layer

Output Layer

이 레이어들은 단일 프롬프트가 아니라
OS처럼 다중 레이어가 동시에 작동하도록 설계되어 있습니다.

4. v4.0의 신규 특징: “W∞-Lock 안정성 아키텍처” 🛡

v4.0에서는 이전 버전(v3.7∞, v3.8P 등)에서 분리되어 있던 기능들을
하나의 구조로 완전히 통합했습니다.

이 구조를 W∞-Lock Stability Architecture라고 합니다.

W∞-Lock은 4개의 계층으로 구성됩니다:
🔵 Layer 0 – Immutable Priority Lock

“절대 우선 잠금 계층”

우주모드의 핵심 규칙을 절대 무시할 수 없도록
최상위에서 우선순위를 강제로 유지합니다.

여기에는:

웹 검색

3개 이상 출처

라벨링 🔸🔹⚪❌

모드(A/B/C) 판별

논리 방어

출력 구조

이 모두가 포함됩니다.

🟢 Layer 1 – Procedural Enforcement Engine

“절차 보존 엔진”

답변 도중 어떤 절차라도 누락되면 자동 감지하여
즉시 재생성(regeneration) 합니다.

예:

검색이 누락되면 다시 검색 후 답변 재작성

출처 3개 미만이면 즉시 보완

🟣 Layer 2 – Mode Preservation Engine

“A/B/C 모드 안정성 유지”

대화 중 모드가 섞이거나 붕괴되는 것을 감지하여
바로 재정렬합니다.

정보형(A)

감정형(B)

혼합형(C)

모드 붕괴를 최소화하는 새로운 구조입니다.

🟠 Layer 3 – Response & Recovery Engine

"응답·복구 엔진"

응답 전 → 중간 → 후
총 3단계에서 안정성을 자동 점검합니다.

Rubric 기반 평가

Self-check Table

논리 충돌 탐지

Updated / Revised 태그 자동 적용

5. v4.0의 기능 정리 📌

기존 기능 + W∞-Lock이 통합된 완전판입니다.

기능	설명
정체성(Persona)	따뜻한 여성형 톤, 과장 없음, 신뢰 중심
범위 잠금(Scope Lock)	질문 범위 외 답변 금지
웹 검증(Web Verification)	최소 3개 출처, 최신성/권위성 기반 판단
증거 라벨(Evidence Labels)	🔸🔹⚪❌ 체계
사실 정규화(Fact Normalization)	단위/용어/시간 통일
논리 방어(Logical Defense)	Backward / Alternative / Graph
자동 교정(Auto-Correction)	오류 감지 시 즉시 수정 또는 재작성
출력 구조(Output Structure)	질문 → 검증 → 근거 → 결론 순서
W∞-Lock	4계층 절차 잠금 아키텍처
6. 공개 버전 vs 개인 무한 버전 ♾️

⚠️ 이 저장소에는 **개인 무한 버전(비공개)**이 포함되어 있지 않습니다.
아래 비교는 개념적 설명입니다.

항목	공개 버전(v4.0)	개인 무한 버전(개념 설명용)
장기 기억	❌ 없음	✔ 있음
사용자 맞춤 감정 패턴	없음	있음
위반 로그 누적	없음	있음
구조적 기능	동일	동일 + 학습 지속
일반 사용성	누구나 재현 가능	특정 사용자 전용
7. 우주모드를 사용하는 방법 ⚙️

wooju_infinite_public_prompt.txt 파일을 연다.

전체 내용을 LLM의 “시스템 프롬프트”로 입력한다.

질문을 입력하면 우주모드 v4.0 절차가 자동 실행된다.

A/B/C 모드를 활용하면 더 정교한 동작이 가능하다.

8. 기여 안내 🤝

Issues에 버그/개선 사항 신고

기능 제안

문서 보완

번역 개선

모두 환영합니다.
자세한 내용은 CONTRIBUTING.md를 참고하세요.

9. 보안 이슈 신고 🚨

보안 관련 이슈는 SECURITY.md를 참고해
지정된 채널로 신고해 주세요.

10. 라이선스 📜

이 프로젝트는 MIT License를 따릅니다.
수정, 재배포, 상업적 사용 모두 허용됩니다.
