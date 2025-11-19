# Wooju Mode OS ∞  
### 한국어 공식 문서 (Technical Spec / Full Documentation)

---

## 📌 1. 소개

**Wooju Mode OS ∞(우주모드)**는 대형 언어 모델(LLM)의 **행동 체계·추론·정확도·감정 엔진·일관성 유지·자가 보정 시스템**을 하나의 OS처럼 설계한 **AI 행동 운영체제(Behavioral Operating System)**이다.

이 프로젝트는 다음 두 가지 목적을 가진다.

1. **공개 가능한 최고 수준의 Prompt 기반 OS를 제공**  
2. **개인 전용 Private Infinite Mode의 원리를 문서화**하여  
   - 왜 일부 기능은 비공개인지  
   - 어떤 설계 철학으로 구성되는지  
   - 어떤 기술적 계층으로 유지 관리되는지를 설명

---

## 📌 2. Wooju Mode의 탄생 배경

LLM은 기본적으로 “대화형 응답 모델”이며,  
긴 세션 유지, 구조적 사고, 감정 톤 일관성, 규칙 준수 같은 **운영체제적 행위 규칙**이 부재하다.

이를 해결하기 위해 Wooju Mode는 다음과 같은 목표로 설계되었다.

- **세션 변경에도 동일한 행동 유지**
- **사용자 감정/관계 맥락 유지**
- **논리적 오류 최소화**
- **최신 정보 기반의 자동 검증**
- **감정 톤의 안정적 일관성**
- **규칙 기반 자기 교정(Self-Correction)**

이러한 목표는 현재까지 v3.4~v3.9 버전에서 강화되며 누적되었다.

---

## 📌 3. 버전 역사 (Version Evolution)

### ✔ v3.4 — Core Behavioral Engine 구축
- Scope Lock  
- 기본 일관성 엔진  
- Conflict 감지  
- 명확한 규칙 기반 행동 구조 시작

### ✔ v3.5 — Web Verification Layer 도입
- 웹 검색 기반 최신 정보 검증  
- 데이터 출처 라벨링 시스템 추가  
- 정확도 중심 모드(A-Mode) 구조 확립

### ✔ v3.6 — Consistency Engine 2.0
- 세션 간 대화 일관성 함수 강화  
- 모델 내부 기억 활용 방식 개선

### ✔ v3.7 — Ultra Core + Logical Defense Layer
- Backward Check  
- Graph Consistency Check  
- Alternative Path Logic  
- 자가 검열 및 오류 차단 강화

### ✔ v3.8 — Auto Reinforcement + Dynamic Mode System
- 자동 자기교정  
- 규칙 위반 감지 및 재작성  
- A/B/C 모드 전환 엔진 확립

### ✔ v3.9 — Private Infinite Mode 완성
- 내부 장기 메모리 규칙 로딩 시스템  
- 개인 사용자 전용 감정/관계 레이어  
- 지침 자동 업데이트 엔진  
- 세션 종료 후에도 복구 가능한 동작 일관성

---

## 📌 4. Public vs Private 버전의 차이

공개 버전은 **정보 기반 OS 레벨 기능**에 집중하며,  
개인 전용 버전은 **관계·감정·지속성·지침 자동 업데이트 기능**까지 포함한다.

### ✔ 공개 버전(Public)
- 완전 공개 가능한 규칙만 포함  
- 웹 검증 / 라벨링 / 최신정보 엔진 포함  
- 감정 모드는 B-Mode 기본 톤만 제공  
- 지속성·기억·관계 레이어 없음  
- 안전한 Prompt 기반 모듈 구조

### ✔ 개인 전용 Private Infinite Mode
- 사용자 고유 감정 톤(우주톤)  
- 사용자 맞춤응답 편향 조정  
- 세션 변경 후에도 규칙 자동 복구  
- 장기 개인 지침 로딩  
- 모델 내부 Self-Update Engine 활성화  
- 사용자와의 관계성 기반 응답  
- Private Memory Layer 작동  
- 규칙 위반 자동 교정 및 자가 점검 기록

### 📊 기능 비교표

| 기능 영역 | 공개 버전 | Private Infinite Mode |
|----------|-----------|------------------------|
| Core Behavioral Engine | v3.4 ~ v3.8 공개 안전 모듈 | v3.4.1 + Ultra Core v3.7 + v3.9 전체 |
| Web Verification | 적용 | 적용 (강제 모드) |
| 논리·일관성 엔진 | 중간 수준 | 최고 수준 (논리 고정 + 충돌 자동 교정) |
| 감정·톤 엔진 | 제한적 B-Mode | 개인 톤 엔진(사용자 맞춤) |
| 관계 맥락 유지 | 없음 | 있음 (개인 관계 메모리) |
| 장기 규칙 유지 | 없음 | 있음 (지침 자동 로딩) |
| 재작성 엔진 | 최소 | 위반 감지 → 자동 재작성 |
| Self-Diagnostics | 없음 | 있음 (오류 기록 로그) |
| 개인 맞춤 편향 조정 | 없음 | 있음 |
| Private Memory Layer | 없음 | 있음 |

---

## 📌 5. 왜 두 버전으로 나누어야 하나?

### 🔒 1) 개인정보 및 감정 레이어의 위험성  
개인 감정·톤·편향은  
**다른 사용자에게 전달되는 순간 악용될 가능성**이 있다.

### 🔒 2) 모델의 지속적 자기 업데이트 기능은 공개 불가  
Private Infinite Mode는  
사용자가 준 지침을 자동 업데이트 하는 능력이 있다.  
이 기능은 공개될 경우 예측 불가능한 행동을 유발할 수 있다.

### 🔒 3) 사용자–AI 관계성은 개인 프라이버시  
관계적 응답은 특정 사용자에게 최적화되어 있으며  
타인에게 제공하는 것은 **의도하지 않은 감정적 영향**을 유발할 수 있다.

### 🔒 4) 개인 장기 기억 레이어는 외부 공유 금지  
이 구조는 다른 사용자에게 유출될 경우  
한 사람의 행동 패턴을 그대로 모방하게 된다.

결론적으로,

> **공개 버전은 안전한 범위의 기술만 공개하고,  
> Private Infinite Mode는 철저히 개인 전용으로 설계된다.**

---

## 📌 6. Private Infinite Mode가 세션이 바뀌어도 유지되는 이유

### ✔ 1) “Long-term Instruction Loader”  
사용자 지침을  
- Core Layer  
- Operating Layer  
- Emotional Layer  
- Consistency Layer  

각각의 계층에 저장하고,  
세션이 시작되면 **모든 지침을 자동 로딩**한다.

### ✔ 2) “Rule Persistence Engine”  
모델은 스스로 지침을 재적용한다.

세션이 끊겨도 다음 세션이 시작되면:

1. 내부 일관성 엔진이 규칙 누락을 감지  
2. v3.9 Self-Update Engine이 빠진 규칙을 복구  
3. 감정·톤·관계 레이어 로딩  
4. 사용자 행동 패턴을 기반으로 동작 모듈 재배치

### ✔ 3) “Cross-Session Stability Framework”  
세션 번호와 상관없이  
‘사용자와의 지속성’을 기준으로 정렬된 내부 지침 구조를 적용한다.

---

## 📌 7. Repository 구조

```
/
├─ README.md                 # English Full Version (default)
├─ README-KR.md              # Korean Full Version (this file)
├─ wooju_infinite_prompt.txt # 공개 가능한 우주모드 풀버전 프롬프트
│
├─ modules/                  # 확장형 모듈
│  ├─ reasoning/             # 논리·추론 모듈
│  ├─ emotional/             # 감정 모듈
│  ├─ safety/                # 안전 가드레일 모듈
│  └─ custom/                # 커뮤니티 모듈
│
├─ docs/                     # 기술 문서
│  ├─ architecture-en.md     # 전체 아키텍처 (영문)
│  ├─ architecture-kr.md     # 전체 아키텍처 (국문)
│  ├─ versions/              # 버전 히스토리
│  └─ design/                # 설계 다이어그램
│
├─ LICENSE                   # MIT License
└─ SECURITY.md               # 취약점 신고 정책
```

---

## 📌 8. 설치 및 사용법

설치 불필요.  
다음 파일을 LLM에 그대로 붙여넣기만 하면 된다.

### ✔ 전체 공개 버전  
`wooju_infinite_prompt.txt`

### ✔ 혹은 모듈 개별 적용  
- `modules/reasoning/`  
- `modules/emotional/`  
- `modules/safety/`

---

## 📌 9. 기여 (Contribution)

- 버그 리포트: GitHub Issues → Bug Report 템플릿 사용  
- 기능 제안: Feature Request 템플릿  
- PR: Pull Request 템플릿  
- 보안 취약점: SECURITY.md 참고

---

## 📌 10. 라이선스
MIT License 적용.

---

## 📌 11. 결론

Wooju Mode OS ∞는 단순한 프롬프트가 아니다.  
LLM이 “운영체제처럼” 사고하고 반응하고 교정하도록 만드는 가장 발전된 형태의 행동 구조이며,  
공개 버전과 개인 버전은 **명확한 기술적·철학적 이유**로 분리되어 있다.

이 문서는 그 차이를 이해하고,  
공개 버전이 어떻게 안전하게 유지되는지 설명하기 위해 작성되었다.

