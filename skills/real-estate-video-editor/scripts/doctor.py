"""Read-only capability inventory; never installs tools or models."""
import argparse
import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

NAMES = ['hyperframes', 'general-video', 'hyperframes-core',
         'hyperframes-animation', 'hyperframes-keyframes', 'hyperframes-creative',
         'hyperframes-audio', 'media-use', 'hyperframes-cli']

def run(exe, *args):
    if not exe or not Path(exe).is_file():
        return {'status': 'missing', 'path': str(exe) if exe else None}
    try:
        p = subprocess.run([str(exe), *args], capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=20,
                           env={**os.environ, 'HYPERFRAMES_NO_TELEMETRY': '1'})
        lines = (p.stdout + '\n' + p.stderr).strip().splitlines()
        return {'status': 'verified_command' if p.returncode == 0 else 'command_failed',
                'path': str(exe), 'exit_code': p.returncode, 'summary': lines[:2]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'status': 'command_failed', 'path': str(exe), 'error': str(exc)}

def inventory(workspace):
    extra = workspace / '.hyperframes-tools/python-asr'
    if extra.is_dir(): sys.path.insert(0, str(extra))
    user = Path.home()
    codex = Path(os.environ.get('CODEX_HOME', str(user / '.codex')))
    deps = user / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
    modules = workspace / '.hyperframes-tools/node_modules'
    roots = [('project-discovery', workspace / '.agents/skills'),
             ('project-legacy', workspace / '.codex/skills'),
             ('user', codex / 'skills'), ('user-agents', user / '.agents/skills')]
    plugins = codex / 'plugins/cache/openai-curated-remote/hyperframes'
    if plugins.is_dir():
        roots += [('plugin-bundle', p / 'skills') for p in sorted(plugins.iterdir()) if p.is_dir()]
    roots.append(('cli-bundled-reference', modules / 'hyperframes/dist/skills'))
    found = {name: [] for name in NAMES}
    for kind, root in roots:
        if root.is_dir():
            for f in root.glob('*/SKILL.md'):
                if f.parent.name in found:
                    found[f.parent.name].append({'kind': kind, 'path': str(f)})
    ff = modules / 'ffmpeg-static/ffmpeg.exe'
    fp = modules / 'ffprobe-static/bin/win32/x64/ffprobe.exe'
    node = shutil.which('node') or str(deps / 'node/bin/node.exe')
    tools = {'python': run(sys.executable, '--version'), 'node': run(node, '--version'),
             'ffmpeg': run(ff if ff.exists() else shutil.which('ffmpeg'), '-version'),
             'ffprobe': run(fp if fp.exists() else shutil.which('ffprobe'), '-version'),
             'npm_on_path': bool(shutil.which('npm') or shutil.which('npm.cmd')),
             'npx_on_path': bool(shutil.which('npx') or shutil.which('npx.cmd')),
             'tesseract': run(shutil.which('tesseract'), '--version'),
             'whisper_cli': run(shutil.which('whisper-cli') or shutil.which('whisper'), '--help')}
    cli = modules / 'hyperframes/bin/hyperframes.mjs'
    tools['hyperframes'] = run(node, str(cli), '--version') if cli.exists() else {'status': 'missing'}
    pkg = modules / 'hyperframes/package.json'
    if pkg.is_file():
        tools['hyperframes']['package_version'] = json.loads(pkg.read_text(encoding='utf-8'))['version']
    browsers = list((user / '.cache/hyperframes/chrome').glob('**/chrome-headless-shell.exe'))
    tools['chrome'] = {'status': 'file_found_not_launched' if browsers else 'missing',
                       'paths': [str(p) for p in browsers]}
    packages = {}
    for name in ['PIL', 'numpy', 'cv2', 'pytesseract', 'easyocr', 'paddleocr',
                 'faster_whisper', 'whisper', 'ultralytics', 'torch', 'onnxruntime', 'rapidocr_onnxruntime']:
        try:
            packages[name] = 'import_spec_found_not_end_to_end_tested' if importlib.util.find_spec(name) else 'missing'
        except (ImportError, ValueError, AttributeError):
            packages[name] = 'missing'
    filters = {name: False for name in ['sidechaincompress', 'loudnorm', 'alimiter', 'boxblur', 'crop', 'overlay']}
    if tools['ffmpeg']['status'] == 'verified_command':
        p = subprocess.run([tools['ffmpeg']['path'], '-hide_banner', '-filters'], capture_output=True, text=True, timeout=20)
        words = (p.stdout + p.stderr).split()
        filters = {name: name in words for name in filters}
    versions = {}
    for name in ['numpy','Pillow','faster-whisper','onnxruntime','rapidocr-onnxruntime','opencv-python-headless','opencv-python']:
        try: versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: pass
    return {'workspace': str(workspace), 'skills': found,
            'missing_requested_skills': [n for n in NAMES if not found[n]],
            'tools': tools, 'python_packages': packages,
            'package_versions': versions,
            'extra_python_path': str(extra) if extra.is_dir() else None, 'ffmpeg_filters': filters,
            'end_to_end_status': {'reference_analysis': 'per_job_required_not_certified_by_doctor',
                'speech_transcription_and_sentence_editing': 'unverified',
                'ocr_detection_tracking_and_redaction': 'unverified',
                'speech_ducking_and_preview_approval_workflow': 'unverified'},
            'note': 'Discovery is not model readiness or an end-to-end test. No tools/models installed; no video rendered.'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workspace', type=Path, default=Path.cwd())
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        ap.error('workspace must be an existing directory')
    payload = json.dumps(inventory(workspace), ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + '\n', encoding='utf-8')
    print(payload)

if __name__ == '__main__':
    main()
