"""Mirror Google's Firebase Unity UPM tarballs as git-installable packages.

Usage: python update.py <version>   (e.g. 14.0.0), then commit and tag <version>.
Source: https://developers.google.com/unity/archive (dl.google.com).
"""
import io, json, shutil, sys, tarfile, urllib.request
from pathlib import Path

PACKAGES = ["com.google.firebase.app", "com.google.firebase.analytics"]
URL = "https://dl.google.com/games/registry/unity/{name}/{name}-{version}.tgz"
# Desktop players and tvOS: the game ships to Android and iOS only, and its editor never calls Firebase.
DROPPED_FOLDERS = {"x86_64", "tvOS"}
UNITY_EDM = ("com.unity.external-dependency-manager", "2.1.1")


def is_dropped(member_name):
    parts = member_name.split("/")
    parts[-1] = parts[-1][:-len(".meta")] if parts[-1].endswith(".meta") else parts[-1]
    return any(part in DROPPED_FOLDERS for part in parts)


def mirror(name, version, root):
    target = root / name
    if target.exists():
        shutil.rmtree(target)
    data = urllib.request.urlopen(URL.format(name=name, version=version)).read()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or is_dropped(member.name):
                continue
            relative = Path(member.name).relative_to("package")
            if ".." in relative.parts:
                raise ValueError(member.name)
            out = target / relative
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(archive.extractfile(member).read())
    manifest_path = target / "package.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    dependencies = manifest.get("dependencies", {})
    # Google's EDM4U package is deprecated for Unity's signed one, which ships the same assemblies.
    if dependencies.pop("com.google.external-dependency-manager", None) is not None:
        dependencies[UNITY_EDM[0]] = UNITY_EDM[1]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    for package in PACKAGES:
        mirror(package, sys.argv[1], Path(__file__).parent)
