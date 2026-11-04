"""Read the attributed additions to ordinary notes directly from Git objects."""
from pathlib import Path
import re
import subprocess

from .store import capture

TEXT = {".md", ".rst", ".txt", ".adoc"}
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def command(root, *args):
    return subprocess.check_output(["git", "--literal-pathspecs", "-C", str(root), *args])


def additions(patch):
    first = None
    text = []
    for line in patch.splitlines():
        hunk = HUNK.match(line)
        if hunk:
            if text:
                yield first, text
            first, text = int(hunk[1]), []
        elif first is not None and line.startswith("+"):
            text.append(line[1:])
    if text:
        yield first, text


def collect(store, root, revision_range, folder):
    """Import first-parent arrivals; blame added lines to their original committing author."""
    folder = Path(folder)
    if folder.is_absolute() or ".." in folder.parts or ".git" in folder.parts:
        raise ValueError("notes directory must be inside the repository")
    commits = command(root, "rev-list", "--reverse", "--first-parent", revision_range, "--", str(folder)).decode().splitlines()
    groups = []
    for sha in commits:
        parent = command(root, "show", "-s", "--format=%P", sha).decode().split()
        diff = ["diff", "--no-renames", parent[0], sha] if parent else ["diff-tree", "--no-commit-id", "--root", "-r", sha]
        paths = command(root, *diff, "--name-only", "--diff-filter=AM", "-z", "--", str(folder)).split(b"\0")
        members = []
        for raw in filter(None, paths):
            name = raw.decode("utf-8", "surrogateescape")
            if Path(name).suffix.lower() not in TEXT or (root / name).is_relative_to(store.root.resolve()):
                continue
            patch = command(root, *diff, "-p", "--no-ext-diff", "--unified=0", "--", name).decode("utf8", "replace")
            for first, lines in additions(patch):
                # A merge may introduce work by someone other than the merger.
                blame = command(root, "blame", "--line-porcelain", "-L", f"{first},+{len(lines)}", sha, "--", name).decode("utf8", "replace")
                runs = []
                for line in blame.splitlines():
                    if line.startswith("author "):
                        owner = line[7:]
                    elif line.startswith("\t"):
                        if not runs or runs[-1][0] != owner:
                            runs.append((owner, []))
                        runs[-1][1].append(line[1:])
                stamp = command(root, "show", "-s", "--format=%cI", sha).decode().strip()
                for owner, body in runs:
                    last = first + len(body) - 1
                    if any(line.strip() for line in body):
                        loc = f"git:{sha}:{name}#L{first}-L{last}"
                        members.append(capture(store, dict(owner=owner, observed_at=stamp,
                            source=dict(speaker=owner, location=loc, text="\n".join(body)))))
                    first = last + 1
        if members:
            groups.append(members)
    return groups
