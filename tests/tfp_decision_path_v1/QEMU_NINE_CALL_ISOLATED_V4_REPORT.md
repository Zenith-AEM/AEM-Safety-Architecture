# QEMU isolated-effect run: R12 toolchain provenance

> Public subset note (November 2026): this report describes the retained full local V4 packet. Some linked V1–V3 reports, build artifacts, logs and snapshots are not included in this public subset. See [the public milestone](../../QEMU_MILESTONE_2026_11.md) for the files available here and the replay limit.

The [V4 one-shot runner](qemu_nine_call_isolated_v4.py) returned `PASS`
on 2026-11-16. This is a fresh local QEMU run. The accepted
[V3 result](QEMU_NINE_CALL_ISOLATED_V3_REPORT.md) and its
[R12 review](../tfp_decision_path_v1_returns/CLAUDE_CODE_REVIEW_R12_QEMU_ISOLATED_V3.md)
remain unchanged.

R12-1 is addressed for this run. Before either TA build, the runner recorded
a canonical [file and symlink inventory](qemu_nine_call_isolated_v4/staged-kit-tree.txt)
of the copied and signer-updated TA development kit. Its SHA-256 is
`9b9a441dd4ed8503a1c5ec3a25135a8ccde1afcfd547d1914e26a0feb86faffe`.
The [run record](qemu_nine_call_isolated_v4/RUN_RECORD.json) also records
the SHA-256 of the staged `default_ta.pem` target, without retaining the
private key bytes. It records the exact Buildroot compiler wrapper,
underlying compiler, and system kernel cross-compiler paths, versions and
binary hashes. The 11 child, Authority and signer inputs remain copied and
hashed as in V3. These identities help diagnose and reproduce the recipe;
they do not show that the TA builds are byte reproducible.

The final 4,363-byte IAL and separate 266-byte effect capture are byte
identical to V3 and pass host replay. Exactly five permit markers appear for
calls 1 and 5–8; the veto-only second boot added none. The first readback
after relaunch equals the pre-restart ledger and score 4 state. Both disk
snapshots decompress to their recorded raw hashes, and the same disk path
was used in both QEMU processes. The directory retains both ramdisks,
the built TAs and client, logs, disk snapshots, build inputs and a
[recursive SHA-256 manifest](qemu_nine_call_isolated_v4/SHA256SUMS.txt).

The child and Authority TA whole-file hashes differ across runs because
their RSA-PSS signatures use fresh random salt. R13 identified this, and an
offline [stable TA identity derivation](qemu_nine_call_isolated_v4/TA_STABLE_IDENTITY.json)
independently checked the eight retained TA files. Within each TA family,
the signed digest and unsigned payload SHA-256 are identical across runs,
while signature hashes differ. Each signature verifies against the public
half of the recorded default development key. The derivation was added
after V4 ran; it does not change the original run record or imply that QEMU
was rerun. The [derivation script](ta_stable_identity.py) checks its output
with `--check`.

For this result, exact binary identity rests on the retained TA files and
their equality to the ramdisk contents. Their matching unsigned images are
reproducible across these builds; the randomized signed files are not byte
identical. The QEMU-only Authority variant and public test
HMAC key provide no production signer or root of trust. The effect is a
client marker, not a physical action. No Board B contact or hardware,
RPMB, target-write or release authority follows from this demo.
