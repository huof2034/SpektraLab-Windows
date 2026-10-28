#!/usr/bin/env python3
"""Package and verify exact native dependency sources used by this Windows build."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--deps', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
deps = args.deps.resolve()
entries = []

def add(path, expected, source):
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise RuntimeError(f'{path}: checksum mismatch {actual}')
    entries.append((path.name, data, source, actual))

add(deps/'LibRaw-0.22.2.zip', '02275a04cf0d1477ab9fd7ee231ddea59e7b14497458da6e3ba957517d6655c7',
    'https://codeload.github.com/LibRaw/LibRaw/zip/refs/tags/0.22.2')
for name, expected, url in [
    ('libjpeg-turbo-3.2.0.tar.gz','6f30092cef9fb839779646608f4ee14ae3cbac989c47fa05e841b0841f09878e','https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/3.2.0/libjpeg-turbo-3.2.0.tar.gz'),
    ('libpng-1.6.59.tar.xz','d80dd2a38a37f803cb9b6ac7b14bd6e74ddc3b654780a8380bdf93523fdb4389','https://downloads.sourceforge.net/libpng/libpng-1.6.59.tar.xz'),
    ('zlib-ng-2.3.3.tar.gz','f9c65aa9c852eb8255b636fd9f07ce1c406f061ec19a2e7d508b318ca0c907d1','https://codeload.github.com/zlib-ng/zlib-ng/tar.gz/refs/tags/2.3.3'),
]:
    add(deps/'export-codecs'/name, expected, url)
for pin in json.loads((ROOT/'engine/cmake/input-codecs-pins.json').read_text(encoding='utf-8')):
    add(deps/'input-codecs'/(pin['name']+'.tar.gz'), pin['sha256'], pin['url'])
pins = json.loads((ROOT/'engine/cmake/lens-codecs-pins.json').read_text(encoding='utf-8-sig'))
for pin in pins['sources']:
    ext = '.tar.xz' if pin['url'].endswith('.xz') else '.tar.gz'
    add(deps/'lens-codecs'/(pin['name']+ext), pin['sha256'], pin['url'])
for pin in pins['wraps']:
    add(deps/'lens-codecs/glib-2.86.5/subprojects/packagecache'/pin['name'], pin['sha256'], pin['url'])

git_sources = [(deps/'Vulkan-Headers', 'b5c8f996196ba4aa6d8f97e52b5d3b6e70f7e4e2', 'Vulkan-Headers', 'https://github.com/KhronosGroup/Vulkan-Headers')]
for pin in pins['git']:
    git_sources.append((deps/'lens-codecs/glib-2.86.5/subprojects'/pin['name'], pin['revision'], pin['name'], pin['url']))
for path, revision, name, url in git_sources:
    actual = subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'], text=True).strip()
    if actual != revision:
        raise RuntimeError(f'{path}: revision {actual} differs from {revision}')
    data = subprocess.check_output(['git','-C',str(path),'archive','--format=tar',revision])
    entries.append((f'{name}-{revision}.tar', data, f'{url} @ {revision}', hashlib.sha256(data).hexdigest()))

names = [x[0] for x in entries]
if len(names) != len(set(names)):
    raise RuntimeError('Duplicate dependency archive names')
args.output.parent.mkdir(parents=True, exist_ok=True)
if args.output.exists():
    raise RuntimeError(f'Output exists: {args.output}')
manifest = [{'file':name, 'sha256':digest, 'source':url} for name,_,url,digest in entries]
with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for name,data,_,_ in entries:
        archive.writestr('sources/'+name, data)
    archive.writestr('MANIFEST.json', json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    archive.writestr('SHA256SUMS.txt', ''.join(f'{digest}  sources/{name}\n' for name,_,_,digest in entries))
    archive.writestr('README.txt', 'Exact native dependency source archives, pins and SHA-256 values used for this build.\nGit snapshots are archive exports of the pinned commits. See repository THIRD_PARTY_NOTICES.md and WINDOWS_BUILD.md.\n')
print(f'Wrote {args.output}: {len(entries)} verified source archives')
