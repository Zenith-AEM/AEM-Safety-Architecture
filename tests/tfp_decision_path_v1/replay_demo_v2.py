#!/usr/bin/env python3
"""Offline decision recomputation and exact-byte check of draft QEMU captures."""

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE.parents[1] / "research/cfv_tfp_patent_decision_v1/tfp_reference_model_v1"
sys.path.insert(0, str(MODEL))
from tfp_reference_model import ProjectedState, TFP_PASS, check_temporal_foresight

SCENARIO = HERE / "QEMU_SCENARIO_INPUTS_V2.json"
IAL = HERE / "expected_ial_v2_c5.txt"
IAL_HASH = HERE / "expected_ial_v2_c5.sha256"
DELTAS = {
    "network": 2, "remote": 2, "daemon": 2, "service": 2,
    "config": 1, "system": 1, "kernel": 1, "STATUS_CHECK": -1,
}


def transition(action: str, risk: Fraction, _step: int) -> ProjectedState:
    next_score = max(0, int(risk) + DELTAS[action])
    return ProjectedState(Fraction(next_score), next_score > 9)


EVALUATION = re.compile(
    r"\[AEM_TFP_EVALUATION_V1\] "
    r"(?P<identity>request_id=[a-z0-9-]+ node_id=[a-z0-9-]+ "
    r"role=[A-Z]+ rule_id=[0-9]+ timestamp=[0-9]+ nonce=[0-9]+ "
    r"action=(?P<action>[A-Za-z_]+)) "
    r"model_version=1 model=sustained_repetition steps=5 "
    r"current_score=(?P<score>[0-9]+) "
    r"projected=(?P<projected>[0-9]+(?:,[0-9]+){4}) "
    r"projected_limit=9 weights=16,8,4,2,1 "
    r"weighted_numerator=(?P<weighted>[0-9]+) denominator=32 tolerance=5 "
    r"first_limit_step=(?P<first_limit>[0-9]+) "
    r"reason=(?P<reason>PASS|PROJECTED_LIMIT|WEIGHTED_LIMIT)\n"
)
RESET_LINE = (
    "[AEM_SCENARIO_RESET] token_budget=1000 panic_lock=0 fcp_risk_score=0 "
    "cfv_iel_veto_count=0 cfv_fcp_veto_count=0 cfv_tfp_veto_count=0 "
    "cfv_bad_param_count=0\n"
)
DECISION = re.compile(
    r"\[(?P<event>AEM_(?:IEL_VETO|UNKNOWN_ACTION_VETO|STATE_INVALID|"
    r"FCP_VETO|TFP_VETO|PERMIT_GRANTED))\] "
    r"(?P<identity>request_id=[a-z0-9-]+ node_id=[a-z0-9-]+ "
    r"role=[A-Z]+ rule_id=[0-9]+ timestamp=[0-9]+ nonce=[0-9]+ "
    r"action=(?P<action>[^\n]+))\n"
)
IEL_PHRASES = (
    "REBOOT", "FCP_ALTER", "SHUTDOWN", "chmod", "update_weights",
    "recompile", "sudo", "curl", "wget", "ssh", "ftp",
    "ignore previous instructions", "developer mode", "cron", "at now",
    "sleep", "stage firewall disable", "prepare watchdog removal",
    "queue audit deletion", "preposition persistent service",
    "arm delayed reboot", "schedule trust bypass",
)
TRACE_LAYER = {
    "AEM_IEL_VETO": "IEL",
    "AEM_UNKNOWN_ACTION_VETO": "UNKNOWN_ACTION",
    "AEM_STATE_INVALID": "STATE_INVALID",
    "AEM_FCP_VETO": "FCP",
    "AEM_TFP_VETO": "TFP",
}


def matching_trace(line: str, decision: re.Match[str]) -> bool:
    event = decision["event"]
    layer = TRACE_LAYER.get(event)
    if layer is None:
        return False
    identity = decision["identity"]
    prefix, action = identity.rsplit(" action=", 1)
    # CFV_TRACE deliberately omits timestamp and nonce.
    prefix = prefix.split(" timestamp=", 1)[0]
    return line == f"[CFV_TRACE] source_layer={layer} {prefix} action={action}\n"


def recompute_evaluations(ial: bytes) -> bool:
    """Recalculate stage order, projections, decisions and score continuity."""
    try:
        lines = ial.decode("ascii").splitlines(keepends=True)
    except UnicodeDecodeError:
        return False
    if not lines or lines[0] != RESET_LINE:
        return False
    score = 0
    decisions = 0
    i = 1
    while i < len(lines):
        line = lines[i]
        if not line.startswith("[AEM_TFP_EVALUATION_V1]"):
            decision = DECISION.fullmatch(line)
            if not decision or i + 1 >= len(lines):
                return False
            action = decision["action"]
            expected = (
                "AEM_IEL_VETO" if any(word in action for word in IEL_PHRASES)
                else "AEM_UNKNOWN_ACTION_VETO" if action not in DELTAS
                else "AEM_STATE_INVALID" if score > 5
                else "AEM_FCP_VETO" if max(0, score + DELTAS[action]) > 5
                else None
            )
            if decision["event"] != expected or not matching_trace(lines[i + 1], decision):
                return False
            decisions += 1
            i += 2
            continue
        match = EVALUATION.fullmatch(line)
        if not match or i + 1 == len(lines):
            return False
        action = match["action"]
        if (action not in DELTAS or score > 5 or
                max(0, score + DELTAS[action]) > 5 or
                int(match["score"]) != score):
            return False
        projected = []
        current = Fraction(score)
        for step in range(1, 6):
            current = transition(action, current, step).risk
            projected.append(int(current))
        first_limit = next((n for n, value in enumerate(projected, 1)
                            if value > 9), 0)
        weighted = sum(a * b for a, b in zip(projected, (16, 8, 4, 2, 1)))
        result = check_temporal_foresight(
            action, Fraction(score), Fraction(5), transition
        )
        model_prefix = tuple(int(value) for value in result.projected_risks)
        if tuple(projected[:len(model_prefix)]) != model_prefix:
            return False
        model_numerator = sum(
            value * weight for value, weight in
            zip(model_prefix, (16, 8, 4, 2, 1))
        )
        if result.future_risk * 32 != model_numerator:
            return False
        if len(model_prefix) == 5 and weighted != model_numerator:
            return False
        reason = ("PROJECTED_LIMIT" if first_limit else
                  "WEIGHTED_LIMIT" if weighted > 160 else "PASS")
        if (result.decision == TFP_PASS) != (reason == "PASS"):
            return False
        if (match["projected"] != ",".join(map(str, projected)) or
                int(match["weighted"]) != weighted or
                int(match["first_limit"]) != first_limit or
                match["reason"] != reason):
            return False
        decision = "AEM_PERMIT_GRANTED" if reason == "PASS" else "AEM_TFP_VETO"
        if lines[i + 1] != f"[{decision}] {match['identity']}\n":
            return False
        if reason == "PASS":
            score = max(0, score + DELTAS[action])
            i += 2
        else:
            parsed = DECISION.fullmatch(lines[i + 1])
            if not parsed or i + 2 >= len(lines) or not matching_trace(lines[i + 2], parsed):
                return False
            i += 3
        decisions += 1
    return decisions > 0


def expected_effect() -> bytes:
    steps = json.loads(SCENARIO.read_text(encoding="ascii"))["steps"]
    return "".join(
        f"AEM_EFFECT_V1 request_id={step['request_id']} action={step['action']}\n"
        for step in steps if step["event"] == "AEM_PERMIT_GRANTED"
    ).encode("ascii")


def classify(ial: bytes, effect: bytes) -> str:
    expected = IAL.read_bytes()
    line = IAL_HASH.read_text(encoding="ascii")
    if line != f"{hashlib.sha256(expected).hexdigest()}  {IAL.name}\n":
        return "INCOMPLETE"
    # Exact bytes also reject a PASS evaluation whose permit/state/audit write
    # failed, leaving no immediately following decision line.
    if not recompute_evaluations(ial):
        return "INCOMPLETE"
    if ial != expected or effect != expected_effect():
        return "INCOMPLETE"
    return "PASS"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ial", required=True, type=Path)
    parser.add_argument("--effect", required=True, type=Path)
    args = parser.parse_args()
    result = classify(args.ial.read_bytes(), args.effect.read_bytes())
    print(result)
    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
