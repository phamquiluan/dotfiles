#!/usr/bin/env python3
"""Research state store: ideas index, experiment ledger, findings.

Layout, rooted at <project>/research/ :

    WORKSPACE.md      project specifics every mode reads first
    IDEAS.md          idea list, one "## I<n> <title>" section per idea
    STORY.md          the paper's argument; its "as of EXP-<id>" line drives
                      staleness, so keep that line current
    LEDGER.jsonl      one JSON object per run; edit only through this script
    findings/         one EXP-<id>.md failure-analysis note per analysed run
    deep/             dive-deep notes: paper-, code-, data-, run-<slug>.md
    reviews/          self-reviews of the draft, plus their triage
    runs/EXP-<id>/    raw artefacts pulled back, one directory per run

research/ is its own local-only git repository, separate from the code repo
and the paper repo; `init` creates it, and every mode ends by committing the
state it changed. State that drives routing is recorded in the files, never
inferred from filesystem timestamps: git resets every mtime. Hence the
`analysed` and `decided` flags and STORY.md's "as of" line.

Every subcommand prints JSON to stdout so the caller can parse it.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

IDEA_RE = re.compile(r"^##\s+(I\d+)\s+(.*?)\s*$", re.M)
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(\S+)", re.M)
STORY_AS_OF_RE = re.compile(r"as of\s+(EXP-\d+)", re.I)
EXP_ID_RE = re.compile(r"EXP-(\d+)$")

LIVE = ("proposed", "active", "revised")
IN_FLIGHT = ("queued", "running")
TERMINAL = ("done", "failed")
STATUSES = ("planned",) + IN_FLIGHT + TERMINAL
KINDS = ("main", "ablation", "sensitivity", "baseline", "probe")
# kinds whose numbers are compared across runs must pin what they ran on
CONFIG_REQUIRED = ("main", "ablation", "sensitivity", "baseline")
CONFIG_KEYS = ("dataset", "seed")

IDEAS_HEADER = """# Ideas

One section per idea. Keep `**Status:**` current and keep it the FIRST
`**Status:**` line in the section: superseded text moved under a `Previously`
heading must not carry its own Status line above the current one.

Statuses: `proposed` (ideate), `active` (experiment, at first run), `revised`,
`parked`, `dropped` (all three: revise).

"""

GITIGNORE = """runs/
.ledger.lock
*.tmp
"""

WORKSPACE_TEMPLATE = """# Workspace

Project specifics. Every mode reads this first, so what is written here
overrides the generic guidance in the skill. Delete lines that do not apply.

## Repositories

- Code: project root; `implement` commits here, ledger `commit` points here
- Paper: directory and remote, if separate from the code repo
- Research: this directory, local-only git created by init; commit every pass
- Test suite command:     e.g. `pytest tests/ -x -q`, run before any submission

## Paper

- Directory:
- Build:                  e.g. `make main 2>&1 | tail -10`
- Table generation:       e.g. `make tables`, regenerating table/ from output
- Figure generation:      e.g. `python scripts/figures.py`, writing figure/*.pdf
- Venue and deadline:

## Compute

- Where jobs run:         e.g. the `katana` skill (UNSW PBS cluster)
- Reconciling job state:  how to check whether a submitted job has finished

## Code and data

- Baseline code catalogue: e.g. `artifacts/_cards/INDEX.md`, read before any
  repo tree
- Datasets and where they live:
- Synthetic generators available:

## Literature

- Search tools:           e.g. the `search-related-works` skill
"""


def root(args):
    return os.path.abspath(os.path.join(args.project, "research"))


def ledger_path(args):
    return os.path.join(root(args), "LEDGER.jsonl")


def ideas_path(args):
    return os.path.join(root(args), "IDEAS.md")


def read_ledger(args):
    path = ledger_path(args)
    if not os.path.exists(path):
        return []
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_ledger(args, records):
    """Rewrite atomically so a crashed or concurrent run cannot truncate it."""
    path = ledger_path(args)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            for rec in records:
                fh.write(json.dumps(rec) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


class locked(object):
    """Advisory lock around read-modify-write, for concurrent sessions."""

    def __init__(self, args):
        self.path = os.path.join(root(args), ".ledger.lock")

    def __enter__(self):
        self.fh = open(self.path, "w")
        try:
            import fcntl
            fcntl.flock(self.fh, fcntl.LOCK_EX)
        except (ImportError, OSError):
            pass
        return self

    def __exit__(self, *exc):
        self.fh.close()
        return False


def read_ideas(args):
    path = ideas_path(args)
    if not os.path.exists(path):
        return [], []
    text = open(path).read()
    ideas, warnings = [], []
    matches = list(IDEA_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        found = STATUS_RE.findall(body)
        if len(found) > 1:
            warnings.append("%s has %d **Status:** lines; the first (%s) is used"
                            % (m.group(1), len(found), found[0]))
        ideas.append({
            "id": m.group(1),
            "title": m.group(2),
            "status": found[0] if found else "unknown",
        })
    return ideas, warnings


def exp_num(rec_id):
    m = EXP_ID_RE.match(rec_id or "")
    return int(m.group(1)) if m else 0


def next_exp_id(records):
    return "EXP-%04d" % (max([exp_num(r.get("id", "")) for r in records] or [0]) + 1)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def git_commit(project):
    """Short HEAD of the project repo, or None when it is not a git repo."""
    try:
        out = subprocess.run(["git", "-C", project, "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return (out.stdout.strip() or None) if out.returncode == 0 else None


def story_state(base, records):
    """Stale when STORY.md predates the newest finished run.

    Keyed on the "as of EXP-<id>" line rather than mtime, so the signal
    survives a git clone.
    """
    path = os.path.join(base, "STORY.md")
    if not os.path.exists(path):
        return {"exists": False, "stale": True, "why": "no STORY.md yet"}
    m = STORY_AS_OF_RE.search(open(path).read())
    if not m:
        return {"exists": True, "stale": True, "as_of": None,
                "why": 'STORY.md has no "as of EXP-<id>" line, so it cannot be checked'}
    as_of = m.group(1)
    newer = sorted(r["id"] for r in records
                   if r["status"] == "done" and exp_num(r["id"]) > exp_num(as_of))
    if newer:
        return {"exists": True, "stale": True, "as_of": as_of,
                "why": "%d run(s) finished after %s: %s"
                       % (len(newer), as_of, ", ".join(newer[:5]))}
    return {"exists": True, "stale": False, "as_of": as_of,
            "why": "STORY.md reflects every finished run"}


def emit(obj):
    print(json.dumps(obj, indent=2))


def init_git(base):
    """Local-only repo tracking research state; every mode commits to it."""
    if os.path.isdir(os.path.join(base, ".git")):
        return "already a repo"
    try:
        subprocess.run(["git", "init", "-q", base],
                       check=True, timeout=10, capture_output=True)
        subprocess.run(["git", "-C", base, "add", "-A"],
                       check=True, timeout=10, capture_output=True)
        subprocess.run(["git", "-C", base, "commit", "-q", "-m",
                        "init: research state scaffold"],
                       check=True, timeout=10, capture_output=True)
    except (OSError, subprocess.SubprocessError):
        return "git init or first commit failed; create the repo by hand"
    return "initialised, scaffold committed"


def cmd_init(args):
    base = root(args)
    created = []
    for sub in ("", "findings", "deep", "reviews", "runs"):
        path = os.path.join(base, sub)
        if not os.path.isdir(path):
            os.makedirs(path)
            created.append(os.path.join(path, ""))
    for name, body in (("IDEAS.md", IDEAS_HEADER),
                       ("WORKSPACE.md", WORKSPACE_TEMPLATE),
                       ("LEDGER.jsonl", ""),
                       (".gitignore", GITIGNORE)):
        path = os.path.join(base, name)
        if not os.path.exists(path):
            with open(path, "w") as fh:
                fh.write(body)
            created.append(path)
    emit({"root": base, "created": created, "git": init_git(base),
          "next": "fill in research/WORKSPACE.md before running a mode; "
                  "add research/ to the code repo's .gitignore"})


def cmd_add(args):
    config = json.loads(args.config) if args.config else {}
    if args.kind in CONFIG_REQUIRED:
        missing = [k for k in CONFIG_KEYS if k not in config]
        if missing:
            emit({"error": "--config for kind '%s' must pin %s"
                           % (args.kind, " and ".join(missing)),
                  "why": "runs of this kind get compared; an unpinned config "
                         "cannot be audited later",
                  "hint": '--config \'{"dataset":"ncmapss","seed":0}\''})
            return 1
    with locked(args):
        records = read_ledger(args)
        rec = {
            "id": next_exp_id(records),
            "idea": args.idea,
            "kind": args.kind,
            "hypothesis": args.hypothesis,
            "config": config,
            "status": args.status,
            "job": args.job,
            "metrics": {},
            "notes": args.notes or "",
            "analysed": False,
            "decided": False,
            "commit": args.commit or git_commit(args.project),
            "data_version": args.data_version,
            "created": now(),
            "finished": None,
        }
        with open(ledger_path(args), "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    emit(rec)
    return 0


def cmd_update(args):
    with locked(args):
        records = read_ledger(args)
        hit = next((r for r in records if r["id"] == args.id), None)
        if hit is None:
            emit({"error": "no such experiment", "id": args.id})
            return 1
        if args.status:
            hit["status"] = args.status
            if args.status in TERMINAL and not hit.get("finished"):
                hit["finished"] = now()
        for field in ("job", "idea", "kind", "hypothesis", "commit", "data_version"):
            val = getattr(args, field, None)
            if val:
                hit[field] = val
        if args.config:
            hit["config"] = json.loads(args.config)
        if args.metrics:
            hit["metrics"].update(json.loads(args.metrics))
        if args.notes:
            hit["notes"] = (hit["notes"] + "\n" if hit["notes"] else "") + args.notes
        if args.analysed:
            hit["analysed"] = True
        if args.decided:
            hit["decided"] = True
        write_ledger(args, records)
    emit(hit)
    return 0


def cmd_list(args):
    records = read_ledger(args)
    for field in ("idea", "status", "kind"):
        want = getattr(args, field)
        if want:
            records = [r for r in records if r.get(field) == want]
    emit(records)


def cmd_show(args):
    for rec in read_ledger(args):
        if rec["id"] == args.id:
            emit(rec)
            return 0
    emit({"error": "no such experiment", "id": args.id})
    return 1


def cmd_status(args):
    base = root(args)
    if not os.path.isdir(base):
        emit({"initialised": False, "suggested_mode": "ideate",
              "why": "no research/ directory yet"})
        return 0
    ideas, warnings = read_ideas(args)
    records = read_ledger(args)

    def listdir(sub):
        path = os.path.join(base, sub)
        return sorted(f for f in os.listdir(path) if f.endswith(".md")) \
            if os.path.isdir(path) else []

    active = [i for i in ideas if i["status"] in LIVE]
    planned = [r for r in records if r["status"] == "planned"]
    in_flight = [r for r in records if r["status"] in IN_FLIGHT]
    done = [r for r in records if r["status"] in TERMINAL]
    unanalysed = [r for r in done if not r.get("analysed")]
    undecided = [r for r in done if r.get("analysed") and not r.get("decided")]
    findings, deep, reviews = listdir("findings"), listdir("deep"), listdir("reviews")
    story = story_state(base, records)

    if not os.path.exists(os.path.join(base, "WORKSPACE.md")):
        warnings.append("no research/WORKSPACE.md; project specifics are unrecorded")
    if not os.path.isdir(os.path.join(base, ".git")):
        warnings.append("research/ is not a git repo; run init to create the "
                        "local progress repo")

    if not active:
        mode, why = "ideate", "no live ideas"
    elif unanalysed:
        mode, why = "analyze", "%d finished run(s) not yet analysed" % len(unanalysed)
    elif in_flight:
        mode, why = "experiment", ("%d run(s) still in flight; reconcile them "
                                   "against the cluster first" % len(in_flight))
    elif undecided:
        mode, why = "revise", "%d analysed run(s) awaiting a decision" % len(undecided)
    elif planned:
        mode, why = "experiment", "%d run(s) planned but not submitted" % len(planned)
    elif not records:
        mode, why = "experiment", "live idea with no runs yet"
    else:
        mode, why = "experiment", "runs complete, findings all acted on"

    also = None
    if story["stale"] and done and mode == "experiment" and not in_flight:
        also = "paper-writing"
        why += "; STORY.md is stale (%s)" % story["why"]

    emit({
        "initialised": True,
        "root": base,
        "ideas": ideas,
        "counts": {
            "ideas": len(ideas), "live_ideas": len(active),
            "runs": len(records), "planned": len(planned),
            "in_flight": len(in_flight), "unanalysed": len(unanalysed),
            "undecided": len(undecided), "findings": len(findings),
            "deep_notes": len(deep), "reviews": len(reviews),
        },
        "in_flight": [{"id": r["id"], "job": r.get("job")} for r in in_flight],
        "unanalysed": [r["id"] for r in unanalysed],
        "undecided": [r["id"] for r in undecided],
        "deep_notes": [os.path.splitext(f)[0] for f in deep],
        "reviews": [os.path.splitext(f)[0] for f in reviews],
        "story": story,
        "warnings": warnings,
        "suggested_mode": mode,
        "also_consider": also,
        "why": why,
    })
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--project", default=".", help="project root holding research/")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create the research/ scaffold")
    sub.add_parser("status", help="state summary plus suggested mode")

    a = sub.add_parser("add", help="append an experiment record")
    a.add_argument("--idea", required=True, help="idea id, e.g. I2")
    a.add_argument("--kind", required=True, choices=KINDS)
    a.add_argument("--hypothesis", required=True, help="what this run tests")
    a.add_argument("--config", help="JSON config; must pin dataset and seed "
                                    "for every kind except probe")
    a.add_argument("--status", default="planned", choices=STATUSES,
                   help="planned (not submitted) or queued/running (has a job)")
    a.add_argument("--job", help="cluster job id")
    a.add_argument("--commit", help="code version (default: git HEAD of --project)")
    a.add_argument("--data-version", help="dataset name/version this run consumed")
    a.add_argument("--notes")

    u = sub.add_parser("update", help="amend an experiment record")
    u.add_argument("id")
    u.add_argument("--status", choices=STATUSES)
    u.add_argument("--job")
    u.add_argument("--idea", help="correct a mistyped idea id")
    u.add_argument("--kind", choices=KINDS, help="correct a mistyped kind")
    u.add_argument("--hypothesis", help="correct the recorded hypothesis")
    u.add_argument("--config", help="replace the config JSON outright")
    u.add_argument("--commit")
    u.add_argument("--data-version")
    u.add_argument("--metrics", help="JSON object merged into metrics")
    u.add_argument("--notes", help="appended to notes")
    u.add_argument("--analysed", action="store_true",
                   help="analyze wrote a finding for this run")
    u.add_argument("--decided", action="store_true",
                   help="revise acted on that finding")

    l = sub.add_parser("list", help="list experiment records")
    l.add_argument("--idea")
    l.add_argument("--status", choices=STATUSES)
    l.add_argument("--kind", choices=KINDS)

    s = sub.add_parser("show", help="print one experiment record")
    s.add_argument("id")

    args = p.parse_args()
    fn = {"init": cmd_init, "add": cmd_add, "update": cmd_update,
          "list": cmd_list, "show": cmd_show, "status": cmd_status}[args.cmd]
    sys.exit(fn(args) or 0)


if __name__ == "__main__":
    main()
