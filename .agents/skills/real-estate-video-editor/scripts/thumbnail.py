from pathlib import Path
import argparse,sys
try:
 from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter,ImageOps
except ImportError as exc:
 raise SystemExit("Thumbnail helper requires Pillow; check the project runtime. It will not install dependencies automatically.") from exc

def load_font(path,size):
 return ImageFont.truetype(str(path),size)

def fit(draw,text,path,max_size,min_size,max_width,stroke=0):
 for size in range(max_size,min_size-1,-2):
  font=load_font(path,size);box=draw.textbbox((0,0),text,font=font,stroke_width=stroke)
  if box[2]-box[0]<=max_width:return font
 raise ValueError(f'Text does not fit safely: {text!r}')

def main():
 ap=argparse.ArgumentParser(description='Create a real-estate thumbnail from an existing property still; never invent architecture or facts.')
 ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--tag',required=True);ap.add_argument('--location',required=True);ap.add_argument('--price',required=True);ap.add_argument('--details',default='');ap.add_argument('--width',type=int,default=1080);ap.add_argument('--height',type=int,default=1440);ap.add_argument('--crop-x',type=float,default=.5);ap.add_argument('--crop-y',type=float,default=.5);ap.add_argument('--font');ap.add_argument('--brightness',type=float,default=1.04);a=ap.parse_args()
 src=Path(a.source);out=Path(a.output)
 if not src.is_file():raise SystemExit(f'Source image not found: {src}')
 if out.exists():raise SystemExit(f'Refusing to overwrite: {out}')
 if a.width<640 or a.height<640:raise SystemExit('Canvas must be at least 640px on both sides')
 if not 0<=a.crop_x<=1 or not 0<=a.crop_y<=1:raise SystemExit('Crop anchors must be between 0 and 1')
 root=Path(__file__).resolve().parent.parent;fontpath=Path(a.font) if a.font else root/'assets/Anton-Regular.ttf'
 if not fontpath.is_file():raise SystemExit(f'Licensed Vietnamese font not found: {fontpath}')
 with Image.open(src) as im:
  im=ImageOps.exif_transpose(im).convert('RGB');sw,sh=im.size
  scale=max(a.width/sw,a.height/sh);nw,nh=round(sw*scale),round(sh*scale);im=im.resize((nw,nh),Image.Resampling.LANCZOS)
  left=round((nw-a.width)*a.crop_x);top=round((nh-a.height)*a.crop_y);im=im.crop((left,top,left+a.width,top+a.height))
 im=ImageEnhance.Brightness(im).enhance(a.brightness);im=ImageEnhance.Contrast(im).enhance(1.035);im=ImageEnhance.Color(im).enhance(1.04);im=ImageEnhance.Sharpness(im).enhance(1.06)
 w,h=im.size;overlay=Image.new('RGBA',(w,h),(0,0,0,0));pix=overlay.load();grad_start=int(h*.66)
 for y in range(grad_start,h):
  t=(y-grad_start)/(h-grad_start);alpha=round(8+210*(t**1.3))
  for x in range(w):pix[x,y]=(5,9,14,alpha)
 im=Image.alpha_composite(im.convert('RGBA'),overlay);d=ImageDraw.Draw(im)
 margin=round(w*.045);tag=a.tag.strip().upper();location=a.location.strip().upper();price=a.price.strip().upper()
 tag_font=fit(d,tag,fontpath,58,34,w-2*margin-54,1);tag_box=d.textbbox((0,0),tag,font=tag_font,stroke_width=1);tag_w=tag_box[2]-tag_box[0]+54;tag_h=tag_box[3]-tag_box[1]+24;tag_y=round(h*.625);tag_rect=(margin,tag_y,margin+tag_w,tag_y+tag_h)
 glow=Image.new('RGBA',(w,h),(0,0,0,0));gd=ImageDraw.Draw(glow);gd.rounded_rectangle(tag_rect,radius=tag_h//2,outline=(255,215,0,180),width=12);glow=glow.filter(ImageFilter.GaussianBlur(13));im=Image.alpha_composite(im,glow);d=ImageDraw.Draw(im);d.rounded_rectangle(tag_rect,radius=tag_h//2,fill=(5,7,10,244),outline=(255,222,0,255),width=5)
 d.text((margin+27,tag_y+tag_h//2),tag,font=tag_font,fill=(255,224,0,255),anchor='lm',stroke_width=1,stroke_fill=(0,0,0,255))
 # Keep location and price together like the supplied thumbnail reference.
 max_main=w-2*margin;main_font=None;sep='  |  '
 for size in range(100,59,-2):
  candidate=load_font(fontpath,size)
  width=d.textlength(location,font=candidate)+d.textlength(sep,font=candidate)+d.textlength(price,font=candidate)
  if width<=max_main:main_font=candidate;break
 if main_font is None:raise ValueError('Location + price do not fit on one main line; shorten text or widen canvas.')
 main_y=round(h*.775);loc_width=d.textlength(location,font=main_font);sep_width=d.textlength(sep,font=main_font)
 shadow=Image.new('RGBA',(w,h),(0,0,0,0));sd=ImageDraw.Draw(shadow);sd.text((margin+3,main_y+7),location+sep+price,font=main_font,fill=(0,0,0,220),anchor='lm',stroke_width=12,stroke_fill=(0,0,0,240));shadow=shadow.filter(ImageFilter.GaussianBlur(8));im=Image.alpha_composite(im,shadow);d=ImageDraw.Draw(im)
 d.text((margin,main_y),location,font=main_font,fill=(255,255,255,255),anchor='lm',stroke_width=6,stroke_fill=(5,7,10,255))
 sep_x=margin+loc_width;d.text((sep_x,main_y),sep,font=main_font,fill=(255,220,0,255),anchor='lm',stroke_width=6,stroke_fill=(5,7,10,255))
 price_x=sep_x+sep_width;d.text((price_x,main_y),price,font=main_font,fill=(255,220,0,255),anchor='lm',stroke_width=6,stroke_fill=(5,7,10,255))
 details=a.details.strip().upper()
 if details:
  detail_font=fit(d,details,fontpath,68,40,max_main,4);detail_y=round(h*.875)
  d.text((margin,detail_y),details,font=detail_font,fill=(255,255,255,255),anchor='lm',stroke_width=5,stroke_fill=(5,7,10,255))
 out.parent.mkdir(parents=True,exist_ok=True);im.convert('RGB').save(out,format='PNG',optimize=True)
 print(f'created={out} size={a.width}x{a.height} source={sw}x{sh} source={src}')
if __name__=='__main__':main()



