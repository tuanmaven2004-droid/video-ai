"""Read-only analysis and non-overwriting job helpers. Python stdlib + FFmpeg/FFprobe.
Run --help; every report preserves pending human checks, never certifies privacy/listening.
"""
import argparse, json, hashlib, math, os, shutil, statistics, subprocess, sys
from pathlib import Path
from fractions import Fraction

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def save(p, obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2)

def tool(name, workspace):
    override=os.environ.get(name.upper())
    p=override or shutil.which(name)
    if p: return str(p)
    rel={'ffmpeg':'.hyperframes-tools/node_modules/ffmpeg-static/ffmpeg.exe',
         'ffprobe':'.hyperframes-tools/node_modules/ffprobe-static/bin/win32/x64/ffprobe.exe'}[name]
    p=Path(workspace)/rel
    if not p.is_file(): raise ValueError(f'{name} missing: use {name.upper()} environment variable')
    return str(p)

def run(args):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode: raise ValueError(f'Command failed ({p.returncode}): {p.stderr[-1800:]}')
    return p.stdout,p.stderr

def digest(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def probe(p,w):
    q=load_probe(p,w);v=next((s for s in q['streams'] if s['codec_type']=='video'),{})
    _,log=run([tool('ffmpeg',w),'-hide_banner','-t','12','-i',p,'-vf','vfrdet','-an','-f','null','-'])
    rotation=v.get('tags',{}).get('rotate',0)
    for s in v.get('side_data_list',[]): rotation=s.get('rotation',rotation)
    rotation=float(rotation);width=v.get('width',0);height=v.get('height',0)
    return {'path':str(Path(p).resolve()),'bytes':Path(p).stat().st_size,'sha256':digest(p),
            'probe':q,'display_size':[height,width] if round(rotation)%180 else [width,height],
            'duration':float(q['format'].get('duration',v.get('duration',0))),'rotation':rotation,'hdr_candidate':v.get('color_transfer') in ['smpte2084','arib-std-b67'],
            'vfr_sample_seconds':12,'vfr_log':[x for x in log.splitlines() if 'VFR:' in x],
            'vfr_full_file_verified':False,'quality_rank':'requires_visual_review'}

def load_probe(p,w):
    return json.loads(run([tool('ffprobe',w),'-v','error','-show_streams','-show_format','-of','json',p])[0])

def init_job(dst,property_id):
    root=Path(dst)
    if root.exists(): raise ValueError('Job directory already exists; choose a new job/revision')
    template=Path(__file__).resolve().parents[1]/'templates/job.json'
    pack=load(template)
    root.mkdir(parents=True)
    for name,obj in pack.items():
        obj.update(schema_version='1.0',property_id=property_id)
        save(root/name,obj)
    return {'job':str(root),'files':list(pack),'ready_to_render':False}

def validate(root):
    root=Path(root);names=list(load(Path(__file__).resolve().parents[1]/'templates/job.json'))
    data={n:load(root/n) for n in names};errors=[];pending=[]
    ids={x.get('property_id') for x in data.values()}
    if len(ids)!=1 or None in ids: errors.append('property_id must agree across all records')
    if any(x.get('schema_version')!='1.0' for x in data.values()): errors.append('schema_version must be 1.0')
    brief=data['brief.json'];plan=data['edit-plan.json'];manifest=data['source-manifest.json']
    sources={s['id']:s for s in manifest['sources']};sentences={s['id']:s for s in data['transcript.json']['sentences']}
    claims={c['id']:c for c in brief['claims']};licenses={s['id']:s for s in data['asset-ledger.json']['assets']}
    def interval(s,a='in',b='out'):
        return isinstance(s.get(a),(int,float)) and isinstance(s.get(b),(int,float)) and 0<=s[a]<s[b]
    for s in manifest['sources']:
        if not s.get('sha256') or not s.get('duration'): errors.append(f'missing hash/duration: {s["id"]}')
    for s in data['transcript.json']['sentences']:
        if not interval(s) or s.get('source_id') not in sources: errors.append(f'invalid sentence {s.get("id")}')
        if not s.get('listened') or not s.get('complete') or not s.get('reviewer') or not s.get('evidence'): pending.append(f'listen/confirm sentence {s.get("id")}')
    last=0
    if not plan.get('fps') or not plan.get('fps_reason'): pending.append('select fps with source/purpose rationale')
    for s in plan['visuals']:
        if not interval(s,'timeline_in','timeline_out') or abs(s['timeline_in']-last)>.04: errors.append(f'visual gap/overlap/invalid: {s.get("id")}')
        last=s.get('timeline_out',last)
        src=sources.get(s.get('source_id'))
        if not src: errors.append(f'unknown visual source {s.get("id")}');continue
        if not interval(s,'source_in','source_out') or s['source_out']>src['duration']+.04: errors.append(f'source bounds: {s.get("id")}')
        if src.get('property_id')!=brief['property_id'] and not (src.get('role')=='public_amenity' and src.get('relationship_verified')): errors.append(f'property mismatch: {s.get("id")}')
        if not s.get('relevance'): errors.append(f'B-roll/visual relevance missing: {s.get("id")}')
    if abs(last-plan['duration'])>.04: errors.append('visuals must cover duration')
    for s in plan['speech']:
        t=sentences.get(s.get('sentence_id'))
        if not t: errors.append('unknown sentence');continue
        if s.get('source_id')!=t['source_id'] or abs(s['source_in']-t['in'])>.001 or abs(s['source_out']-t['out'])>.001: errors.append(f'partial or different sentence: {s.get("sentence_id")}')
        if s['timeline_out']>plan['duration']+.001: errors.append('speech exceeds timeline')
        if not interval(s,'timeline_in','timeline_out') or abs((s['timeline_out']-s['timeline_in'])-(t['out']-t['in']))>.02: errors.append('speech time mapping must be 1:1')
        src=sources.get(t['source_id'],{})
        if t['out']>src.get('duration',0)+.04: errors.append('speech exceeds source')
    ordered=sorted(plan['speech'],key=lambda s:s['timeline_in'])
    if any(a['timeline_out']>b['timeline_in']+.001 for a,b in zip(ordered,ordered[1:])): errors.append('speech overlap')
    for g in plan['graphics']:
        if not interval(g,'timeline_in','timeline_out') or g['timeline_out']>plan['duration']+.001: errors.append('graphic interval')
        for cid in g.get('claim_ids',[]):
            c=claims.get(cid,{})
            if not c.get('confirmed') or not c.get('evidence'): errors.append(f'unconfirmed graphic claim: {cid}')
        if g.get('factual') and not g.get('claim_ids'): errors.append('factual graphic requires claim_ids')
    cues=data['cue-sheet.json']['cues']
    for c in cues:
        asset=licenses.get(c.get('asset_id'),{})
        if not 0<=c.get('at',-1)<plan['duration'] or not c.get('reason') or not c.get('visual_or_keyword'): errors.append(f'invalid cue {c.get("id")}')
        if not asset.get('permitted') or not asset.get('license_evidence') or not asset.get('source') or not asset.get('sha256'): errors.append(f'missing permitted asset evidence: {c.get("asset_id")}')
        if not c.get('listened_in_mix'): pending.append(f'audition cue {c.get("id")}')
    if any(sum(t<=c['at']<t+5 for c in cues)>3 for t in [c['at'] for c in cues]): pending.append('dense SFX: review >3 cues within 5 seconds')
    pr=data['privacy-review.json']
    if pr['status']!='reviewed' or not pr.get('reviewer') or not pr.get('artifact_sha256') or not pr.get('full_timeline_scanned'): pending.append('privacy full-timeline review pending')
    for x in pr['intervals']:
        if not x.get('all_frames_reviewed') or not x.get('encode_checked') or not x.get('reviewer'): pending.append(f'privacy interval {x.get("id")} unresolved')
        if x.get('status')=='verified' and (not x.get('all_frames_reviewed') or not x.get('encode_checked')): errors.append('privacy cannot be verified by detector/negative OCR alone')
    for k,v in data['qa-report.json']['manual'].items():
        if v.get('status')!='passed' or not v.get('evidence'): pending.append(f'manual {k} pending')
    if not sources or not plan['visuals'] or not plan['speech']: pending.append('job has no confirmed source/edit/speech yet')
    return {'errors':errors,'pending':sorted(set(pending)),'ready_to_deliver':not errors and not pending}

def compare(spec,out,w):
    spec=load(spec);out=Path(out)
    if out.exists(): raise ValueError('Comparison folder exists')
    out.mkdir(parents=True);rows=[]
    for i,pair in enumerate(spec['pairs']):
        for role in ['source','export']:
            p=pair[role];filters=[f'scale={spec["width"]}:{spec["height"]}:flags=lanczos']
            if pair.get('crop'): filters.append('crop='+':'.join(str(n) for n in pair['crop']))
            run([tool('ffmpeg',w),'-v','error','-ss',str(p['time']),'-i',p['path'],'-frames:v','1','-vf',','.join(filters),'-n',str(out/f'{i:02}-{role}.png')])
        rows.append(pair)
    save(out/'comparison.json',{'pairs':rows,'raster':[spec['width'],spec['height']],
         'status':'needs_visual_review','checks':['motion blur','fine detail','halos','noise','skin','color/HDR','crop/scale'],
         'warning':'Do not use PSNR/SSIM across different grades, crops, overlays, or unaligned motion.'})
    return {'pairs_written':len(rows),'review':'pending'}

def audio_report(p,w):
    _,log=run([tool('ffmpeg',w),'-hide_banner','-i',p,'-vn','-af','loudnorm=I=-16:TP=-1:LRA=7:print_format=json','-f','null','-'])
    start=log.rfind('{');end=log.rfind('}')
    return {'file':str(p),'measurement':json.loads(log[start:end+1]),'audition':'pending',
            'note':'input_i/input_tp are measured original values; output_* are hypothetical normalization, not applied.'}

def mix(spec,out,w):
    s=load(spec);args=[tool('ffmpeg',w),'-v','error'];labels=[]
    # Voice and background are pre-aligned full-timeline WAV stems. SFX are delayed individually.
    args+=['-i',s['voice']['path']];filters=['[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[voice][sc]'];labels=['[voice]']
    idx=1
    if s.get('music'):
        m=s['music'];assert m.get('permitted') and m.get('license_evidence'),'Music license evidence required'
        args+=['-i',m['path']]
        filters+=[f'[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={m.get("gain_db",-18)}dB[bed]',f'[bed][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[ducked]'];labels+=['[ducked]'];idx+=1
    else: filters+=['[sc]anullsink']
    for c in s.get('sfx',[]):
        assert c.get('permitted') and c.get('license_evidence'),'SFX license evidence required'
        assert c['at']>=0
        args+=['-i',c['path']];delay=round(c['at']*1000)
        filters+=[f'[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={c["gain_db"]}dB,adelay={delay}|{delay}[fx{idx}]'];labels+=[f'[fx{idx}]'];idx+=1
    filters+=[''.join(labels)+f'amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.891:latency=1,atrim=duration={s["duration"]}[mix]']
    args+=['-filter_complex',';'.join(filters),'-map','[mix]','-ar','48000','-c:a','pcm_s16le','-n',out]
    run(args);return audio_report(out,w)

def qa(p,w,expected):
    allowed={'width','height','fps','video_codec','audio_codec','duration'}
    if not expected or set(expected)-allowed: raise ValueError('expected must contain only target width/height/fps/video_codec/audio_codec/duration')
    q=load_probe(p,w);v=next(s for s in q['streams'] if s['codec_type']=='video');a=next((s for s in q['streams'] if s['codec_type']=='audio'),{})
    _,decode=run([tool('ffmpeg',w),'-v','error','-i',p,'-f','null','-'])
    _,log=run([tool('ffmpeg',w),'-hide_banner','-i',p,'-vf','blackdetect=d=0.1:pix_th=0.03,freezedetect=n=-50dB:d=1','-an','-f','null','-'])
    fps=float(Fraction(v['avg_frame_rate']));actual={'width':v['width'],'height':v['height'],'fps':fps,'video_codec':v['codec_name'],'audio_codec':a.get('codec_name'),'duration':float(q['format']['duration'])}
    mismatch={k:{'expected':val,'actual':actual.get(k)} for k,val in expected.items() if k!='duration' and actual.get(k)!=val}
    if 'duration' in expected and abs(actual['duration']-expected['duration'])>.1:mismatch['duration']=actual['duration']
    return {'sha256':digest(p),'file':str(Path(p).resolve()),'actual':actual,'mismatch':mismatch,'decode_errors':decode,
            'suspect_intervals':[x.strip() for x in log.splitlines() if 'black_start:' in x or 'freeze_' in x],
            'audio':audio_report(p,w) if a else {'error':'no audio stream'},
            'manual_pending':['listen to original speech and cuts','AV sync against source mapping','black/freeze intent','source/export detail comparison','phone typography and motion','privacy including transitions/encode'],
            'passed_technical':not mismatch and not decode,'ready_to_deliver':False}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--workspace',default=str(Path.cwd()))
    sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('init');p.add_argument('job');p.add_argument('--property-id',required=True)
    p=sub.add_parser('probe');p.add_argument('sources',nargs='+');p.add_argument('--out',required=True)
    p=sub.add_parser('validate');p.add_argument('job');p.add_argument('--out',required=True)
    p=sub.add_parser('compare');p.add_argument('spec');p.add_argument('--out',required=True)
    p=sub.add_parser('mix');p.add_argument('spec');p.add_argument('--audio-out',required=True);p.add_argument('--out',required=True)
    p=sub.add_parser('audio');p.add_argument('file');p.add_argument('--out',required=True)
    p=sub.add_parser('qa');p.add_argument('file');p.add_argument('--expected',required=True);p.add_argument('--out',required=True)
    a=ap.parse_args();c=a.command
    if c=='init':r=init_job(a.job,a.property_id)
    elif c=='probe':r={'schema_version':'1.0','sources':[dict(id=f's{i:03}',**probe(p,a.workspace)) for i,p in enumerate(a.sources)]}
    elif c=='validate':r=validate(a.job)
    elif c=='compare':r=compare(a.spec,a.out,a.workspace)
    elif c=='mix':r=mix(a.spec,a.audio_out,a.workspace)
    elif c=='audio':r=audio_report(a.file,a.workspace)
    else:r=qa(a.file,a.workspace,load(a.expected))
    if c not in ['init','compare']:save(a.out,r)
    print(json.dumps(r,ensure_ascii=False,indent=2))
    if c=='validate' and (r['errors'] or r['pending']):return 2
    if c=='qa' and (not r['passed_technical'] or r['suspect_intervals']):return 2
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,KeyError,AssertionError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
