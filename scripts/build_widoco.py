"""Build SHKG documentation with WIDOCO and the two rendering fixes."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
from urllib.request import urlopen

from patch_widoco_property_entries import JAR_SHA256, patch_jar


ROOT = Path(__file__).resolve().parents[1]
JAR_URL = (
    "https://github.com/dgarijo/Widoco/releases/download/v1.4.25/"
    "widoco-1.4.25-jar-with-dependencies_JDK-17.jar"
)


def get_jar(path):
    """Download the pinned WIDOCO JAR if absent; reject an unexpected checksum."""
    path = path.resolve()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(JAR_URL, timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != JAR_SHA256:
            raise ValueError("Downloaded WIDOCO JAR has an unexpected SHA-256")
        path.write_bytes(data)
    # patch_jar also checks the checksum when reusing a cached JAR.
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", default="java", help="Java 17 executable")
    parser.add_argument(
        "--jar", type=Path, default=ROOT / ".cache/widoco/widoco-1.4.25.jar",
        help="Original WIDOCO 1.4.25 JDK 17 JAR; downloaded if absent",
    )
    args = parser.parse_args()
    jar = patch_jar(
        get_jar(args.jar),
        ROOT / ".cache/widoco/widoco-1.4.25-property-entries.jar",
    )
    output = ROOT / "build/site"
    output.mkdir(parents=True, exist_ok=True)
    log_path = ROOT / "build/widoco.log"
    command = [
        args.java, "-Djava.awt.headless=true", "-Dfile.encoding=UTF-8",
        "-jar", str(jar), "-ontFile", str(ROOT / "soil_health_SKOS.ttl"),
        "-outFolder", str(output), "-confFile", str(ROOT / "widoco.properties"),
        "-rewriteAll", "-uniteSections", "-excludeProvenance",
        "-includeAnnotationProperties", "-lang", "en",
    ]
    print(f"Building with WIDOCO 1.4.25; log: {log_path}", flush=True)
    with log_path.open("w", encoding="utf-8") as log:
        subprocess.run(
            command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
            check=True, timeout=600,
        )

    # Serve the English page at the site root without changing its contents.
    shutil.copyfile(output / "index-en.html", output / "index.html")
    (output / ".nojekyll").touch()
    print(f"Documentation generated in {output}")
    print("Preview: python -m http.server 8000 --directory build/site")


if __name__ == "__main__":
    main()
