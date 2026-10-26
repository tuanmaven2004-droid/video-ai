"""Apply opaque privacy masks from manually verified keyframes to a NEW FFV1 MKV.
No automatic OCR/detection/tracking. Linear interpolation only inside a shot.
Coordinates refer to decoded autorotated display pixels, full input duration.
"""
import argparse,bisect,json,subprocess,sys
from pathlib import Path
from fractions import Fraction
from video_tools import load,save,tool,load_probe,digest

def boxes_at(spec,t,w,h):
    boxes=[]
    for r in spec['intervals']:
        if not r['in']<=t<=r['out']:continue
        keys=r['keyframes'];times=[k['t'] for k in keys]
        if times!=sorted(set(times)) or times[0]>r['in'] or times[-1]<r['out']:raise ValueError('Keys must cover interval and be strictly sorted')
        j=min(max(1,bisect.bisect_right(times,t)),len(keys)-1)
        if len(keys)<2:raise ValueError('Need >=2 keyframes, including interval boundaries')
        a,b=keys[j-1],keys[j];p=max(0,min(1,(t-a['t'])/(b['t']-a['t'])))
        x,y,bw,bh=[a['bbox'][i]+p*(b['bbox'][i]-a['bbox'][i]) for i in range(4)];pad=r.get('padding',12)
        if bw<=0 or bh<=0:raise ValueError('Invalid mask dimensions')
        boxes.append((max(0,int(x-pad)),max(0,int(y-pad)),min(w,int(x+bw+pad+1)),min(h,int(y+bh+pad+1))))
    return boxes

def apply(specpath,out,wspace):
    s=load(specpath);src=Path(s['source']).resolve();out=Path(out).resolve()
    if out==src or out.exists() or out.suffix.lower()!='.mkv':raise ValueError('Choose NEW .mkv output distinct from source')
    if s.get('coordinate_space')!='autorotated_display_pixels' or not s.get('cfr_verified'):raise ValueError('Verify display coordinates and CFR; VFR requires a timestamp-aware adapter')
    w,h=s['display_size'];fps=float(Fraction(s['fps']));q=load_probe(src,wspace);v=next(x for x in q['streams'] if x['codec_type']=='video')
    rotation=float(v.get('tags',{}).get('rotate',0))
    for side in v.get('side_data_list',[]):rotation=float(side.get('rotation',rotation))
    actual=[v['height'],v['width']] if round(rotation)%180 else [v['width'],v['height']]
    if [w,h]!=actual:raise ValueError('Display size does not match autorotated source')
    if v.get('color_transfer') in ['smpte2084','arib-std-b67']:raise ValueError('HDR requires a color-preserving mask adapter; not this RGB helper')
    if abs(float(Fraction(v['avg_frame_rate']))-fps)>.01:raise ValueError('fps does not match source')
    duration=float(q['format']['duration'])
    if not s['intervals']:raise ValueError('No masks supplied')
    for r in s['intervals']:
        if not 0<=r['in']<r['out']<=duration+.01:raise ValueError('Mask interval outside source')
        boxes_at(s,r['in'],w,h);boxes_at(s,r['out'],w,h)
    f=tool('ffmpeg',wspace);out.parent.mkdir(parents=True,exist_ok=True)
    before=digest(src)
    dec=subprocess.Popen([f,'-v','error','-i',str(src),'-an','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc=subprocess.Popen([f,'-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(s['fps']),'-i','-','-i',str(src),'-map','0:v:0','-map','1:a?','-c:v','ffv1','-level','3','-c:a','copy','-map_metadata','-1','-n',str(out)],stdin=subprocess.PIPE)
    n=0;masked=0
    try:
        while True:
            raw=dec.stdout.read(w*h*3)
            if not raw:break
            if len(raw)!=w*h*3:raise ValueError('Short decoded frame: check display size/rotation')
            im=bytearray(raw);boxes=boxes_at(s,n/fps,w,h)
            for x0,y0,x1,y1 in boxes:
                if x1<=x0 or y1<=y0:raise ValueError('Mask outside image')
                strip=b'\0'*((x1-x0)*3)
                for y in range(y0,y1):im[(y*w+x0)*3:(y*w+x1)*3]=strip
            if boxes:masked+=1
            enc.stdin.write(im);n+=1
        enc.stdin.close()
        if enc.wait()!=0 or dec.wait()!=0:raise ValueError('Mask encode/decode failed; partial file requires review')
    finally:
        for proc in [dec,enc]:
            if proc.poll() is None:proc.kill();proc.wait()
    if n!=round(float(v['duration'])*fps):raise ValueError('Frame count differs from expected; inspect VFR/rotation')
    if digest(src)!=before:raise ValueError('Source hash changed')
    report={'source_sha256':before,'output_sha256':digest(out),'frames':n,'masked_frames':masked,'method':'opaque mask; manual-keyframe linear interpolation','privacy_status':'mask_applied_needs_all_frame_review','reviewer':None,'audio':'copied unchanged; disclosure review pending'}
    save(str(out)+'.mask-report.json',report);return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('spec');ap.add_argument('--out',required=True);ap.add_argument('--workspace',default=str(Path.cwd()));a=ap.parse_args()
    try:print(json.dumps(apply(a.spec,a.out,a.workspace),indent=2))
    except (ValueError,KeyError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
