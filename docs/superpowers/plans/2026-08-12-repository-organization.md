# YOLOv8 Dust Detection Repository Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a clean, documented, testable `dust-detection-yolov8` repository while retaining the Ultralytics upstream history and the YOLOv8-adapted `refine` pipeline.

**Architecture:** Retain the upstream package layout and history, classify personal experiment code separately, and remove generated assets from the publication index without deleting local files. Keep the YOLOv8 `refine` adaptation distinct from YOLOv5 while documenting their shared algorithm.

**Tech Stack:** Python, PyTorch, NumPy, SciPy, Ultralytics YOLOv8, pytest, Git, GitHub Desktop

## Global Constraints

- Do not push to `ultralytics/ultralytics`.
- Do not delete datasets, weights, results, images, logs, archives, IDE settings, or unknown experiment files.
- Preserve existing staged and unstaged user work until each file is classified.
- Preserve YOLOv8-specific `refine` behavior and experimental thresholds.
- Cite `bochinski/iou-tracker` and retain its MIT copyright notice.
- Use explicit Git paths and audit the full index before every commit.

---

### Task 1: Audit and reset publication boundaries

**Files:**
- Modify: `.gitignore`
- Create: `LOCAL_ASSETS.md`
- Create: `docs/script-inventory.md`

**Interfaces:**
- Consumes: current 131-file index, unstaged changes, directory sizes, and import graph
- Produces: per-file keep/local-only classification without deleting files

- [ ] Export staged and unstaged file lists and classify each as upstream modification, experiment source, generated asset, dependency snapshot, or unknown.
- [ ] Add ignore rules for weights, training folders, crops, media, logs, archives, caches, and local model checkpoints.
- [ ] Remove generated/local-only files from the Git index using `git rm --cached` while retaining them on disk.
- [ ] Document local asset placement in `LOCAL_ASSETS.md` and uncertain script ownership in `docs/script-inventory.md`.
- [ ] Confirm `git status --short` no longer proposes generated assets for publication.

### Task 2: Document ownership and reproducibility

**Files:**
- Modify: `README.md`
- Create: `NOTICE.md`
- Create: `docs/chapter-4-algorithm.md`

**Interfaces:**
- Consumes: paper Chapter 4, Ultralytics upstream metadata, iou-tracker MIT license
- Produces: public project overview, attribution, comparison relationship, and reproduction instructions

- [ ] Add a prominent research-project section while retaining upstream attribution and useful Ultralytics documentation links.
- [ ] Document installation, asset placement, training, validation, inference, and `refine` integration with commands verified in this checkout.
- [ ] Add `NOTICE.md` with Ultralytics and iou-tracker URLs, license names, TU Berlin copyright, and modification statement.
- [ ] Explain the Chapter 4 modules and map `refine` files to the shared YOLOv5/YOLOv8 algorithm.
- [ ] Verify every referenced path and command locally.

### Task 3: Stabilize and test `refine`

**Files:**
- Modify: `refine/__init__.py`
- Modify: `refine/iou_giou_matching.py`
- Modify: `refine/track.py`
- Modify: `refine/Tracker.py`
- Modify: `refine/TSYDD.py`
- Modify: `refine/PPMove.py`
- Create: `tests/test_refine.py`

**Interfaces:**
- Consumes: detections shaped as `[x1, y1, x2, y2, confidence, class_id]`
- Produces: importable YOLOv8-adapted `refine` package with matching, tracking, and filtering APIs

- [ ] Write tests for identical/disjoint IoU, finite GIoU, track lifecycle, and tensor row filtering.
- [ ] Run `pytest tests/test_refine.py -v` and record initial failures.
- [ ] Convert package imports to relative imports and add concise UTF-8 module/API documentation without changing thresholds.
- [ ] Apply only test-proven numerical safety fixes.
- [ ] Run the focused tests and require all to pass.

### Task 4: Separate experiment code from generated assets

**Files:**
- Create: `examples/dust/README.md`
- Move: verified standalone personal scripts into `examples/dust/`
- Keep: `ultralytics/` upstream package structure

**Interfaces:**
- Consumes: script inventory and import graph
- Produces: discoverable examples without changing upstream package semantics

- [ ] Identify the minimal training, inference, Flask, crop, and classification examples used by the research project.
- [ ] Move only scripts with verified callers and update imports and documentation atomically.
- [ ] Keep dependency source snapshots such as `proxy_package/` local-only unless a live import proves they are required.
- [ ] Compile every moved or modified script and run its `--help` path when available.
- [ ] Record scripts that require unavailable weights/data as unexecuted integration checks.

### Task 5: Validate and prepare GitHub Desktop publication

**Files:**
- Modify: Git remote configuration only after the new repository exists

**Interfaces:**
- Consumes: reviewed source tree and preserved upstream history
- Produces: local `main` branch ready for `dust-detection-yolov8`

- [ ] Run focused tests and compile all project-modified Python files.
- [ ] Inspect staged extensions, largest staged files, tracked ignored files, and the complete diff from upstream commit `4bd62a2`.
- [ ] Commit reviewed changes as coherent documentation, core, and organization commits; never use an unreviewed all-files commit.
- [ ] In GitHub Desktop, create/publish `dust-detection-yolov8` under the user's account and preserve the official upstream URL in README/NOTICE.
- [ ] Confirm the new `origin` points to the user's repository and no push target points to `ultralytics/ultralytics`.
- [ ] Clone or inspect the published file list and run the README's minimal import test.

