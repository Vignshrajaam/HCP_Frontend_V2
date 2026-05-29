import os
import zipfile
import tarfile
from pathlib import Path


def extract_all_archives_recursive(input_path, extract_dir):
    """
    Recursively extracts ZIP / tar / tar.xz archives.
    Mirrors the backend's archive_utils exactly so the same ZIP works
    in both the CLI and the Streamlit frontend.

    Structure for HCP ZIPs:
        ZIP  →  node_101.tar.xz  →  access-logs-YYYYMMDD.tar  →  http_gateway_request.log.*
    """
    extracted_files = []

    if input_path.endswith(".zip"):
        with zipfile.ZipFile(input_path, "r") as z:
            z.extractall(extract_dir)
            for name in z.namelist():
                extracted_files.append(os.path.join(extract_dir, name))

    elif input_path.endswith(".tar.xz") or input_path.endswith(".tar"):
        with tarfile.open(input_path, "r:*") as t:
            t.extractall(extract_dir, filter="data")
            for member in t.getnames():
                extracted_files.append(os.path.join(extract_dir, member))

    else:
        extracted_files.append(input_path)

    # Recurse into any archive that was just extracted
    for f in extracted_files:
        if os.path.isfile(f) and (
            f.endswith(".zip") or f.endswith(".tar.xz") or f.endswith(".tar")
        ):
            subdir = os.path.join(extract_dir, Path(f).stem)
            os.makedirs(subdir, exist_ok=True)
            extract_all_archives_recursive(f, subdir)

    return extract_dir
