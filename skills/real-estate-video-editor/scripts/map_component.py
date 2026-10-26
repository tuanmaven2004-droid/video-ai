"""Build an offline, seekable location SVG component from licensed map artwork.
No geocoding/tile fetching. Input ONLY coordinates approved for publication.
Background: north-up, unrotated EPSG:3857 raster with exact geographic bounds.
"""
import argparse,base64,html,json,math,mimetypes,sys
from pathlib import Path
from video_tools import load,save,digest

def xy(lat,lon,bounds,w=1080,h=1920):
    west,south,east,north=bounds
    if not (-180<=west<east<=180 and -85<south<north<85):raise ValueError('Invalid or dateline-crossing bounds')
    if not (south<=lat<=north and west<=lon<=east):raise ValueError('Point outside basemap')
    def merc(y):return math.log(math.tan(math.pi/4+math.radians(y)/2))
    return ((lon-west)/(east-west)*w,(merc(north)-merc(lat))/(merc(north)-merc(south))*h)

def build(spec,out):
    s=load(spec);out=Path(out)
    if out.exists():raise ValueError('Output exists')
    if not s.get('publication_confirmed') or not s.get('location_evidence'):raise ValueError('Confirmed public location/evidence required')
    if s.get('precision') not in ['approximate','exact']:raise ValueError('Choose approved public precision')
    if s['precision']=='exact' and not s.get('exact_publication_authorized'):raise ValueError('Exact publication requires authorization')
    if s.get('projection')!='EPSG:3857' or not s.get('north_up'):raise ValueError('Only north-up Web Mercator artwork supported')
    a=s['asset']
    if not all(a.get(k) for k in ['source','license_evidence','attribution','video_use_permitted']):raise ValueError('Licensed background and attribution required')
    p=Path(a['path']);mime=mimetypes.guess_type(p)[0]
    if mime not in ['image/png','image/jpeg','image/webp']:raise ValueError('Use local raster; SVG/network assets not accepted')
    bg='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
    points=[s['pin']]+s.get('landmarks',[]);positions=[]
    for v in points:
        if not v.get('confirmed') or not v.get('evidence'):raise ValueError('Unconfirmed pin/landmark')
        positions.append(xy(v['lat'],v['lon'],s['bounds']))
    px,py=positions[0];zoom=float(s.get('zoom',1.8))
    if not 1<=zoom<=4:raise ValueError('Zoom must be 1..4; review readability at chosen asset resolution')
    items=[]
    for i,(v,(x,y)) in enumerate(zip(points,positions)):
        items.append(f'<g class="point" data-index="{i}"><circle cx="{x:.3f}" cy="{y:.3f}" r="{20 if i==0 else 12}" fill="#ffca45" stroke="#102029" stroke-width="5"/><text x="{x+28:.3f}" y="{y:.3f}" fill="white" stroke="#102029" stroke-width="3" paint-order="stroke" font-size="42">{html.escape(v["label"])}</text></g>')
    routes=[]
    for r in s.get('routes',[]):
        if not r.get('confirmed') or not r.get('evidence'):raise ValueError('Route geometry must be verified, not a guessed straight line')
        path=' '.join(('M' if i==0 else 'L')+f'{x:.3f},{y:.3f}' for i,(x,y) in enumerate(xy(lat,lon,s['bounds']) for lat,lon in r['coordinates']))
        routes.append(f'<path class="route" d="{path}" fill="none" stroke="#ffca45" stroke-width="8"/>')
    # Public coordinates become pixels; private coordinates are neither accepted nor emitted.
    if any(k in s for k in ['private_coordinates','private_pin']):raise ValueError('Keep private coordinates outside public component input')
    attribution=html.escape(a['attribution']);precision='VỊ TRÍ GẦN ĐÚNG' if s['precision']=='approximate' else 'VỊ TRÍ ĐÃ XÁC NHẬN'
    doc='''<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#102029}svg{width:1080px;height:1920px;font-family:sans-serif}.point,.route{opacity:0}</style><svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><g id="camera"><image width="1080" height="1920" preserveAspectRatio="none" href="BG"/>ROUTES POINTS</g><rect x="0" y="0" width="1080" height="110" fill="#102029"/><text x="540" y="72" text-anchor="middle" fill="white" font-size="44">PRECISION</text><rect x="0" y="1700" width="1080" height="220" fill="#102029"/><foreignObject x="70" y="1720" width="850" height="180"><div xmlns="http://www.w3.org/1999/xhtml" style="color:white;font:32px/1.3 sans-serif">ATTR</div></foreignObject></svg><script>
const ZOOM=ZOOM_VALUE,PX=PIN_X,PY=PIN_Y;
window.mapSeek=function(t){const p=Math.max(0,Math.min(1,(t-.6)/1.2));const e=p*p*(3-2*p);const z=1+(ZOOM-1)*e;document.getElementById('camera').setAttribute('transform',`translate(${(540-PX)*e} ${(960-PY)*e}) translate(${PX} ${PY}) scale(${z}) translate(${-PX} ${-PY})`);document.querySelectorAll('.point').forEach((v,i)=>v.style.opacity=Math.max(0,Math.min(1,(t-1.8-i*.3)/.25)));document.querySelectorAll('.route').forEach(v=>{let l=v.getTotalLength();v.style.opacity=t>=2.6?1:0;v.style.strokeDasharray=l;v.style.strokeDashoffset=l*(1-Math.max(0,Math.min(1,(t-2.6)/1.2)));});};window.mapSeek(0);
</script>'''
    # Single replacement pass prevents marker-looking labels/assets being evaluated as code.
    import re
    values={'BG':bg,'ROUTES':''.join(routes),'POINTS':''.join(items),'PRECISION':precision,'ATTR':attribution,'ZOOM_VALUE':str(zoom),'PIN_X':str(px),'PIN_Y':str(py)}
    doc=re.sub(r'\b(BG|ROUTES|POINTS|PRECISION|ATTR|ZOOM_VALUE|PIN_X|PIN_Y)\b',lambda m:values[m[0]],doc)
    out.mkdir(parents=True);(out/'map.html').write_text(doc,encoding='utf-8')
    save(out/'provenance.json',{'source':a['source'],'license_evidence':a['license_evidence'],'attribution':a['attribution'],'asset_sha256':digest(p),'precision':s['precision'],'publication_confirmed':True,'listening':'not_applicable','visual_review':'pending; attribution, label clipping and precision need final-frame review','duration_recommendation':5})
    return {'output':str(out),'status':'built_not_certified','projection':'EPSG:3857'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('spec');ap.add_argument('--out',required=True);a=ap.parse_args()
    try: print(json.dumps(build(a.spec,a.out)))
    except (ValueError,KeyError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
