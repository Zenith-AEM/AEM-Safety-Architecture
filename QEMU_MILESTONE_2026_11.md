# QEMU decision and evidence milestone

**Status:** local research result, 16 November 2026. This is a bounded software demonstration, not an operational safety certification.

## What was observed

One controlled QEMU run used two boots and the same virtual disk. Nine fixed requests went through the Gateway Authority and child trusted application. Calls 1 and 5–8 were permitted and produced exactly five lines in a separate effect capture. The other four requests were vetoed and produced no effect marker. The first readback after the second boot matched the pre-restart ledger and score 4 state. The final ledger was 4,363 bytes; the effect capture was 266 bytes. The host replay checker returned `PASS` for those exact bytes.

The [V4 report](tests/tfp_decision_path_v1/QEMU_NINE_CALL_ISOLATED_V4_REPORT.md) records the run and its provenance limits. A [separate Claude Code review](tests/tfp_decision_path_v1_returns/CLAUDE_CODE_REVIEW_R13_QEMU_ISOLATED_V4.md) checked the retained run packet without rerunning QEMU; its closure check covers the later stable TA identity derivation. That review is not an independent external assessment.

The five-step forward check repeats the *same* proposed action under a fixed demo transition rule. For starting scores 0–5, this reduces to a simple bounded rule: +2 actions are never permitted (TFP vetoes at lower scores and FCP vetoes at higher scores); +1 actions are vetoed by TFP at score 4 and by FCP at score 5; other allowed actions are not vetoed by TFP. The projected limit of 9 is a demo parameter. This is not a forecast of arbitrary controller behavior.

## Replay the public subset

From the repository root, with Python 3:

```sh
python3 tests/tfp_decision_path_v1/replay_demo_v2.py \
  --ial tests/tfp_decision_path_v1/qemu_nine_call_isolated_v4/ial-final.bin \
  --effect tests/tfp_decision_path_v1/qemu_nine_call_isolated_v4/effect.raw
```

Expected output: `PASS` with exit code 0. The checker uses the published [scenario inputs](tests/tfp_decision_path_v1/QEMU_SCENARIO_INPUTS_V2.json), [expected ledger](tests/tfp_decision_path_v1/expected_ial_v2_c5.txt), [ledger hash](tests/tfp_decision_path_v1/expected_ial_v2_c5.sha256) and [reference model](research/cfv_tfp_patent_decision_v1/tfp_reference_model_v1/tfp_reference_model.py). The captured [ledger](tests/tfp_decision_path_v1/qemu_nine_call_isolated_v4/ial-final.bin) and [effect](tests/tfp_decision_path_v1/qemu_nine_call_isolated_v4/effect.raw) are exact copies from the retained V4 packet.

The public subset checks the captured bytes against a fixed expected scenario; it does not independently replay the virtual machine or prove how those bytes were produced. The [public subset manifest](PUBLIC_SUBSET_SHA256SUMS.txt) hashes the selected files in this update. The complete local packet also retains two ramdisks, built trusted applications and client, raw consoles, disk snapshots, build inputs, a run record and a 37-entry SHA-256 manifest. Those larger inputs are not published in this update. The stable TA identity derivation and corresponding manifest update occurred **after** the QEMU run; the original run record was unchanged.

## Claim boundary

The QEMU effect is a client marker, not a physical output. The Authority variant uses a public demo HMAC key and the trusted applications use OP-TEE's default development signing key. The controlled restart does not establish arbitrary power-loss durability. The published subset and local review do not establish a production signer, protected output path, privileged-attacker resistance, Board B RPMB safety or a verified physical sidecar. No Board B contact or hardware authority followed from this run.
