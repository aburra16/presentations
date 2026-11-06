import json, io, copy
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches
from lxml import etree

S=json.load(open('states.json'))
SITE='../bitfest-2026/'
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
W,H=prs.slide_width,prs.slide_height
blank=prs.slide_layouts[6]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def jpg(path):
    path=path.replace('pptx/','')
    im=Image.open(path).convert('RGB'); b=io.BytesIO(); im.save(b,'JPEG',quality=92,optimize=True); b.seek(0); return b
def pic_id(pic): return int(pic._element.xpath('./p:nvPicPr/p:cNvPr')[0].get('id'))

def timing_xml(click_spids, video_spid):
    """main sequence: optional autoplay of video on entry, then one fade-in per click."""
    nid=[2]
    def n():
        nid[0]+=1; return str(nid[0])
    groups=[]
    if video_spid is not None:
        groups.append(f'''<p:par><p:cTn id="{n()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst><p:par><p:cTn id="{n()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{n()}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{n()}" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="{video_spid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>''')
    for spid in click_spids:
        groups.append(f'''<p:par><p:cTn id="{n()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{n()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{n()}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr><p:cTn id="{n()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{n()}" dur="350"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>''')
    if not groups: return None
    bld=''.join(f'<p:bldP spid="{s}" grpId="0"/>' for s in click_spids)
    xml=f'''<p:timing xmlns:p="{NS['p']}" xmlns:a="{NS['a']}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{''.join(groups)}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>{('<p:bldLst>'+bld+'</p:bldLst>') if bld else ''}</p:timing>'''
    return etree.fromstring(xml)

for sl in S['slides']:
    slide=prs.slides.add_slide(blank)
    files=sl['files']
    base=slide.shapes.add_picture(jpg(files[0]),0,0,W,H); base.name='state 0'
    video_spid=None
    if sl['video']:
        f=sl['frame']; sx=W/1600; sy=H/900
        poster=Image.open(files[0].replace('pptx/','')).convert('RGB'); pw,ph=poster.size; k=pw/1600
        crop=poster.crop((int(f['x']*k),int(f['y']*k),int((f['x']+f['w'])*k),int((f['y']+f['h'])*k))); pb=io.BytesIO(); crop.save(pb,'JPEG',quality=90); pb.seek(0)
        mv=slide.shapes.add_movie(SITE+sl['video'],Emu(int(f['x']*sx)),Emu(int(f['y']*sy)),Emu(int(f['w']*sx)),Emu(int(f['h']*sy)),poster_frame_image=pb,mime_type='video/mp4')
        mv.name='footage'; video_spid=int(mv._element.xpath('./p:nvPicPr/p:cNvPr')[0].get('id'))
        # python-pptx adds its own timing for the movie; drop it, we write ours
        for t in slide._element.xpath('./p:timing'): slide._element.remove(t)
    click=[]
    for k,fp in enumerate(files[1:],1):
        p=slide.shapes.add_picture(jpg(fp),0,0,W,H); p.name=f'state {k}'; click.append(pic_id(p))
    if sl['notes']:
        slide.notes_slide.notes_text_frame.text=sl['notes']
    t=timing_xml(click,video_spid)
    if t is not None: slide._element.append(t)
prs.save('bitfest-2026-backup.pptx')
import os; print('slides', os.path.getsize('bitfest-2026-backup.pptx')//1024,'KB')
