from argparse import ArgumentParser
from pathlib import Path
import json

from .io import read_jobs, read_rows, write_rows
from .planner import expand
from .report import summarize
from .runner import run


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("config")

    execute = sub.add_parser("run")
    execute.add_argument("plan")
    execute.add_argument("--out", required=True)
    execute.add_argument("--binary", default="llama-cli")

    report = sub.add_parser("report")
    report.add_argument("path")

    args = parser.parse_args()

    if args.cmd == "plan":
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        for job in expand(config):
            print(json.dumps(job.to_dict(), sort_keys=True))
    elif args.cmd == "run":
        rows = [run(job, args.binary) for job in read_jobs(args.plan)]
        write_rows(args.out, rows)
        print(json.dumps({
            "jobs": len(rows),
            "successful": sum(bool(row["ok"]) for row in rows),
        }))
    else:
        print(json.dumps(summarize(read_rows(args.path)), indent=2))


if __name__ == "__main__":
    main()
