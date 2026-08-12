# YOLOv8 Python File Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move all personal YOLOv8 root scripts into categorized current examples or legacy archive and remove the classifier's machine-specific checkpoint path.

**Architecture:** Preserve the upstream `ultralytics/` layout and top-level functional packages. Run current examples as modules from repository root so `ultralytics`, `refine`, and `proxy_package` imports remain stable.

**Tech Stack:** Python, Ultralytics YOLOv8, PyTorch, Git

## Global Constraints

- Keep `setup.py`, `refine/`, `proxy_package/`, and `ultralytics/` in place.
- Keep `flask_yolo.py` as the current service and archive `flask_yolo1.py`.
- Do not change YOLOv8 tracking thresholds or classifier architecture.
- Do not push to the official `upstream` remote.

---

### Task 1: Move and classify root scripts

**Files:**
- Move: `flask_yolo.py` to `examples/dust/web/serve.py`
- Move: `flask_yolo1.py` to `archive/legacy/web/flask_yolo1.py`
- Move: remaining personal scripts into classification, preprocessing, or experiments
- Create: package `__init__.py` files

**Interfaces:**
- Consumes: repository-root module execution
- Produces: categorized scripts with stable top-level package imports

- [ ] Move files with `git mv` according to the approved design.
- [ ] Compile all moved scripts.
- [ ] Verify current service imports without loading model weights.

### Task 2: Make classifier checkpoint portable

**Files:**
- Modify: `proxy_package/models/efficientnetv2/efficientnetv2_s.py`
- Modify: `proxy_package/root_test.py`

**Interfaces:**
- Consumes: optional checkpoint path supplied by caller
- Produces: repository-relative default checkpoint path with a clear missing-file error

- [ ] Add a focused test or direct assertion for absence of the old `D:\pythonProject` path.
- [ ] Replace the absolute default with `Path(__file__).with_name('Train_Epoch266-Loss0.046.pth')` or an explicit caller argument.
- [ ] Compile and inspect the classification loader call path.

### Task 3: Verify, document, commit, and push

**Files:**
- Modify: `README.md`
- Modify: `docs/script-inventory.md`

**Interfaces:**
- Consumes: final directory tree
- Produces: published organization change with upstream remote preserved

- [ ] Update README commands and inventory paths.
- [ ] Run focused `refine` tests, compile checks, root-file audit, and forbidden-file audit.
- [ ] Commit `refactor: organize YOLOv8 experiment scripts`.
- [ ] Push only to `origin/main`; verify `upstream` remains official Ultralytics.
