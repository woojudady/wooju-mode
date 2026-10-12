"""우주모드 훅 시험 — 실행: python test_wooju.py (cwd 아래 wtest/ 에 시험 기록을 만든다)."""
import json, subprocess, os
H = os.path.expanduser('~/.claude/hooks/wooju_mode.py')
os.environ.setdefault("WOOJU_LOG", os.path.abspath("wtest/test_log.jsonl"))  # 실제 경고 기록을 건드리지 않게
os.environ["WOOJU_STATE"] = os.path.abspath("wtest/state_sub")  # 실제 판정 기록을 건드리지 않게
os.environ["WOOJU_FAKE_REVIEW"] = "ok"  # 하위 프로세스 시험이 진짜 검토자를 부르지 않게(10/12 13번 불림)
os.makedirs("wtest", exist_ok=True)
# 앞 시험의 판정 기록이 남으면 두 번째 실행부터 2건이 실패한다(10/12 실측: 빈 폴더 0/18 → 같은 폴더 재실행 2/18)
import shutil
for _d in ("wtest/state", "wtest/state_sub"):
    shutil.rmtree(_d, ignore_errors=True)
def tr(name, reply, tools=(), image=False):
    rows=[{"type":"user","message":{"role":"user","content":"질문"}}]
    if image:
        rows[0]["message"]["content"]=[{"type":"text","text":"이 화면 봐"},{"type":"image","source":{}}]
    for i,(t,out) in enumerate(tools):
        rows.append({"type":"assistant","message":{"content":[{"type":"tool_use","id":f"t{i}","name":t[0],"input":t[1]}]}})
        rows.append({"type":"user","message":{"content":[{"type":"tool_result","tool_use_id":f"t{i}","content":out}]}})
    rows.append({"type":"assistant","message":{"content":[{"type":"text","text":reply}]}})
    p=f"wtest/{name}.jsonl"; open(p,"w",encoding="utf-8").write("\n".join(json.dumps(r,ensure_ascii=False) for r in rows))
    return p
read=("Read",{"file_path":"C:/kiwoom_bot/tools/hook_gate.py","offset":30,"limit":20})
other=("Read",{"file_path":"C:/kiwoom_bot/config.py"})
grep=("Bash",{"command":"grep -n def tools/hook_gate.py"})
web=("WebFetch",{"url":"https://github.com/woojudady/wooju-mode"})
OK_A="범위: 훅 줄 수\n모드: A\n검증: Read 로 확인\n🔸 hook_gate.py 는 693줄이다 [근거: hook_gate.py:41]\n⚪ 대략 700줄이다(가정: 반올림)\n결론: 위 확인대로다."
R=[(read,"    41\tdef _run 693 lines")]
cases=[
 ("no_mode","그냥 답입니다.",(),False,{},2),
 ("b_with_tool","범위: 인사\n모드: B\n좋아요!",R,False,{},2),
 ("b_ok","범위: 인사\n모드: B\n좋아요!",(),False,{},0),
 ("a_ok",OK_A,R,False,{},0),
 ("a_grep_ok",OK_A,[(grep,"41:def _run\n693")],False,{},0),
 ("a_bad_num",OK_A.replace("693줄이다","812줄이다"),R,False,{},2),
 ("a_bad_line",OK_A.replace("hook_gate.py:41","hook_gate.py:500"),R,False,{},2),
 ("a_no_ev","범위: x\n모드: A\n검증: y\n🔸 693줄이다\n결론: z",R,False,{},2),
 ("a_no_label","범위: x\n모드: A\n검증: y\n693줄이다\n결론: z",R,False,{},2),
 ("a_no_concl","범위: x\n모드: A\n검증: y\n⚪ 추정",(),False,{},2),
 ("web_1dom","범위: x\n모드: A\n검증: y\n🔸 v4.0 이다 [근거: https://github.com/woojudady/wooju-mode]\n결론: z",[(web,"Wooju v4.0")],False,{},2),
 ("web_short","범위: x\n모드: A\n검증: y\n🔸 v4.0 이다 [근거: https://github.com/woojudady/wooju-mode]\n출처 부족: 저장소 하나가 원문\n결론: z",[(web,"Wooju v4.0")],False,{},0),
 ("web_unseen","범위: x\n모드: A\n검증: y\n🔸 v4.0 이다 [근거: https://example.org/a]\n출처 부족: q\n결론: z",[(web,"Wooju v4.0")],False,{},2),
 ("img_ok","범위: x\n모드: A\n검증: 화면\n🔸 종가 76,500원 [근거: 이미지]\n결론: z",R,True,{},0),
 ("img_none","범위: x\n모드: A\n검증: 화면\n🔸 종가 76,500원 [근거: 이미지]\n결론: z",R,False,{},2),
 ("retry_noblock","그냥 답",(),False,{"stop_hook_active":True},0),
 ("code_fence_ok","범위: x\n모드: C\n```\n모드: B 1234\n```\n⚪ 해석\n결론: z",(),False,{},0),
 # ── 보완 1~3
 ("new1_unlabeled_num","범위: x\n모드: A\n검증: y\n⚪ 해석\n환율은 1,400원이다\n결론: z",R,False,{},2),
 ("new1_two_digit_ok","범위: x\n모드: A\n검증: y\n⚪ 해석\n종목 51개 중 15개\n결론: z",R,False,{},0),
 ("new1_scope_line_ok","범위: 2026년 1,400원 질문\n모드: C\n⚪ 해석\n결론: z",(),False,{},0),
 ("new2_white_no_calc","범위: x\n모드: A\n검증: y\n⚪ 환율 1,400원으로 치면 55만원\n결론: z",R,False,{},2),
 ("new2_white_calc_ok","범위: x\n모드: A\n검증: y\n⚪ 455 = 580 − 125\n결론: z",R,False,{},0),
 ("new2_white_assume_ok","범위: x\n모드: A\n검증: y\n⚪ 가정: 환율 1,400원\n결론: z",R,False,{},0),
 ("new3_scoped_wrong_file","범위: x\n모드: A\n검증: y\n🔸 값은 777 [근거: hook_gate.py:41]\n결론: z",[(read,"    41\tdef _run"),(other,"777")],False,{},2),
 ("new3_scoped_right_file","범위: x\n모드: A\n검증: y\n🔸 값은 777 [근거: hook_gate.py:41]\n결론: z",[(read,"    41\tdef _run 777"),(other,"1")],False,{},0),
 ("new3_two_digit_not_checked","범위: x\n모드: A\n검증: y\n🔸 51개다 [근거: hook_gate.py:41]\n결론: z",R,False,{},0),
]
fail=0
for name,reply,tools,img,extra,want in cases:
    p=tr(name,reply,tools,img)
    data={"transcript_path":os.path.abspath(p),"session_id":"test","cwd":"x",**extra}
    env={k:v for k,v in os.environ.items() if k!='PYTHONIOENCODING'}
    r=subprocess.run(["python",H,"check"],input=json.dumps(data).encode(),capture_output=True,env=env)
    ok = r.returncode==want; fail += not ok
    msg=(r.stderr or r.stdout).decode('utf-8').strip().replace("\n"," / ")
    print(("OK  " if ok else "FAIL"), name, "exit", r.returncode, "|", msg[60:200])
print("FAILS", fail, "/", len(cases))
# last_assistant_message: 기록 파일엔 위반 답, 필드엔 정상 답 → 필드를 따라야 통과
p=tr("lam", "그냥 답", R)
for msg,want in ((OK_A,0),("그냥 답",2)):
    env={k:v for k,v in os.environ.items() if k!='PYTHONIOENCODING'}
    r=subprocess.run(["python",H,"check"],input=json.dumps({"transcript_path":os.path.abspath(p),"last_assistant_message":msg}).encode(),capture_output=True,env=env)
    print(("OK  " if r.returncode==want else "FAIL"), "last_assistant_message", want, r.returncode)
r=subprocess.run(["python",H,"check"],input=json.dumps({"last_assistant_message":"그냥 답"}).encode(),capture_output=True)
print(("OK  " if r.returncode==2 else "FAIL"), "no transcript", r.returncode)
# Updated 강제: 턴 안에 우주모드 반려(isMeta) → 다시 쓴 답에 Updated 없으면 위반
def tr_fb(name, reply):
    rows=[{"type":"user","message":{"role":"user","content":"질문"}},
          {"type":"assistant","message":{"content":[{"type":"text","text":"첫 답"}]}},
          {"type":"user","isMeta":True,"message":{"role":"user","content":"Stop hook feedback:\nAgent hook condition was not met: [우주모드 검토] x"}},
          {"type":"assistant","message":{"content":[{"type":"text","text":reply}]}}]
    p=f"wtest/{name}.jsonl"; open(p,"w",encoding="utf-8").write("\n".join(json.dumps(r,ensure_ascii=False) for r in rows)); return p
base="범위: x\n모드: C\n⚪ 해석\n결론: z"
for name,reply,want in (("fb_no_updated",base,2),("fb_updated","Updated: 고침\n"+base,0)):
    r=subprocess.run(["python",H,"check"],input=json.dumps({"transcript_path":os.path.abspath(tr_fb(name,reply))}).encode(),capture_output=True)
    print(("OK  " if r.returncode==want else "FAIL"), name, r.returncode, r.stderr.decode('utf-8').strip().replace("\n"," / ")[40:140])

# ── 표시 전 검토(MessageDisplay) — 검토자는 가짜로 바꿔 끼운다(사용량 0), 판정은 시험 폴더에
import io, contextlib, sys as _sys
_sys.path.insert(0, os.path.dirname(H)); import wooju_mode as w
w.STATE = __import__("pathlib").Path(os.path.abspath("wtest/state")); w.STATE.mkdir(parents=True, exist_ok=True)
def run(fn, data):
    out = io.StringIO(); err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fn(data)
    return rc, out.getvalue(), err.getvalue()
def shown(o):
    return json.loads(o)["hookSpecificOutput"]["displayContent"] if o.strip() else None
ANS = "범위: x\n모드: A\n검증: y\n🔸 값 [근거: a.py:1]\n결론: z\n"
def stream(mid, text, verdict, session="s1"):
    w.review = lambda t, d, p: verdict
    lines = text.splitlines(keepends=True); res = []
    for i, ln in enumerate(lines):
        res.append(shown(run(w.do_display, {"message_id": mid, "session_id": session, "turn_id": "T", "index": i,
                                             "final": i == len(lines) - 1, "delta": ln, "transcript_path": "", "cwd": ""})[1]))
    return res
dcases = []
r = stream("m_pass", "파일을 확인하겠습니다.\n다음 줄\n", (True, ""));           dcases.append(("pass_through", r == [None, None]))
r = stream("m_ok", ANS, (True, ""));                                            dcases.append(("hold_then_full", r[:-1] == [""] * (len(r) - 1) and r[-1] == ANS))
r = stream("m_rej", ANS.replace("결론", "결론2"), (False, "틀림"));               dcases.append(("rejected_notice", r[-1].startswith("⏳") and "결론2" not in r[-1]))
r = stream("m_b", "범위: x\n모드: B\n좋아요\n", (False, "불림"));               dcases.append(("mode_b_no_review", r[-1] == "범위: x\n모드: B\n좋아요\n"))
r = stream("m_err", ANS.replace("결론", "결론3"), (None, "시간 초과"));          dcases.append(("error_shows_text", r[-1].startswith("⚠") and "결론3" in r[-1]))
# Stop 연동: 반려된 답과 같은 글이면 경고 모드여도 막는다 / 통과한 답은 안 막는다
rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s1", "last_assistant_message": ANS.replace("결론", "결론2")})
dcases.append(("stop_blocks_rejected", rc == 2 and "틀림" in e))
rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s1", "last_assistant_message": ANS})
dcases.append(("stop_allows_ok", rc == 0 and "틀림" not in e))
# 다시 쓴 답 검토 때 앞 반려 이유가 넘어가는지
seen = {}
w.review = lambda t, d, p: (seen.setdefault("prev", p), (True, ""))[1]
stream_ = [run(w.do_display, {"message_id": "m_re", "session_id": "s1", "turn_id": "T", "index": 0, "final": True,
                              "delta": "범위: x\nRevised: 고침\n모드: A\n결론: z\n", "transcript_path": "", "cwd": ""})]
dcases.append(("previous_rejection_passed", seen.get("prev") == "틀림"))
# 실제 순서(10/12): Stop 이 답 기록 0.3초 뒤에 돌고 표시 검토 판정은 20~30초 뒤 — Stop 이 판정 없이 지나가 반려가 묻혔다
calls = []
w.review = lambda t, d, p: (calls.append(t), (False, "틀림4"))[1]
ANS4 = ANS.replace("결론", "결론4")
rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s4", "last_assistant_message": ANS4})
dcases.append(("stop_first_reviews_and_blocks", rc == 2 and "틀림4" in e and len(calls) == 1))
r = stream("m_after_stop", ANS4, (True, "불리면 안 됨"), session="s4")
dcases.append(("display_after_stop_reuses_verdict", r[-1].startswith("⏳")))
# 다른 쪽이 검토 중(잠금)이면 판정이 기록될 때까지 기다린다
import threading, time as _time
ANS5 = ANS.replace("결론", "결론5")
try:
    lock = w._lock_file("s1", w._hash(ANS5)); lock.write_text("x")
    def _later():
        _time.sleep(1.5); w._save_verdict("s1", w._hash(ANS5), {"status": "rejected", "reason": "틀림5"}); lock.unlink()
    threading.Thread(target=_later).start()
    w.review = lambda t, d, p: (True, "불리면 안 됨")
    rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s1", "last_assistant_message": ANS5})
    dcases.append(("stop_waits_for_other_review", rc == 2 and "틀림5" in e))
except AttributeError:
    dcases.append(("stop_waits_for_other_review", False))
# 반려 횟수 기준(사용자 결정): 같은 질문에서 1번째 반려는 막고 다시 쓰게, 2번째부터는 막지 않고 경고와 함께 표시
_pf = w.STATE / "prompt_s2"
_pf.write_text("2000-01-01T00:00:00", encoding="utf-8")
w.review = lambda t, d, p: (False, "틀림A")
rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s2", "last_assistant_message": ANS.replace("결론", "결론A")})
dcases.append(("first_rejection_blocks", rc == 2 and "틀림A" in e))
w.review = lambda t, d, p: (False, "틀림B")
ANSB = "범위: x\nRevised: 고침\n모드: A\n검증: y\n🔸 값 [근거: a.py:1]\n결론: zB\n"
rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s2", "last_assistant_message": ANSB})
dcases.append(("second_rejection_not_blocked", rc == 0 and "틀림B" in o))
r = stream("m_second", ANSB, (False, "불리면 안 됨"), session="s2")
dcases.append(("second_rejection_shown_with_warning", r[-1].startswith("⚠") and "틀림B" in r[-1] and ANSB in r[-1]))
# 새 질문이면 횟수가 0부터 — 다시 1번째 반려로 막는다
_pf.write_text("2999-01-01T00:00:00", encoding="utf-8")
w.review = lambda t, d, p: (False, "틀림C")
rc, o, e = run(lambda d: w.do_check(d, True), {"session_id": "s2", "last_assistant_message": ANS.replace("결론", "결론C")})
dcases.append(("new_prompt_resets_count", rc == 2 and "틀림C" in e))
# 집계(report): 판정 기록 기준으로 프로젝트별 통과 · 1차 반려 · 2차 반려(경고 표시) · 실패를 센다
import pathlib as _pl
_proj = _pl.Path(os.path.abspath("wtest/projects/P1")); _proj.mkdir(parents=True, exist_ok=True)
(_proj / "s3.jsonl").write_text("", encoding="utf-8")
w._verdict_file("s3").write_text(json.dumps({
    "a": {"t": "x", "status": "ok"}, "b": {"t": "x", "status": "rejected"}, "c": {"t": "x", "status": "rejected"},
    "d": {"t": "x", "status": "warned"}, "e": {"t": "x", "status": "error"}}), encoding="utf-8")
_old_log = w.LOG; w.LOG = _pl.Path(os.path.abspath("wtest/report_log.jsonl"))
w.LOG.write_text(json.dumps({"cwd": "C:\\P1", "errs": ["`범위:` 줄이 없다 (Scope Lock).",
                                                       "🔸/🔹 줄에 [근거: …] 가 없다: 🔸 값"]}) + "\n", encoding="utf-8")
rc, o, e = run(lambda _: w.report([os.path.abspath("wtest/projects/*/*.jsonl")]), None)
w.LOG = _old_log
dcases.append(("report_counts_verdicts", "P1: 검토 5회 · 통과 1 · 1차 반려 2 · 2차 반려(경고 표시) 1 · 검토 실패 1" in o))
dcases.append(("report_error_kinds_readable", "`범위:` 줄이 없다" in o and "🔸/🔹 줄에 [근거: …] 가 없다" in o))
# 중첩 방지: WOOJU_NESTED 면 아무것도 안 한다
r2 = subprocess.run(["python", H, "display"], input=rb'{"message_id":"n","final":true,"delta":"\ubc94\uc704: x\n\ubaa8\ub4dc: A\n"}',
                    capture_output=True, env=dict(os.environ, WOOJU_NESTED="1"))
dcases.append(("nested_noop", r2.returncode == 0 and not r2.stdout.strip()))
for name, ok in dcases:
    print(("OK  " if ok else "FAIL"), "display", name)
print("DISPLAY FAILS", sum(not ok for _, ok in dcases), "/", len(dcases))

# 실제 Claude Code 처럼 UTF-8 원문(이스케이프 없음)을 넣는다 — 10/11 cp949 로 읽어 Stop·표시 훅이 죽은 결함
_env = {k: v for k, v in os.environ.items() if k != 'PYTHONIOENCODING'}
_raw = json.dumps({"last_assistant_message": "범위: 시험\n모드: B\n안녕"}, ensure_ascii=False).encode("utf-8")
r = subprocess.run(["python", H, "check"], input=_raw, capture_output=True, env=_env)
ok = r.returncode == 0 and "검사 오류" not in r.stdout.decode("utf-8", "replace")
print(("OK  " if ok else "FAIL"), "raw_utf8_check")
_raw = json.dumps({"message_id": "raw8", "final": True, "delta": "범위: 시험\n모드: B\n안녕"}, ensure_ascii=False).encode("utf-8")
r = subprocess.run(["python", H, "display"], input=_raw, capture_output=True, env=_env)
ok = "모드: B" in r.stdout.decode("utf-8", "replace")
print(("OK  " if ok else "FAIL"), "raw_utf8_display")
