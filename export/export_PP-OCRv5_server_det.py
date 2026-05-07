from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT_DIR = SCRIPT_DIR.parent


def getenv_path(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser().resolve()


def ensure_file(path: Path, desc: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{desc} not found: {path}")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def print_train_config_summary(train_config_path: Path) -> None:
    pattern = re.compile(r"(model:|module:|dataset_dir:|save_dir:|vdl_log_dir:)")
    print()
    print("Pre-check: train config summary")
    for idx, line in enumerate(train_config_path.read_text(encoding="utf-8").splitlines(), 1):
        if pattern.search(line):
            print(f"{idx}:{line}")


def main() -> int:
    root_dir = getenv_path("ROOT_DIR", str(DEFAULT_ROOT_DIR))
    conda_env = os.environ.get("CONDA_ENV")
    conda_exe = os.environ.get("CONDA_EXE")
    python_bin = os.environ.get("PYTHON_BIN", sys.executable)

    config_path = getenv_path(
        "CONFIG_PATH",
        str(root_dir / "paddlex/configs/modules/text_detection/PP-OCRv5_server_det.yaml"),
    )
    weight_dir = getenv_path("WEIGHT_DIR", str(root_dir / "weights/best_accuracy"))
    weight_path = getenv_path("WEIGHT_PATH", str(weight_dir / "best_accuracy.pdparams"))
    train_config_path = getenv_path("TRAIN_CONFIG_PATH", str(weight_dir / "config.yaml"))
    export_dir = getenv_path("EXPORT_DIR", str(root_dir / "inference"))

    home_dir = getenv_path("HOME_DIR", str(root_dir / ".home"))
    cache_dir = getenv_path("CACHE_DIR", str(root_dir / ".cache"))
    pdx_cache_dir = getenv_path("PDX_CACHE_DIR", str(root_dir / ".paddlex_cache"))
    mpl_dir = getenv_path("MPL_DIR", str(root_dir / ".matplotlib"))

    for path in (home_dir, cache_dir, pdx_cache_dir, mpl_dir, export_dir):
        ensure_dir(path)

    ensure_file(config_path, "Base config")
    ensure_file(weight_path, "Weight file")
    ensure_file(train_config_path, "Train config")

    print("Exporting PP-OCRv5_server_det with:")
    print(f"  ROOT_DIR={root_dir}")
    print(f"  PYTHON_BIN={python_bin}")
    print(f"  CONDA_ENV={conda_env or '<not set>'}")
    print(f"  CONFIG_PATH={config_path}")
    print(f"  WEIGHT_PATH={weight_path}")
    print(f"  TRAIN_CONFIG_PATH={train_config_path}")
    print(f"  EXPORT_DIR={export_dir}")

    print_train_config_summary(train_config_path)

    print()
    print("Important:")
    print("  - TRAIN_CONFIG_PATH must be the config.yaml from the same run as best_accuracy.pdparams")
    print("  - For local evaluate, pass Global.dataset_dir explicitly if train config still points to Kaggle paths")

    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home_dir),
            "XDG_CACHE_HOME": str(cache_dir),
            "PADDLE_PDX_CACHE_HOME": str(pdx_cache_dir),
            "MPLCONFIGDIR": str(mpl_dir),
            "TMPDIR": str(cache_dir),
            "PYTHONNOUSERSITE": "1",
        }
    )

    base_cmd = [
        python_bin,
        str(root_dir / "main.py"),
        "-c",
        str(config_path),
        "-o",
        "Global.mode=export",
        "-o",
        f"Global.output={export_dir}",
        "-o",
        "Global.device=cpu",
        "-o",
        f"Export.weight_path={weight_path}",
    ]

    if conda_env:
        conda_runner = conda_exe or "conda"
        cmd = [conda_runner, "run", "-n", conda_env, *base_cmd]
    else:
        cmd = base_cmd

    print()
    print("Running command:")
    print(" ".join(cmd))

    completed = subprocess.run(cmd, env=env)
    return completed.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        if "Train config" in str(exc):
            print(
                "You must download config.yaml from the same Kaggle training run.",
                file=sys.stderr,
            )
        raise
