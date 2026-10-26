"""Small isolated functional tests; no property footage/render. FFmpeg required.
Pass a NEW --out directory for reports and <=3s synthetic media fixtures.
"""
import argparse,copy,json,math,sys,wave,struct
from pathlib import Path
from video_tools import init_job,load,save,validate,tool,run,probe,qa,mix,compare,digest
from map_component import build,xy
from mask_keyframes import apply as apply_mask,boxes_at

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--workspace',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out)
 if out.exists():raise ValueError('Use new test directory')
 out.mkdir(parents=True);passed=[];f=tool('ffmpeg',a.workspace)
 def ok(name,condition):
  if not condition:raise AssertionError(name)
  passed.append(name)
 def rejects(name,fn):
  try:fn()
  except (ValueError,AssertionError,FileExistsError):passed.append(name);return
  raise AssertionError(name)
 fixture=out/'test.mp4'
 run([f,'-v','error','-f','lavfi','-i','testsrc2=size=180x320:rate=30:duration=3','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest','-n',fixture])
 original_hash=digest(fixture);p=probe(fixture,a.workspace);save(out/'probe.json',p)
 ok('probe actual size fps audio duration hash',p['display_size']==[180,320] and p['duration']==3 and any(s['codec_type']=='audio' for s in p['probe']['streams']) and p['sha256']==original_hash)
 vf=out/'vfr.mp4';run([f,'-v','error','-i',fixture,'-vf',"select='if(lt(t,1),1,not(mod(n,2)))'",'-fps_mode','vfr','-an','-c:v','libx264','-n',vf])
 vp=probe(vf,a.workspace);save(out/'vfr-probe.json',vp);ok('VFR sample produces evidence, not full-file certification',bool(vp['vfr_log']) and not vp['vfr_full_file_verified'])
 job=out/'job';init_job(job,'TEST-ONLY');ok('empty job stays pending',not validate(job)['ready_to_deliver'])
 manifest=load(job/'source-manifest.json');manifest['sources']=[dict(id='s1',property_id='TEST-ONLY',role='house',duration=3,sha256=original_hash,path=str(fixture))]
 plan=load(job/'edit-plan.json');plan.update(duration=3,fps=30,fps_reason='synthetic source')
 plan['visuals']=[dict(id='v1',source_id='s1',source_in=0,source_out=3,timeline_in=0,timeline_out=3,relevance='fixture test')]
 plan['speech']=[dict(sentence_id='q1',source_id='s1',source_in=.2,source_out=2.8,timeline_in=.2,timeline_out=2.8)]
 tr=load(job/'transcript.json');tr['sentences']=[dict(id='q1',source_id='s1',**{'in':.2,'out':2.8},text='TEST tone, not real speech.',complete=True,listened=False)]
 def replace(name,obj): (job/name).write_text(json.dumps(obj),encoding='utf-8')
 replace('source-manifest.json',manifest);replace('edit-plan.json',plan);replace('transcript.json',tr)
 result=validate(job);ok('valid mapping accepted while audition remains pending',not result['errors'] and bool(result['pending']))
 bad=copy.deepcopy(plan);bad['speech'][0]['source_out']=2.4;replace('edit-plan.json',bad);ok('partial sentence rejected',bool(validate(job)['errors']));replace('edit-plan.json',plan)
 bad=copy.deepcopy(manifest);bad['sources'][0]['property_id']='OTHER-HOUSE';replace('source-manifest.json',bad);ok('wrong property rejected',bool(validate(job)['errors']));replace('source-manifest.json',manifest)
 bad=copy.deepcopy(plan);bad['graphics']=[dict(id='g1',factual=True,claim_ids=['price'],timeline_in=0,timeline_out=2)];replace('edit-plan.json',bad);ok('unconfirmed claim rejected',bool(validate(job)['errors']));replace('edit-plan.json',plan)
 pr=load(job/'privacy-review.json');pr['intervals']=[dict(id='p1',status='verified',all_frames_reviewed=False,encode_checked=False)];replace('privacy-review.json',pr);ok('negative OCR cannot clear privacy',bool(validate(job)['errors']))
 cues=load(job/'cue-sheet.json');cues['cues']=[dict(id='fx',asset_id='unlicensed',at=1,reason='test',visual_or_keyword='test')];replace('cue-sheet.json',cues);ok('missing asset rights rejected',bool(validate(job)['errors']))
 expected=dict(width=180,height=320,fps=30,video_codec='h264',audio_codec='aac',duration=3)
 q=qa(fixture,a.workspace,expected);save(out/'qa.json',q);ok('decode/codec/size/fps actual file',q['passed_technical'] and not q['ready_to_deliver'])
 black=out/'black.mp4';run([f,'-v','error','-f','lavfi','-i','color=black:size=180x320:rate=30:duration=2','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','2','-c:v','libx264','-c:a','aac','-n',black]);bq=qa(black,a.workspace,{**expected,'duration':2});save(out/'qa-black.json',bq);ok('black/freeze fixture flagged',bool(bq['suspect_intervals']))
 spec=out/'compare-spec.json';save(spec,dict(width=180,height=320,pairs=[dict(source=dict(path=str(fixture),time=.5),export=dict(path=str(fixture),time=.5))]));compare(spec,out/'comparison',a.workspace)
 ok('aligned same-frame comparison produces identical PNG',digest(out/'comparison/00-source.png')==digest(out/'comparison/00-export.png'))
 rejects('comparison refuses overwrite',lambda:compare(spec,out/'comparison',a.workspace))
 # Full-timeline voice envelope with a silent gap. Tones are test signals, NOT music assets.
 sr=48000
 def wav(path,fn):
  with wave.open(str(path),'wb') as w:
   w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<hh',int(fn(i/sr)*32767),int(fn(i/sr)*32767)) for i in range(sr*3)))
 voice=out/'voice.wav';bed=out/'bed.wav';wav(voice,lambda t:.2*math.sin(2*math.pi*800*t) if .2<t<1.4 else 0);wav(bed,lambda t:.15*math.sin(2*math.pi*160*t))
 ms=out/'mix.json';save(ms,dict(duration=3,voice=dict(path=str(voice)),music=dict(path=str(bed),permitted=True,license_evidence='own synthetic test signal',gain_db=0),sfx=[]));mr=mix(ms,out/'mix.wav',a.workspace);save(out/'mix-report.json',mr)
 # Compare background-band amplitude in voiced interval vs settled silence, without numpy.
 with wave.open(str(out/'mix.wav'),'rb') as w:raw=w.readframes(w.getnframes());vals=struct.unpack('<'+'h'*(len(raw)//2),raw)[::2]
 def band(t):
  n=round(.2*sr);start=round(t*sr)
  return abs(sum(vals[start+i]*complex(math.cos(-2*math.pi*160*i/sr),math.sin(-2*math.pi*160*i/sr)) for i in range(n)))/n
 ratio=band(.8)/band(2.6);ok('sidechain reduces bed during voice',ratio<.7);save(out/'duck-test.json',dict(active_to_idle_background_amplitude_ratio=ratio,listened=False))
 png=out/'map-fixture.png';run([f,'-v','error','-f','lavfi','-i','testsrc2=size=180x320:duration=1','-frames:v','1','-n',png])
 m=dict(publication_confirmed=True,location_evidence='synthetic test coordinates, no property',precision='approximate',projection='EPSG:3857',north_up=True,bounds=[0,0,2,2],zoom=1.5,asset=dict(path=str(png),source='generated calibration fixture',license_evidence='own test pattern',attribution='TEST MAP — NOT A PROPERTY',video_use_permitted=True),pin=dict(lat=1,lon=1,label='TEST PIN',confirmed=True,evidence='synthetic'),landmarks=[dict(lat=1.3,lon=1.2,label='TEST POI',confirmed=True,evidence='synthetic')],routes=[dict(coordinates=[[1,1],[1.1,1.1],[1.3,1.2]],confirmed=True,evidence='synthetic route')])
 mp=out/'map-spec.json';save(mp,m);build(mp,out/'map');ok('projection known central longitude',abs(xy(1,1,[0,0,2,2])[0]-540)<.001)
 for name,changes in [('unconfirmed location',{'publication_confirmed':False}),('exact without authorization',{'precision':'exact'}),('private coordinates',{'private_pin':[1,1]}),('wrong projection',{'projection':'EPSG:4326'})]:
  bad={**m,**changes};spec2=out/(name.replace(' ','-')+'.json');save(spec2,bad);rejects('map rejects '+name,lambda:build(spec2,out/('bad-'+name)))
 bad=copy.deepcopy(m);bad['asset']['license_evidence']=None;spec2=out/'missing-license.json';save(spec2,bad);rejects('map rejects missing license',lambda:build(spec2,out/'bad-license'))
 mask_spec=out/'mask-spec.json';mask_out=out/'masked.mkv'
 save(mask_spec,dict(source=str(fixture),coordinate_space='autorotated_display_pixels',display_size=[180,320],fps='30/1',cfr_verified=True,intervals=[{'in':0,'out':2.9,'padding':0,'keyframes':[{'t':0,'bbox':[10,20,30,20]},{'t':2.9,'bbox':[60,20,30,20]}]}]))
 mask_report=apply_mask(mask_spec,mask_out,a.workspace)
 ok('manual keyframe masks preserve frame count and report pending',mask_report['frames']==90 and 'needs_all_frame_review' in mask_report['privacy_status'])
 raw=__import__('subprocess').check_output([f,'-v','error','-ss','1','-i',str(mask_out),'-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'])
 box=boxes_at(load(mask_spec),1,180,320)[0];x0,y0,x1,y1=box
 ok('moving opaque mask covers expected interpolated pixels',all(raw[(y*180+x)*3:(y*180+x)*3+3]==b'\0\0\0' for y in range(y0,y1) for x in range(x0,x1)))
 rejects('mask refuses overwrite',lambda:apply_mask(mask_spec,mask_out,a.workspace))
 ok('source fixture unchanged',digest(fixture)==original_hash)
 save(out/'tests.json',dict(passed=passed,count=len(passed),full_property_render=False,audition=False,map_is_synthetic=True));print(json.dumps({'passed':len(passed),'report':str(out/'tests.json')}))

if __name__=='__main__':main()
