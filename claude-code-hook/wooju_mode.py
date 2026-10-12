"""우주모드 훅 — https://github.com/woojudady/wooju-mode (v4.0) 규칙을 훅으로 강제한다.

원문은 챗봇 시스템 프롬프트다. 프롬프트는 모델이 잊으면 안 돈다. 여기서는
기계가 확인할 수 있는 부분만 골라 Stop 훅으로 검사한다.

  inject  : 매 사용자 메시지마다 규칙 요약을 컨텍스트에 넣는다     (UserPromptSubmit)
  check   : 응답을 끝내려 할 때 최종 답을 검사한다                 (Stop)
            --warn 이면 막지 않고 알리기만 한다
  measure : 과거 대화 기록에 돌려 숫자 · 파일 근거 위반 비율을 잰다 (오프라인)

훅이 판정할 수 있는 건 참 · 거짓이 아니라 '형식'과 '추적 가능성'이다.
  - 🔸 라고 한 근거를 이 세션에서 실제로 열어봤나
  - 🔸 줄의 숫자가 이 세션 도구 출력 · 사용자 글에 실제로 있나
  - 웹 근거가 서로 다른 도메인 3개 이상인가
원문의 말투(페르소나) 규칙은 기계 검사가 안 되고 할루시네이션과 무관해 뺐다.
'A 모드 = 무조건 웹 검색'은 코드 작업에 안 맞아 근거를 파일 · 명령 · URL 로 넓혔다.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

# 시험은 WOOJU_LOG 로 다른 파일에 쓴다 — 실제 경고 기록을 지우지 않게(10/11 시험 뒤 삭제로 실기록 유실)
LOG = Path(os.environ.get("WOOJU_LOG") or Path(__file__).with_name("wooju_log.jsonl"))

STATE = Path(os.environ.get("WOOJU_STATE") or Path(__file__).with_name("state"))  # 표시 버퍼 · 검토 판정 (git 제외)
# 시험은 WOOJU_FAKE_REVIEW=ok|rejected 로 진짜 검토자(claude -p) 대신 가짜 판정을 쓴다 — 10/12 시험이 검토자를 13번 불렀다
FAKE_REVIEW = os.environ.get("WOOJU_FAKE_REVIEW")
NESTED = bool(os.environ.get("WOOJU_NESTED"))  # 훅이 띄운 검토자 안에서는 우주모드 훅을 모두 끈다(무한 반복 방지)
REVIEW_TIMEOUT = 270                           # 검토자 한도. 훅 timeout 은 REVIEW_TIMEOUT + 60 (기다림 + 여유)
POLL = 1.0                                     # 다른 훅의 검토를 기다릴 때 판정 확인 간격(초)
HOLD_HEAD = re.compile(r"^\W*(범위|scope|모드|mode|revised|updated)\W*[:：]", re.I)

RULES = """\
[우주모드 v4.0 — 최종 답은 화면에 나가기 전에 검토된다. 반려되면 사용자는 그 답을 보지 못한다]
1. 최종 답 맨 앞 두 줄:
     범위: <이번 질문의 범위 한 문장 — 이 밖은 답하지 않는다>
     모드: A | B | C      (A 정보·사실·코드 / B 감정·잡담 / C 해석·판단)
   B 는 도구를 안 쓰고 사실 주장(숫자 · 파일)이 없을 때만.
2. A · C 모드: 사실 주장 줄 앞에 라벨 하나
     🔸 확인됨 — 이 세션 도구 출력으로 확인. 줄 끝에 [근거: 파일:줄 | 명령 | URL | 이미지]
     🔹 공식 출처 — 공식 문서 · 기관. 줄 끝에 [근거: URL]
     ⚪ 해석 · 계산 · 추론        ❌ 확인 못 함
   ⚪ · ❌ 를 🔸 처럼 쓰지 않는다. 🔸 줄의 숫자는 근거 출력에 그대로 있어야 한다(계산한 값은 ⚪).
   [근거: 파일:줄] 은 이 세션에서 그 줄을 실제로 열었거나 grep 으로 본 것만.
   세 자리 이상 숫자가 든 줄은 반드시 라벨을 단다(범위 · 모드 줄 제외).
   ⚪ 줄의 세 자리 이상 숫자는 계산식(`455 = 580 − 125`)이나 `가정:` 을 같이 적는다.
3. 웹 근거(URL)를 쓰면 서로 다른 도메인 3개 이상. 못 채우면 `출처 부족: <이유>` 줄로 밝힌다.
4. A 모드는 `검증: <무엇을 어떻게 확인했나>` 줄과 `결론: <한 줄>` 줄. C 모드는 `결론:` 줄.
5. 논리 방어: 결론 → 근거 역추적, 다른 경로로 한 번 더, 앞서 확인한 내용과 모순 없는지.
6. 검토에서 반려되면 고친 부분만이 아니라 **답 전체를 다시** 쓴다(반려된 답은 화면에 안 나갔다).
   맨 위 `범위:` 줄 바로 아래에 `Revised: <무엇을 고쳤나 한 줄>` 을 붙인다.
   같은 질문에서 두 번째 반려부터는 막지 않고, 검토자 지적을 경고로 붙여 그대로 보인다.
"""

LABELS = "🔸🔹⚪❌"
NUM_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
FILE_LINE_RE = re.compile(
    r"([\w./\\~:-]*?[\w-]+\.(?:py|md|json|jsonl|txt|csv|ps1|js|ts|tsx|toml|ya?ml|ini|bat|cfg|html|css|sql))"
    r":(\d+)"
)
URL_RE = re.compile(r"https?://[^\s\])>'\"`]+")
FENCE_RE = re.compile(r"```.*?```", re.S)
NON_PROMPT = ("<command-name>", "<command-message>", "<local-command-stdout>", "<local-command-stderr>",
              "<local-command-caveat>", "<bash-input>", "<bash-stdout>", "<bash-stderr>")
HEAD_RE = {
    "scope": re.compile(r"^\W*(범위|scope)\W*[:：]", re.I | re.M),
    "mode": re.compile(r"^\W*(모드|mode)\W*[:：]\s*\**\s*([ABC])\b", re.I | re.M),
    "verify": re.compile(r"^\W*(검증|verification)\W*[:：]", re.I | re.M),
    "concl": re.compile(r"^\W*(결론|conclusion)\W*[:：]", re.I | re.M),
    "short": re.compile(r"^\W*출처\s*부족\W*[:：]", re.M),
}


# ── 대화 기록 읽기 ────────────────────────────────────────────────────────────

def _content(d: dict):
    return (d.get("message") or {}).get("content")


def _text_of(c) -> str:
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        out = []
        for b in c:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    out.append(b.get("text") or "")
                elif b.get("type") == "tool_result":
                    out.append(_text_of(b.get("content")))
        return "\n".join(out)
    return ""


def _is_prompt(d: dict) -> bool:
    """사람이 보낸 메시지(도구 결과 · 메타 줄 제외)."""
    if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain") or d.get("isCompactSummary"):
        return False
    c = _content(d)
    # 슬래시 명령 · ! 셸 출력은 모델 응답을 부르지 않는다 — 턴 경계가 아니다
    if _text_of(c).lstrip().startswith(NON_PROMPT):
        return False
    if isinstance(c, str):
        return True
    return isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "text" for b in c) \
        and not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c)


def _load(path: Path) -> list[dict]:
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return [r for r in rows if not r.get("isSidechain")]


class Session:
    """한 시점까지의 세션 증거: 도구 입출력 · 사용자 글 · 읽은 파일 범위."""

    def __init__(self) -> None:
        self.evidence: list[str] = []   # 도구 출력 + 사용자 글 (숫자 대조용)
        self.tool_io: list[str] = []    # 도구 입력 + 출력 (파일 · URL 대조용)
        self.reads: list[tuple[str, int, int]] = []  # (경로 소문자, 시작, 끝)
        self.pairs: list[tuple[str, str]] = []       # (도구 입력 소문자, 그 출력) — grep -n · sed -n 대조용
        self._pending: dict[str, str] = {}
        self.tool_calls = 0
        self.images = 0
        self.wooju_feedback = False  # 이번 턴에 우주모드 훅이 답을 반려했나

    def add(self, d: dict) -> None:
        c = _content(d)
        if d.get("type") == "user":
            self.evidence.append(_text_of(c))
            if isinstance(c, list):
                for b in c:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "image":
                        self.images += 1
                    if b.get("type") == "tool_result":
                        out = _text_of(b.get("content"))
                        self.tool_io.append(out)
                        if isinstance(b.get("content"), list):
                            self.images += sum(1 for x in b["content"]
                                               if isinstance(x, dict) and x.get("type") == "image")
                        self.pairs.append((self._pending.pop(b.get("tool_use_id"), ""), out))
        elif d.get("type") == "attachment":
            a = d.get("attachment") or {}
            self.evidence.append(_text_of(a.get("prompt") or a.get("content") or ""))
        elif d.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    self.tool_calls += 1
                    inp = b.get("input") or {}
                    self.tool_io.append(json.dumps(inp, ensure_ascii=False))
                    self._pending[b.get("id")] = json.dumps(inp, ensure_ascii=False).lower()
                    if b.get("name") == "Read" and inp.get("file_path"):
                        start = int(inp.get("offset") or 1)
                        end = start + int(inp.get("limit") or 2000)
                        self.reads.append((_norm(inp["file_path"]), start, end))

    def blobs(self):
        return "\n".join(self.evidence).replace(",", ""), "\n".join(self.tool_io)


def _norm(p: str) -> str:
    return p.replace("\\", "/").lower().rstrip("/")


def turns(rows: list[dict]):
    """(세션 증거 스냅샷, 최종 답 글, 이번 턴 도구 호출 수) 를 턴마다 낸다."""
    sess = Session()
    i, n = 0, len(rows)
    while i < n:
        if not _is_prompt(rows[i]):
            sess.add(rows[i])
            i += 1
            continue
        sess.add(rows[i])
        sess.wooju_feedback = False
        j = i + 1
        calls_before = sess.tool_calls
        final: list[str] = []
        while j < n and not _is_prompt(rows[j]):
            d = rows[j]
            c = _content(d)
            if d.get("type") == "assistant" and isinstance(c, list):
                if any(isinstance(b, dict) and b.get("type") == "tool_use" for b in c):
                    final = []
                final += [b.get("text") or "" for b in c if isinstance(b, dict) and b.get("type") == "text"]
            elif d.get("type") == "user":
                final = []  # 도구 결과 · 훅 반려(isMeta) 뒤의 글만 최종 답
                if isinstance(c, str) and c.startswith("Stop hook feedback") and "[우주모드" in c:
                    sess.wooju_feedback = True
            sess.add(d)
            j += 1
        yield sess, "\n".join(t for t in final if t.strip()), sess.tool_calls - calls_before
        i = j


# ── 검사 ─────────────────────────────────────────────────────────────────────

def _num_found(num: str, ev: str) -> bool:
    k = num.replace(",", "")
    return re.search(r"(?<![\d.])" + re.escape(k) + r"(?![\d])", ev) is not None


def _file_line_ok(path: str, line: int, sess: Session, tool_io: str) -> bool:
    base = _norm(path).rsplit("/", 1)[-1]
    for rp, s, e in sess.reads:
        if (rp.endswith("/" + base) or rp == base) and s <= line < e:
            return True
    if re.search(re.escape(base) + r"[:\-](?:\s*)" + str(line) + r"\b", tool_io, re.I):
        return True
    # 한 파일만 grep -n / Grep 하면 출력에 파일명 없이 '2662:' 로만 찍힌다 → 명령에 파일명이 있으면 인정
    # sed -n 3009,3020p 파일 은 범위로 인정
    own = re.compile(r"(?m)^\s*" + str(line) + r"[:\-\t]")
    for inp, out in sess.pairs:
        if base not in inp:
            continue
        if own.search(out):
            return True
        for a, b in re.findall(r"sed -n '?(\d+),(\d+)p", inp):
            if int(a) <= line <= int(b):
                return True
    return False


def _evidence_of(line: str) -> str:
    m = re.search(r"\[근거\s*[:：](.*?)\]", line)
    return m.group(1) if m else ""


def _nums3(ln: str) -> list[str]:
    """줄의 세 자리 이상 숫자(근거 · 파일:줄 · URL 안의 숫자는 뺀다). 두 자리는 긴 출력 어디에나 있어 대조 의미가 없다."""
    body = re.sub(r"\[근거\s*[:：].*?\]", "", ln)
    body = FILE_LINE_RE.sub("", URL_RE.sub("", body))
    return [m.group() for m in NUM_RE.finditer(body) if len(re.sub(r"\D", "", m.group())) >= 3]


def _scoped_evidence(ln: str, sess: Session) -> str:
    """근거로 든 파일 · URL 이 있으면 그 도구 출력만, 없으면 세션 전체(도구 출력 + 사용자 글)."""
    ev = _evidence_of(ln)
    keys = [_norm(p).rsplit("/", 1)[-1] for p, _ in FILE_LINE_RE.findall(ev)]
    keys += [urlparse(u).netloc.lower().removeprefix("www.") for u in URL_RE.findall(ev)]
    keys = [k for k in keys if k]
    if keys:
        outs = [out for inp, out in sess.pairs if any(k in inp or k in out.lower() for k in keys)]
        if outs:
            return "\n".join(outs).replace(",", "")
    return sess.blobs()[0]


def check_numbers(lines: list[str], sess: Session) -> list[str]:
    bad = []
    for ln in lines:
        hay = _scoped_evidence(ln, sess)
        bad += [x for x in _nums3(ln) if not _num_found(x, hay)]
    return bad


def check_files(text: str, sess: Session) -> list[str]:
    _, tio = sess.blobs()
    return [f"{p}:{n}" for p, n in FILE_LINE_RE.findall(text) if not _file_line_ok(p, int(n), sess, tio)]


def check(text: str, sess: Session, turn_calls: int) -> list[str]:
    errs: list[str] = []
    body = FENCE_RE.sub("", text)
    if sess.wooju_feedback and not re.search(r"\b(Updated|Revised)\s*[:：]", body):
        errs.append("우주모드 반려 뒤 다시 쓴 답에 `Updated:` / `Revised:` 표시가 없다.")
    mode_m = HEAD_RE["mode"].search(body)
    if not HEAD_RE["scope"].search(body):
        errs.append("`범위:` 줄이 없다 (Scope Lock).")
    if not mode_m:
        errs.append("`모드: A|B|C` 줄이 없다.")
        return errs
    mode = mode_m.group(2).upper()
    lines = body.splitlines()

    if mode == "B":
        if turn_calls:
            errs.append(f"모드 B 인데 이번 턴에 도구를 {turn_calls}번 썼다 — 정보 작업이면 A.")
        if FILE_LINE_RE.search(body) or any(len(re.sub(r"\D", "", m.group())) >= 2 for m in NUM_RE.finditer(body)):
            errs.append("모드 B 인데 숫자 · 파일 같은 사실 주장이 있다 — A 또는 C 로 쓰고 라벨을 단다.")
        return errs

    if not any(ch in body for ch in LABELS):
        errs.append(f"모드 {mode} 인데 근거 라벨(🔸🔹⚪❌)이 하나도 없다.")
    if mode == "A" and not HEAD_RE["verify"].search(body):
        errs.append("모드 A 인데 `검증:` 줄이 없다.")
    if not HEAD_RE["concl"].search(body):
        errs.append(f"모드 {mode} 인데 `결론:` 줄이 없다.")

    # 라벨 없는 줄은 검사를 빠져나간다 — 세 자리 이상 숫자가 든 줄은 라벨 필수
    unlabeled = [ln.strip()[:50] for ln in lines
                 if _nums3(ln) and not any(ch in ln for ch in LABELS)
                 and not (HEAD_RE["scope"].match(ln) or HEAD_RE["mode"].match(ln))]
    if unlabeled:
        errs.append("세 자리 이상 숫자가 든 줄에 라벨이 없다: " + " / ".join(unlabeled[:3]))
    # ⚪ 로 숫자 대조를 피하지 못하게 — 계산식이나 가정을 밝힌다
    loose = [ln.strip()[:50] for ln in lines
             if "⚪" in ln and "🔸" not in ln and "🔹" not in ln and _nums3(ln)
             and not re.search(r"=|가정", ln)]
    if loose:
        errs.append("⚪ 줄의 세 자리 이상 숫자에 계산식(=)이나 `가정:` 이 없다: " + " / ".join(loose[:3]))

    claim = [ln for ln in lines if "🔸" in ln or "🔹" in ln]
    if claim and sess.tool_calls == 0:
        errs.append("🔸/🔹 를 썼는데 이 세션에서 도구를 한 번도 안 썼다 — 확인한 게 없으면 ⚪/❌.")
    no_ev = [ln.strip()[:60] for ln in claim if not _evidence_of(ln)]
    if no_ev:
        errs.append("🔸/🔹 줄에 [근거: …] 가 없다: " + " / ".join(no_ev[:3]))

    img_lines = [ln for ln in claim if "이미지" in _evidence_of(ln)]
    if img_lines and not sess.images:
        errs.append("[근거: 이미지] 를 썼는데 이 세션에 이미지가 없다.")
    # 스크린샷에서 읽은 숫자는 글자 대조가 안 된다 — 이미지가 실제로 있을 때만 숫자 대조를 건너뛴다
    num_lines = [ln for ln in lines if "🔸" in ln and not (sess.images and ln in img_lines)]
    bad_nums = check_numbers(num_lines, sess)
    if bad_nums:
        errs.append("🔸 줄의 숫자가 이 세션 도구 출력 · 사용자 글에 없다(계산값이면 ⚪): "
                    + ", ".join(sorted(set(bad_nums))[:8]))

    bad_files = check_files("\n".join(_evidence_of(ln) for ln in claim), sess)
    if bad_files:
        errs.append("근거로 든 파일:줄 을 이 세션에서 열거나 grep 한 적이 없다: " + ", ".join(bad_files[:6]))

    urls = [u for ln in claim for u in URL_RE.findall(_evidence_of(ln))]
    if urls:
        _, tio = sess.blobs()
        doms = {urlparse(u).netloc.lower().removeprefix("www.") for u in urls}
        unseen = sorted(d for d in doms if d and d not in tio.lower())
        if unseen:
            errs.append("근거 URL 도메인을 이 세션에서 검색 · 열람한 적이 없다: " + ", ".join(unseen[:5]))
        if len(doms) < 3 and not HEAD_RE["short"].search(body):
            errs.append(f"웹 근거 도메인이 {len(doms)}개 — 3개 이상이거나 `출처 부족: <이유>` 줄로 밝힌다.")
    return errs


# ── 근거 검토 에이전트 (공식 Stop agent 훅) ─────────────────────────────────────
# agent 훅은 조건부 실행 기능이 없다 → 조건은 지시문 안에 둔다. 경고 모드도 없다(ok:false = 반려).
# 검토자 모델은 백그라운드 기본 모델이 아니라 Opus 로 고정(2026-10-11 사용자 결정).
REVIEW_MODEL = "claude-opus-5-5"
REVIEW_PROMPT = """\
너는 우주모드 근거 검토자다. 파일을 고치지 않는다. 입력(JSON): $ARGUMENTS
answer 는 아직 사용자에게 보이지 않은 최종 답이다. transcript_path 는 그 답을 쓴 세션의 대화 기록(도구 출력 포함)이다.
지적할 것은 아래 단계에서 모두 모아 한 번에 돌려준다.

0) answer 에 `모드: B` 줄이 있으면 ok=true 로 끝낸다(B 의 형식 위반은 다른 훅이 기록한다).

1) [반려 뒤 다시 쓴 답] previous_rejection 이 비어 있지 않으면, 이 answer 는 그 반려를 받고 다시 쓴 답이다.
   'Revised:' 줄이 없으면 지적한다. previous_rejection 이 짚은 문제가 실제로 고쳐졌는지도 본다.

2) [라벨 없는 사실 주장 — 도구를 쓰지 말고 글만 읽는다]
   라벨(🔸🔹⚪❌)이 없는 줄과 ⚪ 줄 가운데, 다음을 확인된 사실처럼 단정하는 줄을 찾는다:
     코드 · 파일 · 데이터의 내용, 수치, 바깥 세상의 사실, '완료했다 · 통과했다 · 확인했다 · 동작한다' 같은 작업 보고.
   제외: 범위 · 모드 · 검증 줄 / 제안 · 계획 · 질문 · 의견 · 앞으로 할 일 / 위 라벨 줄을 그대로 요약한 결론 줄 /
         표의 머리줄 · 구분줄 / 코드 블록 / 사용자가 한 말을 되풀이한 것.
   있으면 지적: "라벨 없는 사실 주장: <줄 요약> — 🔸/🔹 근거를 달거나 ⚪(해석) · ❌(확인 못 함)로 밝힐 것".
   ⚪ 줄인데 추론이 아니라 확인된 사실처럼 단정하면 같은 식으로 지적한다.

3) [근거 대조] 🔸/🔹 줄이 3개 이상이거나, 세 자리 이상 숫자가 든 🔸 줄이 있을 때만 한다.
   🔸/🔹 줄마다 [근거: …] 를 직접 대조한다.
   - 파일:줄 → Read 로 그 줄 앞뒤를 열어, 주장(숫자 · 이름 · 동작)이 실제로 그렇게 적혀 있는지 본다.
   - 명령 · URL → transcript_path 파일을 Grep 해 그 도구 출력을 찾아 대조한다.
   - 이미지 → 대조할 수 없으니 넘어간다.
   근거가 주장을 뒷받침하지 않으면 지적: "<틀린 줄 요약> — 근거에 실제로 적힌 것: <내용>. 고치거나 ⚪/❌ 로 낮출 것".
   표현 차이 · 해석의 여지는 문제 삼지 않는다. 확인한 사실과 다른 것만 잡는다.

4) 지적이 하나라도 있으면 ok=false, reason="<지적 목록>". 없으면 ok=true, reason="".
"""
REVIEW_SCHEMA = json.dumps({"type": "object", "properties": {"ok": {"type": "boolean"}, "reason": {"type": "string"}},
                            "required": ["ok", "reason"]})


# ── 표시 전 검토 (MessageDisplay) ────────────────────────────────────────────────
# 공식 문서: MessageDisplay 는 훅이 끝날 때까지 그 줄 묶음의 표시를 붙잡고, displayContent 로 화면 글자를 바꾼다.
# 막는 기능은 없다 → 최종 답(범위 · 모드 머리줄)이면 앞 묶음은 빈 글자로 숨기고, 마지막 묶음에서 검토한 뒤
# 통과면 전체를, 반려면 안내 한 줄만 보인다. 반려 이유는 판정 파일에 남겨 Stop 훅이 다시 쓰게 한다.

def _norm_text(t: str) -> str:
    return "\n".join(ln.rstrip() for ln in (t or "").strip().splitlines())


def _hash(t: str) -> str:
    import hashlib
    return hashlib.sha1(_norm_text(t).encode("utf-8")).hexdigest()


def _verdict_file(session: str) -> Path:
    return STATE / f"verdict_{re.sub(r'[^\w-]', '_', session or 'none')}.json"


def _verdicts(session: str) -> dict:
    try:
        return json.loads(_verdict_file(session).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_verdict(session: str, h: str, rec: dict) -> None:
    v = _verdicts(session)
    v[h] = rec
    p = _verdict_file(session)
    tmp = p.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)


def _sid(session: str) -> str:
    return re.sub(r"[^\w-]", "_", session or "none")


def _lock_file(session: str, h: str) -> Path:
    return STATE / f"lock_{_sid(session)}_{h[:16]}"


def _mark_prompt(data: dict) -> None:
    """사용자 질문 시각 — 이 뒤의 반려만 '앞 반려'로 넘긴다(Stop 입력엔 turn_id 가 없을 수 있다)."""
    STATE.mkdir(exist_ok=True)
    (STATE / f"prompt_{_sid(data.get('session_id'))}").write_text(
        datetime.now().isoformat(timespec="seconds"), encoding="utf-8")


REJECTED = ("rejected", "warned")   # rejected = 1번째 반려(막고 다시 쓰게) · warned = 2번째부터(경고 붙여 표시)


def _turn_rejections(session: str) -> list[dict]:
    """이번 질문(inject 가 찍은 시각) 이후의 반려 판정, 오래된 순.
    질문 시각 기록이 없으면 세션 전체를 본다 — 첫 반려를 놓쳐 끝없이 막는 쪽보다 일찍 경고로 넘어가는 쪽이 낫다."""
    try:
        since = (STATE / f"prompt_{_sid(session)}").read_text(encoding="utf-8").strip()
    except OSError:
        since = ""
    return sorted((v for v in _verdicts(session).values()
                   if v.get("status") in REJECTED and (v.get("t") or "") >= since), key=lambda v: v.get("t") or "")


def get_verdict(text: str, data: dict) -> dict:
    """같은 답을 Stop · 표시 훅 중 먼저 온 쪽이 검토하고, 다른 쪽은 그 판정을 기다린다.
    10/12: Stop 이 답 기록 0.3초 뒤에 돌고 표시 검토 판정은 20~30초 뒤에 나와, Stop 이 판정 없이 지나가
    반려된 답이 '고친 답을 준비합니다'만 남기고 끝났다. 순서를 가정하지 않는다."""
    STATE.mkdir(exist_ok=True)
    session, h = data.get("session_id") or "", _hash(text)
    lock = _lock_file(session, h)
    deadline = time.time() + REVIEW_TIMEOUT + 20
    while True:
        v = _verdicts(session).get(h)
        if v:
            return v
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > REVIEW_TIMEOUT + 20:   # 죽은 검토가 남긴 잠금
                    lock.unlink(missing_ok=True)
                    continue
            except OSError:
                continue
            if time.time() > deadline:
                return {"status": "error", "reason": f"다른 훅의 검토를 기다리다 시간 초과({REVIEW_TIMEOUT + 20}초)"}
            time.sleep(POLL)
    try:
        prior = _turn_rejections(session)
        ok, reason = review(text, data, prior[-1].get("reason", "") if prior else "")
        # 반려 횟수 기준(10/12 사용자 결정): 같은 질문에서 1번째 반려는 막고 다시 쓰게, 2번째부터는 경고 붙여 표시
        status = "error" if ok is None else "ok" if ok else "warned" if prior else "rejected"
        rec = {"t": datetime.now().isoformat(timespec="seconds"), "turn": data.get("turn_id"), "reason": reason,
               "status": status}
        _save_verdict(session, h, rec)
        return rec
    finally:
        lock.unlink(missing_ok=True)


def _needs_review(text: str) -> bool:
    """범위 · 모드 머리줄이 있는 A · C 최종 답만 검토한다."""
    if not HOLD_HEAD.match(next((ln for ln in text.splitlines() if ln.strip()), "")):
        return False
    m = HEAD_RE["mode"].search(FENCE_RE.sub("", text))
    return bool(m) and m.group(2).upper() != "B"


def review(answer: str, data: dict, previous: str) -> tuple[bool | None, str]:
    """claude -p 로 Opus 검토자를 띄운다. (ok, reason) — 검토 자체가 실패하면 (None, 오류)."""
    if FAKE_REVIEW:
        return FAKE_REVIEW == "ok", "" if FAKE_REVIEW == "ok" else "가짜 반려"
    import shutil
    import subprocess
    exe = shutil.which("claude")
    if not exe:
        return None, "claude 명령을 찾지 못함"
    args = {"answer": answer, "transcript_path": data.get("transcript_path"), "previous_rejection": previous}
    prompt = REVIEW_PROMPT.replace("$ARGUMENTS", json.dumps(args, ensure_ascii=False))
    dirs = [d for d in {data.get("cwd"), str(Path(data.get("transcript_path") or ".").parent)} if d]
    cmd = [exe, "-p", "--model", REVIEW_MODEL, "--allowedTools", "Read", "Grep", "Glob",
           "--no-session-persistence", "--output-format", "json", "--json-schema", REVIEW_SCHEMA,
           "--add-dir", *dirs]
    # 환경의 ANTHROPIC_API_KEY 를 물려주면 구독 로그인 대신 그 키(선불 크레딧)로 돈다 — 10/11 'Credit balance is too low'.
    # 키는 허락 없이 쓰지 않는다(메모리 규칙) → 빼고 구독 로그인으로. 부모 세션 표시 변수도 뺀다.
    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "CLAUDECODE")
           and not k.startswith(("CLAUDE_CODE_SESSION", "CLAUDE_CODE_CHILD", "CLAUDE_CODE_MESSAGING", "CLAUDE_PID"))}
    env["WOOJU_NESTED"] = "1"
    try:
        r = subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, timeout=REVIEW_TIMEOUT,
                           cwd=str(Path(__file__).parent), env=env)
    except subprocess.TimeoutExpired:
        return None, f"검토 시간 초과({REVIEW_TIMEOUT}초)"
    out = r.stdout.decode("utf-8", "replace")
    try:
        res = json.loads(out)
        so = res.get("structured_output")
        if not isinstance(so, dict):
            m = re.search(r"\{.*\}", res.get("result") or "", re.S)
            so = json.loads(m.group()) if m else None
        if isinstance(so, dict) and "ok" in so:
            return bool(so["ok"]), str(so.get("reason") or "")
    except (ValueError, AttributeError):
        pass
    return None, f"검토 결과를 읽지 못함(exit {r.returncode}): {(out or r.stderr.decode('utf-8', 'replace'))[:200]}"


def _show(text: str | None) -> int:
    """text=None 이면 원래 글 그대로, 아니면 그 글로 바꿔 보인다."""
    if text is not None:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "MessageDisplay", "displayContent": text}},
                         ensure_ascii=False))
    return 0


def do_display(data: dict) -> int:
    STATE.mkdir(exist_ok=True)
    mid = re.sub(r"[^\w-]", "_", data.get("message_id") or "none")
    buf, hold, passf = STATE / f"buf_{mid}.txt", STATE / f"hold_{mid}", STATE / f"pass_{mid}"
    with open(buf, "a", encoding="utf-8") as f:
        f.write(data.get("delta") or "")
    text = buf.read_text(encoding="utf-8")
    final = bool(data.get("final"))
    if not hold.exists() and not passf.exists():
        first = next((ln for ln in text.splitlines() if ln.strip()), None)
        if first is None and not final:
            return _show(None)                       # 아직 빈 줄뿐 — 판단 보류
        (hold if first and HOLD_HEAD.match(first) else passf).touch()
    if passf.exists():                               # 중간 안내 글 등 — 검토 없이 그대로
        if final:
            for p in (buf, passf):
                p.unlink(missing_ok=True)
        return _show(None)
    if not final:
        return _show("")                             # 최종 답 — 검토 끝날 때까지 숨긴다
    for p in (buf, hold):
        p.unlink(missing_ok=True)
    try:
        return _review_and_show(text, data)
    except Exception as e:  # noqa: BLE001 — 앞 묶음을 숨겼으니 죽더라도 전체 글은 보여야 한다
        return _show(f"⚠ [우주모드] 검토 중 오류({e!r}) — 아래는 검토되지 않은 답입니다.\n\n{text}")


def _review_and_show(text: str, data: dict) -> int:
    m = HEAD_RE["mode"].search(FENCE_RE.sub("", text))
    if not m or m.group(2).upper() == "B":
        return _show(text)
    v = get_verdict(text, data)
    if v.get("status") == "ok":
        return _show(text)
    if v.get("status") == "rejected":
        return _show("⏳ [우주모드] 검토에서 반려되어 고친 답을 준비합니다.\n")
    if v.get("status") == "warned":
        return _show(f"⚠ [우주모드] 다시 쓴 답도 검토에서 걸렸습니다. 아래 지적 부분은 틀렸을 수 있습니다.\n"
                     f"지적: {v.get('reason')}\n\n{text}")
    return _show(f"⚠ [우주모드] 검토를 하지 못했습니다({v.get('reason')}) — 아래는 검토되지 않은 답입니다.\n\n{text}")


def install() -> int:
    """~/.claude/settings.json 의 우주모드 훅을 이 파일 내용으로 다시 쓴다(다른 훅 · 설정은 그대로)."""
    p = Path.home() / ".claude" / "settings.json"
    s = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    me = f'python "{Path(__file__).resolve().as_posix()}"'

    def ours(h: dict) -> bool:
        return "wooju_mode.py" in (h.get("command") or "") or "우주모드 근거 검토자" in (h.get("prompt") or "")

    hooks = s.setdefault("hooks", {})
    for ev in ("UserPromptSubmit", "Stop", "MessageDisplay"):
        groups = []
        for g in hooks.get(ev, []):
            g = dict(g, hooks=[h for h in g.get("hooks", []) if not ours(h)])
            if g["hooks"]:
                groups.append(g)
        hooks[ev] = groups
    hooks["UserPromptSubmit"].append({"hooks": [{"type": "command", "command": f"{me} inject", "timeout": 10}]})
    # Stop 도 검토하거나 표시 훅의 검토를 기다린다(10/12) — 60초로는 모자란다
    hooks["Stop"].append({"hooks": [{"type": "command", "command": f"{me} check --warn",
                                     "timeout": REVIEW_TIMEOUT + 60}]})
    # 검토는 Stop(답이 보인 뒤)이 아니라 MessageDisplay(보이기 전)에서 한다 — 2026-10-11 사용자 결정(B안)
    hooks["MessageDisplay"].append({"hooks": [{"type": "command", "command": f"{me} display",
                                               "timeout": REVIEW_TIMEOUT + 60}]})
    for ev in [k for k, g in hooks.items() if not g]:
        del hooks[ev]
    tmp = p.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)
    print(f"설치: {p}")
    return 0


def _err_kind(e: str) -> str:
    """형식 위반 문구에서 뒤에 붙는 예시(': 줄 내용 …', '— 설명', '(…)')를 떼고 종류만 남긴다."""
    return re.split(r"(?<=다)\s*[:：.(—]", e, maxsplit=1)[0].strip()


def report(patterns: list[str]) -> int:
    """형식 검사 기록(wooju_log.jsonl) + 검토 판정 기록(state/verdict_*.json)을 프로젝트별로 센다.
    반려는 판정 기록이 원본이다 — 대화 기록 속 'Stop hook feedback' 만 세면 Stop 이 놓친 반려(10/12 2건)와
    경고 표시로 넘어간 2번째 반려가 빠진다. 대화 기록은 v1(Stop agent 훅, 판정 기록 없음) 반려에만 쓴다.
    3~5일 경고 운영 뒤 '막기로 바꿀지' · 'judge 창에서 쓸지' 결정용."""
    from collections import Counter, defaultdict
    fmt = defaultdict(Counter)    # 프로젝트 → 위반 종류 건수
    seen = Counter()              # 프로젝트 → 검사 횟수
    clean = Counter()             # 프로젝트 → 위반 없는 답 수
    files = sorted({f for p in patterns for f in glob.glob(os.path.expanduser(p))})
    proj_of = {Path(f).stem: Path(f).parent.name for f in files}          # 세션 → 프로젝트(두 집계가 같은 이름을 쓰게)
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            proj = proj_of.get(r.get("session") or "") or Path(r.get("cwd") or "?").name or "?"
            seen[proj] += 1
            clean[proj] += not r.get("errs")
            for e in r.get("errs") or []:
                fmt[proj][_err_kind(e)] += 1
    verd = defaultdict(Counter)
    samples = defaultdict(list)
    for vf in sorted(STATE.glob("verdict_*.json")):
        session = vf.stem[len("verdict_"):]
        try:
            vs = json.loads(vf.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        proj = proj_of.get(session, "?")
        for v in sorted(vs.values(), key=lambda v: v.get("t") or ""):
            verd[proj][v.get("status") or "?"] += 1
            if v.get("status") in REJECTED and len(samples[proj]) < 3:
                samples[proj].append((v.get("reason") or "")[:120])
    rev = Counter()
    for f in files:
        proj = Path(f).parent.name
        for d in _load(Path(f)):
            c = _content(d)
            if d.get("type") == "user" and isinstance(c, str) and c.startswith("Stop hook feedback") \
                    and "Agent hook condition was not met: [우주모드 검토]" in c:
                rev[proj] += 1
    print("■ 형식 검사(경고) — 프로젝트별 검사 수 · 위반 종류")
    for proj in sorted(seen):
        print(f"  {proj}: 검사 {seen[proj]}회, 위반 없는 답 {clean[proj]}회")
        for k, n in fmt[proj].most_common():
            print(f"     {n:4d}  {k}")
    print("■ 표시 전 검토 판정 — 프로젝트별 (state/verdict_*.json)")
    for proj in sorted(verd):
        c = verd[proj]
        print(f"  {proj}: 검토 {sum(c.values())}회 · 통과 {c['ok']} · 1차 반려 {c['rejected']} · "
              f"2차 반려(경고 표시) {c['warned']} · 검토 실패 {c['error']}")
        for s in samples[proj]:
            print(f"     · {s}")
    if rev:
        print("■ v1 사후 검토(Stop agent 훅) 반려 — 10/11 v2 이전, 판정 기록 없음")
        for proj, n in rev.most_common():
            print(f"  {proj}: {n}회")
    return 0


# ── 진입점 ───────────────────────────────────────────────────────────────────

def _log(rec: dict) -> None:
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def do_check(data: dict, warn: bool) -> int:
    tp = data.get("transcript_path")
    last = None
    if tp:
        for last in turns(_load(Path(tp))):
            pass
    sess, text, calls = last or (Session(), "", 0)
    # 공식 문서: Stop 시점의 기록 파일엔 마지막 답이 아직 없을 수 있다 → last_assistant_message 우선
    text = data.get("last_assistant_message") or text
    if not text.strip():
        return 0
    # 검토 판정 — 표시 훅보다 먼저 왔으면 여기서 검토하고, 검토 중이면 기다린다.
    # 1번째 반려(rejected)는 경고 모드와 무관하게 다시 쓰게 막고, 2번째부터(warned)는 알리기만 한다.
    notes, status = [], None
    if _needs_review(text):
        v = get_verdict(text, data)
        status = v.get("status")
        if status == "rejected":
            _log({"t": datetime.now().isoformat(timespec="seconds"), "session": data.get("session_id"),
                  "cwd": data.get("cwd"), "retry": bool(data.get("stop_hook_active")), "verdict": status,
                  "errs": check(text, sess, calls)})
            print("[우주모드 검토] 이 답은 검토에서 반려되어 사용자에게 보이지 않았다. 지적:\n" + v.get("reason", "")
                  + "\n→ 고친 부분만이 아니라 답 전체를 다시 쓸 것. `범위:` 줄 아래에 `Revised: <무엇을 고쳤나>`.",
                  file=sys.stderr)
            return 2
        if status == "warned":
            notes.append("[우주모드] 다시 쓴 답도 검토에서 걸려 경고를 붙여 표시했다(2번째 반려 — 막지 않음). 지적: "
                         + (v.get("reason") or ""))
        elif status != "ok":
            notes.append(f"[우주모드] 검토를 하지 못했다: {v.get('reason')}"[:200])
    errs = check(text, sess, calls)
    _log({"t": datetime.now().isoformat(timespec="seconds"), "session": data.get("session_id"),
          "cwd": data.get("cwd"), "retry": bool(data.get("stop_hook_active")), "verdict": status, "errs": errs})
    if errs and not (warn or data.get("stop_hook_active")):
        print("[우주모드 훅] 최종 답이 규칙을 어겼다 — 고쳐서 다시 답할 것:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 2
    if errs:
        # 경고 모드, 또는 이미 한 번 돌려보냈으면 무한 반복을 막고 알리기만 한다.
        notes.append("[우주모드 훅] 최종 답이 규칙을 어겼다 — 고쳐서 다시 답할 것:\n- " + "\n- ".join(errs))
    if notes:
        # systemMessage JSON 은 한 번만 찍는다 — 두 번 찍으면 훅 출력이 JSON 으로 안 읽힌다
        print(json.dumps({"systemMessage": "\n".join(notes)}, ensure_ascii=False))
    return 0


def do_measure(patterns: list[str]) -> int:
    files = sorted({f for p in patterns for f in glob.glob(os.path.expanduser(p))})
    tot = {"turns": 0, "answers": 0, "num_ans": 0, "num_bad_ans": 0, "nums": 0, "nums_bad": 0,
           "file_ans": 0, "file_bad_ans": 0, "refs": 0, "refs_bad": 0}
    samples: list[str] = []
    for f in files:
        for sess, text, _ in turns(_load(Path(f))):
            tot["turns"] += 1
            if not text.strip():
                continue
            tot["answers"] += 1
            body = FENCE_RE.sub("", text)
            body_nofile = FILE_LINE_RE.sub("", URL_RE.sub("", body))
            ev, _ = sess.blobs()
            nums = [m.group() for m in NUM_RE.finditer(body_nofile) if len(re.sub(r"\D", "", m.group())) >= 2]
            bad = [x for x in nums if not _num_found(x, ev)]
            if nums:
                tot["num_ans"] += 1
                tot["nums"] += len(nums)
                tot["nums_bad"] += len(bad)
                tot["num_bad_ans"] += bool(bad)
                tot["num_bad_ans_img_session"] = tot.get("num_bad_ans_img_session", 0) + bool(bad and sess.images)
            refs = FILE_LINE_RE.findall(body)
            badf = check_files(body, sess)
            if refs:
                tot["file_ans"] += 1
                tot["refs"] += len(refs)
                tot["refs_bad"] += len(badf)
                tot["file_bad_ans"] += bool(badf)
            if (bad or badf) and len(samples) < 12:
                samples.append(f"{Path(f).name[:8]} | 숫자 {sorted(set(bad))[:5]} | 파일 {badf[:3]}")
    print(json.dumps({"files": len(files), **tot}, ensure_ascii=False, indent=1))
    print("예시:")
    print("\n".join(samples))
    return 0


def _load_stdin():
    # 훅 입력은 UTF-8 이다. sys.stdin 은 윈도우에서 cp949 로 읽혀 한국어가 깨진다(10/11 Stop 오류)
    return json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if NESTED and cmd in ("inject", "check", "display"):
        return 0
    if cmd == "display":
        try:
            data = _load_stdin()
        except ValueError:
            return 0
        try:
            return do_display(data)
        except Exception:  # noqa: BLE001 — 표시 훅이 죽으면 원래 글이 보인다(공식 동작)
            return 0
    if cmd == "inject":
        try:
            _mark_prompt(_load_stdin())
        except Exception:  # noqa: BLE001 — 규칙 주입은 어떤 경우에도 한다
            pass
        print(RULES)
        return 0
    if cmd == "install":
        return install()
    if cmd == "report":
        return report(sys.argv[2:] or ["~/.claude/projects/*/*.jsonl"])
    if cmd == "measure":
        return do_measure(sys.argv[2:] or ["~/.claude/projects/*/*.jsonl"])
    if cmd == "check":
        try:
            data = _load_stdin()
        except ValueError:
            return 0
        try:
            return do_check(data, "--warn" in sys.argv)
        except Exception as e:  # noqa: BLE001 — 검사기가 죽어도 작업은 막지 않는다
            print(json.dumps({"systemMessage": f"[우주모드 훅] 검사 오류: {e!r}"[:200]}, ensure_ascii=False))
            return 0
    print("usage: wooju_mode.py inject | check [--warn] | install | report [glob...] | measure [glob...]",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
