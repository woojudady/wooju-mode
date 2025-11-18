# 🔐 Security Policy — Wooju Mode OS ∞

Wooju Mode OS ∞ is a behavioral operating system for LLMs, designed with accuracy, safety, 
and rule integrity as core principles.  
To maintain a trusted ecosystem, we take all security-related issues seriously.

This document explains how to report vulnerabilities safely and how maintainers will respond.

---

## 🛡 Supported Versions

Only the **latest version** receives security updates.

| Version | Status |
|--------|---------|
| v3.8   | Supported (active) |
| v3.7 ↓ | Deprecated |
| v3.6 ↓ | Deprecated |

Older versions may receive emergency fixes only for critical issues.

---

## 📣 How to Report a Security Issue

⚠️ **Do NOT create a public GitHub Issue.**  
공개 이슈에 보안 문제를 올리면 취약점이 외부에 노출될 수 있습니다.

대신 아래 방법을 사용해주세요:

### ✔ 1) Private Security Report (권장)
1. 저장소 상단 메뉴 → **“Security”** 탭 클릭  
2. **“Report a vulnerability”** 버튼 선택  
3. 취약점을 비공개 상태에서 제출  
4. 유지관리자만 열람 가능

### ✔ 2) Private Issue 방식 (대체 방법)
1. “Issues” 클릭  
2. “New Issue” → “Security Report (Private)” 선택  
3. 보안 문제를 템플릿에 맞게 작성

제출된 모든 보안 보고는 **외부에서 보이지 않으며**  
너(저장소 주인)와 GitHub 보안 시스템만 확인할 수 있어.

---

## 🧪 What to Include in Your Report

보안 문제를 분석하기 위해 아래 내용을 포함해 주세요:

- 문제 설명 (무엇이 잘못됐는지)
- 재현 방법(가능하면 단계별)
- 예상 동작 vs 실제 동작
- 심각도 추정 (low / medium / high / critical)
- 관련 규칙 또는 레이어 (예: Core Rule 3, A/B/C 모드 스위칭 등)
- 잠재적 영향
- 스크린샷 또는 예시 출력 (옵션)

---

## 🧩 Security-Relevant Issue Examples

아래 유형은 “보안 취약점”으로 간주됩니다:

- Core Layer 규칙이 비정상적으로 우회됨  
- A/B/C 모드가 외부 입력에 의해 강제 변경되는 현상  
- 웹 검증(Verification Layer)이 비정상적으로 꺼짐  
- 시스템이 위험하거나 부정확한 답변을 강제 출력  
- Rule Integrity가 깨져 출력이 예측 불가가 되는 상황  
- 특정 모듈이 다른 모듈의 동작을 비정상적으로 덮어씀  
- Injection prompt로 인해 안전성 규칙 위반 발생  

---

## ⚖ Maintainer Responsibilities

유지관리자는 다음을 준수합니다:

- 보고된 이슈를 **48시간 이내 검토**
- 문제 재현 및 영향 평가
- 적절한 수정 조치 수행
- 필요 시 임시 완화책 제공
- 패치 후 Release Notes에 기록
- 보고자의 신원 및 제보 내용은 전적으로 **비공개** 유지

---

## 🤝 Thanks

Wooju Mode OS ∞의 보안은  
사용자와 개발자 커뮤니티의 협력으로 유지됩니다.  
책임감 있는 취약점 제보는 모든 사용자에게 큰 도움이 됩니다.

Thank you for helping keep Wooju Mode OS ∞ safe!
