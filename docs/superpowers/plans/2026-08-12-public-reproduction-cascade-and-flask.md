# YOLOv8 Public Reproduction, Cascade, and Flask Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a clean public YOLOv8 dust-detection repository with refine tracking, a self-contained YOLO→EfficientNetV2 cascade, reproducible CLIs, and a robust multi-camera Flask service.

**Architecture:** Keep Ultralytics core untouched. Project methods live under explicit `methods` packages; runners adapt Ultralytics results to these APIs. The Flask service shares detector/classifier instances in one inference worker while isolating per-stream temporal state.

**Tech Stack:** Python, PyTorch, OpenCV, Flask, PyYAML, pytest, Ultralytics YOLOv8.

## Global Constraints

- Preserve refine defaults and EfficientNetV2-S checkpoint tensor names/shape compatibility.
- Preserve 224×224 center-crop and mean/std 127.5 preprocessing unless a compatibility test proves otherwise.
- Support `auto`, CPU, and explicit CUDA devices.
- Do not commit weights, datasets, outputs, real RTSP URLs, credentials, or personal absolute paths.
- Do not modify Ultralytics core unless a documented compatibility requirement makes it unavoidable.

---

### Task 1: Refine tracking package

**Files:**
- Create: `methods/__init__.py`, `methods/refine_tracking/__init__.py`
- Move/modify: `refine/*.py` into focused snake-case files
- Modify: `tests/test_refine.py`
- Create: `tests/dust/test_refine_public_api.py`

**Interfaces:**
- Produces: `RefinePostprocessor.refine_box(detections, class_id)` and compatibility alias `NDS`.

- [ ] Add output-parity tests for empty, single, and temporal multi-frame sequences.
- [ ] Run tests and confirm the new import initially fails.
- [ ] Move code with package-qualified imports and explicit `__all__`, retaining algorithm constants.
- [ ] Run old and new tests; compare output tensors exactly where deterministic.
- [ ] Commit as `refactor: expose YOLOv8 refine tracking package`.

### Task 2: Characterize and extract EfficientNetV2 cascade

**Files:**
- Create: `tests/dust/test_cascade_compatibility.py`
- Create: `methods/yolo_efficientnetv2/__init__.py`
- Create: `methods/yolo_efficientnetv2/model/efficientnetv2.py`
- Create: `methods/yolo_efficientnetv2/config.py`
- Create: `methods/yolo_efficientnetv2/pipeline.py`
- Create: `methods/yolo_efficientnetv2/classifier.py`
- Move: `classify/annotations.txt` -> `methods/yolo_efficientnetv2/labels.txt`

**Interfaces:**
- Produces: `Classification(label: str, confidence: float, index: int)`.
- Produces: `EfficientNetV2Classifier(checkpoint, labels=None, device="auto")` and `classify(image) -> Classification`.

- [ ] Build an import/dependency manifest from `InferenceModel`, `BuildNet`, EfficientNetV2-S, global average pooling, linear head, preprocessing, and checkpoint loading; record only the reachable files.
- [ ] Add compatibility tests asserting parameter key/shape sets, preprocessing output shape/value range, label order, checkpoint formats (`state_dict`, `model`, or direct mapping), load-once behavior, and class-0 decision semantics.
- [ ] Run tests against a thin adapter over the old implementation and capture failures caused by broken imports.
- [ ] Extract the necessary model layers and helpers into the method package, using package-local imports and no registry that eagerly imports unused models.
- [ ] Implement safe checkpoint normalization, `torch.inference_mode()`, softmax confidence, structured results, and device resolution.
- [ ] Run compatibility tests with a synthetic state dict; if the private checkpoint is available locally, compare old/new logits without tracking it.
- [ ] Commit as `refactor: extract EfficientNetV2 cascade classifier`.

### Task 3: Cascade pipeline and command-line runners

**Files:**
- Create: `methods/yolo_efficientnetv2/cascade.py`
- Create: `scripts/run_cascade.py`
- Create: `scripts/run_tracking.py`
- Create: `tests/dust/test_cascade_pipeline.py`
- Create: `tests/dust/test_dust_clis.py`

**Interfaces:**
- Produces: `expand_and_clip_box(box, image_shape, ratio=0.125)`.
- Produces: `CascadePipeline(detector, classifier, candidate_class_ids)` and `process(frame)`.
- CLIs accept weights, source, device, thresholds, output, and candidate class IDs.

- [ ] Test class filtering, 1/8 expansion, integer clipped coordinates, empty/zero-area crop suppression, result-to-box association, and `--help` without loading weights.
- [ ] Run tests and verify missing implementation failures.
- [ ] Implement dependency-injected pipeline and structured cascade detections; never use tensors directly as NumPy slice indices.
- [ ] Implement tracking and cascade video runners with `try/finally` resource cleanup and optional output writing.
- [ ] Run focused tests and both `--help` commands.
- [ ] Commit as `feat: add YOLOv8 dust inference CLIs`.

### Task 4: Shared multi-camera service

**Files:**
- Create: `apps/flask_multicam/__init__.py`
- Create: `apps/flask_multicam/buffer.py`
- Create: `apps/flask_multicam/capture.py`
- Create: `apps/flask_multicam/service.py`
- Create: `tests/dust/test_multicam_service.py`

**Interfaces:**
- Produces versioned `LatestFrameBuffer`, reconnecting `CaptureWorker`, and `InferenceService`.
- Service modes are exactly `tracking` or `cascade` per stream configuration.

- [ ] Test overwrite semantics, multiple readers, reconnection, independent tracking state, classifier sharing, mode routing, and clean shutdown.
- [ ] Run tests and confirm missing modules fail.
- [ ] Implement one capture worker per source and one inference worker owning detector/classifier model calls.
- [ ] Ensure cascade streams do not instantiate refine state and tracking streams do not call the classifier.
- [ ] Run all service tests.
- [ ] Commit as `feat: add YOLOv8 multi-camera service`.

### Task 5: Flask application and configuration

**Files:**
- Create: `apps/flask_multicam/app.py`, `apps/flask_multicam/config.py`
- Create: `apps/flask_multicam/templates/index.html`
- Create: `configs/cameras.example.yaml`
- Create: `scripts/run_flask_multicam.py`
- Create: `tests/dust/test_flask_multicam.py`

**Interfaces:**
- Produces: `load_config(path) -> ServiceConfig`, `create_app(service) -> Flask`.
- Routes: `/`, `/streams`, `/video_feed/<stream_id>`, `/health`.

- [ ] Test configuration schema, supported modes, unknown stream 404, health state, multipart JPEG output, and side-effect-free imports.
- [ ] Run tests and verify failures.
- [ ] Implement app factory, redacted logging, dynamic stream page, and CLI host/port overrides.
- [ ] Add example tracking and cascade streams with placeholder sources and weight paths.
- [ ] Run tests and Flask CLI `--help`.
- [ ] Commit as `feat: add configurable YOLOv8 Flask app`.

### Task 6: Remove obsolete framework and personal files

**Files:**
- Delete: `proxy_package/` after replacement tests pass
- Delete: `archive/legacy/`, superseded `examples/dust/`, `refine.zip`, personal images/logs/output directories, IDE metadata, caches, and unneeded Python scripts
- Modify: `.gitignore`

- [ ] Run `rg` for every `proxy_package`, legacy, and example import; confirm all formal consumers use the new methods/CLIs.
- [ ] Compare tracked EfficientNetV2 dependency manifest with extracted files; resolve any missing reachable dependency before deletion.
- [ ] Remove superseded files using `apply_patch`, preserving licenses and attribution.
- [ ] Extend ignores for `*.pt`, `*.pth`, local configs, outputs, datasets, IDE files, caches, and training runs while retaining deliberate upstream assets.
- [ ] Scan tracked files for drive-letter paths, RTSP credentials, `.pyc`, generated media, archive files, and project-owned mojibake comments.
- [ ] Commit as `chore: remove private experiments and obsolete classifier framework`.

### Task 7: Documentation and attribution

**Files:**
- Create: `methods/refine_tracking/README.md`
- Create: `methods/yolo_efficientnetv2/README.md`
- Create: `docs/YOLOV8_CHANGES.md`
- Create: `docs/REPRODUCTION.md`
- Modify: `README.md`, `NOTICE.md`, dependency file as needed

- [ ] Document refine and cascade as distinct methods, including tensor data flow, class filtering, crop expansion, normalization, label semantics, checkpoint placement, and exact commands.
- [ ] Explain all project-owned changes relative to upstream Ultralytics and state that weights/data are not redistributed.
- [ ] Add iou-tracker repository attribution and license/source notes for reused code.
- [ ] Verify every documented path and `--help` option exists.
- [ ] Commit as `docs: document YOLOv8 dust reproduction methods`.

### Task 8: Final verification and publication

**Files:** All changed project files.

- [ ] Run focused refine, cascade, service, and Flask tests.
- [ ] Run `python -m compileall methods apps scripts tests/dust`.
- [ ] Run all three CLI `--help` commands.
- [ ] Run `git diff --check`, clean-status review, credential/path scans, tracked-large-file scan, and upstream-core diff check.
- [ ] Review the full change history for accidental checkpoint, dataset, output, or private-file publication.
- [ ] Push verified commits to `origin/main` without force pushing; retain `upstream` unchanged.

