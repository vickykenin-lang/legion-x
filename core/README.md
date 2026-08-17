# LEGION-X Core Vertical Slice

This zero-dependency Python prototype proves the first controlled flow:

`Oracle → Scripter → SQLite → Guardian`

## Run

```bash
cd legion_x_core
python run.py --seed first-mission
```

The command prints a structured content package and stores it in
`data/runtime/legion_x.sqlite3`.

## Test

```bash
cd legion_x_core
python -m unittest discover -s tests -v
```

This prototype is intentionally local and deterministic. Model providers,
visual generation, FFmpeg assembly, and publishing will be added behind stable
interfaces after this core state flow is proven.
