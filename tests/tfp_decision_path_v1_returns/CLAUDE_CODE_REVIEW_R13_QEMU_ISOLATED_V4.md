# Claude Code review R13: QEMU isolated-effect run V4 (R12-1), and the cause of R11-2

> Public subset note (November 2026): this review examined the retained full local packet. The public repository contains selected replay bytes and sources, not all files described below. This was a separate AI-assisted review, not an independent external assessment.

2026-11-16. Read-only review of:
- `QEMU_NINE_CALL_ISOLATED_V4_REPORT.md`;
- `qemu_nine_call_isolated_v4.py`, compared with V3;
- `qemu_nine_call_isolated_v4/`.

I did not re-run QEMU. I re-checked the retained bytes and extracted both ramdisks in the session scratchpad. I also parsed the signed headers of the retained TAs from every run. No package file was modified.

## Verdict

**ACCEPT. R12-1 is closed.** In checking it I also found the cause of **R11-2**: the TA builds **are** reproducible. Only the RSA-PSS signature changes between builds. The report's "cause not established" can now be replaced (R13-1).

## R12-1 closed

**TA dev kit.**
- `kit_manifest` (`qemu_nine_call_isolated_v4.py:51-63`) records every file with its SHA-256 and every symlink with its target, in a canonical order.
- It does this on the **staged** kit, after the signer swap and before either build (`:154-160`).
- `staged-kit-tree.txt` has 361 entries, and its hash `9b9a441d…` matches the record and the report.
- The kit has a single symlink, `keys/default_ta.pem → default.pem`, which points inside the kit. So the inventory covers the content.
- The signing-key hash `0d49c9e3…` matches both the `default.pem` line and the source kit. `sign_encrypt.py` in the inventory is the QEMU signer, `6cc89059…`.

**Compilers.**
- The Buildroot wrapper (`toolchain-wrapper`, `bce01a9d…`) and the real gcc 14.3.0 (`d42d52ba…`) match their resolved paths on disk.
- So does the system `aarch64-linux-gnu-gcc-13` 13.3.0 (`cd90adc7…`).

## Run re-verified

| Check | Result |
|---|---|
| `SHA256SUMS.txt`, recursive | OK, 36 entries |
| Build inputs | All 11 match their retained copies |
| `ial-final.bin` | Identical to the fixture |
| `effect.raw` | Identical to V3 and to `effect-after-first.bin` |
| `classify` | `PASS` |
| Binaries in both ramdisks match the retained and recorded ones | Child `f199b002…`, Authority `dde2ccf5…`, client `3170a5db…` |
| Exit codes | `0,1,1,1,0,0,0,0`, then `1` |
| State readbacks | Score 0, then 4 after call 8, then 4 after the restart. TFP count 1, then 2. |
| Disk snapshots decompress to the recorded hashes | `bb6498d3…` (equal to `disk_before_second`) and `15a42127…` |
| Effect markers in the normal or secure consoles | 0 in each of the four |

## R11-2 diagnosed: RSA-PSS uses a random salt

**The cause.** Every retained TA header has `algo = 0x70414930`, which is `TEE_ALG_RSASSA_PKCS1_PSS_MGF1_SHA256`, the default in `sign_encrypt.py:11,132`. PSS signing uses a fresh random salt each time, so the signature bytes are different on every signing, even for an identical image.

**How I checked.** I split each `.ta` into three parts:
- the 20-byte `shdr`;
- the 32-byte signed digest and the 256-byte signature;
- the rest, which is the bootstrap header followed by the ELF.

| TA | Runs compared | Signed digest | Payload hash | Signature |
|---|---|---|---|---|
| Child `8aaaf200` | smoke, V2, V3, V4 | `6aff4883…` in every run | `8e12d375…` in every run | Differs every time |
| Authority variant `77ffab7d` | V1, V2, V3, V4 | `1b7e4058…` in every run | `b342c056…` in every run | Differs every time |

V1 had no separate child file; it used the smoke-run child TA. The smoke run's Authority is the **non-variant** source, so its different digest is expected.

**Integrity of the headers.** For the V3 and V4 TAs, `SHA-256(shdr ‖ rest)` equals the digest stored in the header. The signature verifies with PSS (SHA-256, MGF1, 32-byte salt) against the public half of the kit's `default.pem`.

**What this means.** The child and Authority builds are byte-reproducible **up to the signature**. The V1 child is the same image as V2–V4, and the V1–V4 Authority variants are the same image.

## R13-1 (low, wording and record): state the R11-2 cause and record a stable identity

The report's sentence "The cause has not been established" can be replaced with the PSS explanation above.

**Suggested record change.** Add these fields for each TA:
- `signed_digest`, the 32 bytes of the header hash;
- `unsigned_payload_sha256`.

Both are stable across rebuilds. A reviewer can then rebuild, compare the digest, and verify the signature with the kit key, instead of relying only on retention.

**If whole-file hashes must be stable.** Sign with `--algo TEE_ALG_RSASSA_PKCS1_V1_5_SHA256`, which is deterministic. OP-TEE verifies whichever algorithm the header names. I have not run this.

**Scope of the key.** The key is OP-TEE's public **default development key**, so the signature authenticates nothing beyond "built with this kit". The report's no-root-of-trust statement already covers that.

## Minor note

`compiler_identity` records the system `aarch64-linux-gnu-gcc` as it is **now**. The kernel `Image` was built earlier (`qemu_kernel_6p7_virtio_v1/PROVENANCE.md`). Its version matches the one in the provenance note, 13.3.0, but this is not proof that the same binary built it. Only the gcc driver is hashed, not `cc1`, `as` or `ld`. Neither point needs a change before citation.

## Status

The local QEMU demonstration is provenance-complete, and the TA builds are reproducible apart from their signatures. R13-1 is a wording change plus two optional record fields.

The claim limits in the report remain accurate:
- the Authority is a QEMU-only variant;
- the HMAC key is a public test key, and the TA key is a public default key;
- the effect is a client marker;
- no Board B, RPMB, target or release authority is granted.

**Still open, outside this run:**
- the production signer;
- the inherited red `cfv_write_result_integrity_v1` suite;
- committing the work (on request);
- the XX1 and `ABORT_LOCAL` scope decision.

## Not verified

- **QEMU was not re-run.**
- **A PKCS#1 v1.5-signed TA loading in this QEMU OP-TEE build.**
- **The provenance of the kernel `Image` build,** beyond its hash.

## R13-1 closure check (revised report, `TA_STABLE_IDENTITY.json`, `ta_stable_identity.py`)

**Closed.** The report now gives the cause as PSS random salt, and it rests reproducibility on the **unsigned image** while making no claim about the signed file. It also says plainly that the derivation was added after the run and that QEMU was not re-run.

### Checked

**`ta_stable_identity.py --check`.** It gives `TA_STABLE_IDENTITY=PASS`. The script's own hash, `1debd124…`, equals the `derivation_script_sha256` in its output.

**The parser (`:24-42`) is strict.**
- It requires magic `HSTO`, type 1 (bootstrap TA), algorithm PSS, a 32-byte hash and a 256-byte signature.
- It requires `len(payload) == image_size + 20`, the bootstrap header.
- It requires `SHA-256(shdr ‖ payload) == signed_digest`.
- It verifies PSS-SHA256 (MGF1, 32-byte salt) against a key whose hash must equal `RUN_RECORD.ta_dev_kit.default_ta_key_sha256`.

**The group checks (`:58-64`).** One digest and one payload hash per family, and a distinct signature for each file.

**My own check.** For all eight entries, `whole_file_sha256` equals the `child_ta` or `authority_ta` recorded in that run's own `RUN_RECORD.json`: smoke, then V1 to V4. The identities are therefore tied to the files that ran, and earlier I confirmed those match the ramdisk contents. The values agree with my R13 split.

**Manifest.** `SHA256SUMS.txt` verifies, now with 37 entries.

### Notes (no change needed for this run)

- **The manifest changed after the run.** `SHA256SUMS.txt` was regenerated at 16:22 to add `TA_STABLE_IDENTITY.json`. `RUN_RECORD.json` (16:09) is untouched, and the other 36 entries still verify. The report's statement that the original run record is unchanged is true, but the run directory's manifest **is** a post-run edit. For future runs, keep post-run derivations in a separate subdirectory with its own manifest, so the run-time manifest is never rewritten.
- **The tie to the run records is not in the script.** The script does not itself compare each `whole_file_sha256` with the hash recorded in that run's record. I did that by hand above, and it is a one-line addition if wanted.
- **The V1 child.** V1 has no separate child entry, because it used the smoke-run child TA (`34c22a8a…`), which I confirmed earlier from the V1 ramdisk. So `smoke_child` stands for V1's child.

### Status

**The TFP QEMU evidence chain, from V1 to V4 plus the stable identity, has no open review items.** What remains is outside these runs:
- the production signer;
- the inherited red `cfv_write_result_integrity_v1` suite;
- committing the work (on request);
- the XX1 and `ABORT_LOCAL` scope decision.
