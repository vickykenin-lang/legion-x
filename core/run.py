import argparse
import json
from dataclasses import asdict

from legion_x import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LEGION-X core vertical slice")
    parser.add_argument("--seed", default="legion-x-day-0")
    parser.add_argument("--database", default="data/runtime/legion_x.sqlite3")
    args = parser.parse_args()
    print(json.dumps(asdict(run_pipeline(args.seed, args.database)), indent=2))


if __name__ == "__main__":
    main()
