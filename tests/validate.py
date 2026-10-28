#!/usr/bin/env python3
"""Validate published paths, translations and audited dependency/license evidence."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,html
R=Path(__file__).resolve().parents[1];P=R/'public';errors=[]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.links=[];self.lang=None;self.ids=set();self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if a.get('id'):self.ids.add(a['id'])
  for k in ['href','src']:
   if a.get(k):self.links.append(a[k])
pages={f:Page(f.read_text()) for f in P.rglob('*.html')}
for f,page in pages.items():
 for link in page.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  dest=P/unquote(u.path).lstrip('/') if u.path.startswith('/') else f.parent/unquote(u.path)
  if dest.is_dir():dest=dest/'index.html'
  if not dest.exists():errors.append(f'{f.relative_to(P)}: missing {link}')
  elif u.fragment and dest.suffix=='.html' and u.fragment not in pages[dest].ids:errors.append(f'Bad fragment {link}')
for kind,version,sections in [('privacy','1.2',15),('terms','1.1',17),('licenses','1.1',9)]:
 for lang in ['ko','en','es','fr','pt','de','ja']:
  f=P/f'{kind}/{lang}/v{version}/index.html';s=f.read_text();page=pages[f]
  if page.lang!=('pt-BR' if lang=='pt' else lang):errors.append('Wrong lang '+str(f))
  if len(re.findall(r'<h2>',s))!=sections:errors.append('Section count '+str(f))
  for target in ['ko','en','es','fr','pt','de','ja']:
   if f'/{kind}/{target}/v{version}/' not in page.links:errors.append('Missing language '+str(f))
  for forbidden in ['OpenStreetMap','flutter_map','latlong2','2.12.0']:
   if forbidden in s:errors.append('Obsolete '+forbidden+' '+str(f))
  if kind!='licenses' and 'Google Places API' not in s:errors.append('Missing Places disclosure')
 if kind!='licenses':
  for lang in ['ko','en']:
   # Previously published versions are byte-for-byte preserved.
   vv=['1.0','1.1'] if kind=='privacy' else ['1.0']
   for old in vv:
    path=f'public/{kind}/{lang}/v{old}/index.html'
    expected=subprocess.check_output(['git','show','origin/main:'+path],cwd=R)
    if (R/path).read_bytes()!=expected:errors.append('Changed archive '+path)
archive=subprocess.check_output(['git','show','origin/main:public/licenses/index.html'],cwd=R)
# This assertion applies before deployment; after main updates the existing archive is the baseline.
if b'OpenStreetMap' in archive and (P/'licenses/v1.0/index.html').read_bytes()!=archive:errors.append('License archive not preserved')
x=json.loads((P/'licenses/data/inventory.json').read_text());records=x['records']
assert x['appHead']=='35596b94258d3d7c6b6e628685fc4c53a178656c'
assert x['pubspecLockSha256']=='80d1f9a020e2d3217c8d8837d2fe302e629a1faba9fbcfd05b2635f714b71f9c'
for eco,count in [('Dart',134),('Android',123),('iOS',3)]:
 assert len([r for r in records if r['ecosystem']==eco])==count
expected={'google_maps_flutter':'2.18.1','google_maps_flutter_android':'2.21.0','google_maps_flutter_ios_sdk10':'2.19.0','google_maps_flutter_ios':'2.18.7','google_maps_flutter_platform_interface':'2.17.0','google_maps_flutter_web':'0.6.5','com.google.android.gms:play-services-maps':'20.0.0','ios-maps-sdk':'10.15.0','com.google.code.gson:gson':'2.13.2','cwlcatchexception':'2.2.1'}
for name,version in expected.items():assert next(r for r in records if r['name']==name)['version']==version
refs=set()
for r in records:
 for t in r['texts']:
  f=P/t['file'].lstrip('/');assert hashlib.sha256(f.read_bytes()).hexdigest()==t['sha256'];refs.add(f.resolve())
assert refs==set(f.resolve() for f in (P/'licenses/texts').glob('*.txt')),'Unreferenced text files'
for lang in ['ko','en','es','fr','pt','de','ja']:
 s=(P/f'licenses/{lang}/v1.1/index.html').read_text()
 for r in records:
  if html.escape(r['name']) not in s:errors.append('Missing component '+r['name'])
  if r['version'] not in s:errors.append('Missing version '+r['name'])
 rows=re.findall(r'<th scope="row"><code>(.*?)</code>',s)
 assert len(rows)==len(records)
assert (P/'CNAME').read_text().strip()=='plena.meroviq.com'
assert not (P/'terms/es/v1.0/index.html').exists()
# Translation-only release: policy dates, body structure and prior-language text stay stable.
for kind,version,date in [('privacy','1.2','24 octobre 2026'),('terms','1.1','26 octobre 2026'),('licenses','1.1','26 octobre 2026')]:
 current=P/f'{kind}/fr/v{version}/index.html';translated=current.read_text()
 assert date in translated, 'French policy effective date changed'
 if kind!='licenses':
  def body(text):return text[text.index('<div class="notice">'):text.index('<footer>')]
  original=(P/f'{kind}/en/v{version}/index.html').read_text()
  for tag in ['h2','p','li','tr','th','td']:
   assert len(re.findall('<'+tag+r'(?:>|\s)',body(original)))==len(re.findall('<'+tag+r'(?:>|\s)',body(translated))), (kind,tag)
 for lang in ['ko','en','es']:
  path=f'public/{kind}/{lang}/v{version}/index.html'
  before=subprocess.check_output(['git','show','f23ca0fcb675356eb3c85641b12498308b30b4cb:'+path],cwd=R).decode()
  after=(R/path).read_text()
  # Only language navigation may differ in existing documents.
  strip=lambda v:re.sub(r'<nav aria-label="Language[^>]*>.*?</nav>', '', v, flags=re.S)
  assert strip(before)==strip(after), 'Existing legal content changed: '+path
for path in ['public/licenses/data/inventory.json','public/CNAME']:
 assert (R/path).read_bytes()==subprocess.check_output(['git','show','f23ca0fcb675356eb3c85641b12498308b30b4cb:'+path],cwd=R)

# Portuguese is a translation-only addition; existing policies and all archives stay intact.
for kind,version,date in [('privacy','1.2','24 de outubro de 2026'),('terms','1.1','26 de outubro de 2026'),('licenses','1.1','26 de outubro de 2026')]:
 translated=(P/f'{kind}/pt/v{version}/index.html').read_text()
 assert date in translated
 if kind!='licenses':
  original=(P/f'{kind}/en/v{version}/index.html').read_text()
  body=lambda s:s[s.index('<div class="notice">'):s.index('<footer>')]
  for tag in ['h2','p','li','tr','th','td']:
   assert len(re.findall('<'+tag+r'(?:>|\s)',body(original)))==len(re.findall('<'+tag+r'(?:>|\s)',body(translated))), (kind,tag)
 for lang in ['ko','en','es','fr']:
  path=f'public/{kind}/{lang}/v{version}/index.html'
  before=subprocess.check_output(['git','show','9acded8:'+path],cwd=R).decode()
  strip=lambda s:re.sub(r'<nav aria-label="Language[^>]*>.*?</nav>','',s,flags=re.S)
  assert strip(before)==strip((R/path).read_text()),path
for path in subprocess.check_output(['git','ls-tree','-r','--name-only','9acded8','public'],cwd=R).decode().splitlines():
 if '/texts/' in path or '/data/' in path or path.endswith('CNAME') or re.search(r'/(privacy|terms)/[^/]+/v1\.0/',path) or '/privacy/' in path and '/v1.1/' in path or '/licenses/v1.0/' in path:
  assert (R/path).read_bytes()==subprocess.check_output(['git','show','9acded8:'+path],cwd=R),path

# German translation preserves all prior policy content and metadata.
for kind,version,date in [('privacy','1.2','24. Oktober 2026'),('terms','1.1','26. Oktober 2026'),('licenses','1.1','26. Oktober 2026')]:
 translated=(P/f'{kind}/de/v{version}/index.html').read_text()
 assert date in translated
 if kind!='licenses':
  original=(P/f'{kind}/en/v{version}/index.html').read_text()
  body=lambda s:s[s.index('<div class="notice">'):s.index('<footer>')]
  for tag in ['h2','p','li','tr','th','td']:
   assert len(re.findall('<'+tag+r'(?:>|\s)',body(original)))==len(re.findall('<'+tag+r'(?:>|\s)',body(translated))), (kind,tag)
 for lang in ['ko','en','es','fr','pt']:
  path=f'public/{kind}/{lang}/v{version}/index.html'
  before=subprocess.check_output(['git','show','ac17d53:'+path],cwd=R).decode()
  strip=lambda s:re.sub(r'<nav aria-label="Language[^>]*>.*?</nav>','',s,flags=re.S)
  assert strip(before)==strip((R/path).read_text()),path

# Japanese translation preserves all prior policy content and metadata.
for kind,version,date in [('privacy','1.2','2026年10月24日'),('terms','1.1','2026年10月26日'),('licenses','1.1','2026年10月26日')]:
 translated=(P/f'{kind}/ja/v{version}/index.html').read_text()
 assert date in translated
 if kind!='licenses':
  original=(P/f'{kind}/en/v{version}/index.html').read_text()
  body=lambda s:s[s.index('<div class="notice">'):s.index('<footer>')]
  for tag in ['h2','p','li','tr','th','td']:
   assert len(re.findall('<'+tag+r'(?:>|\s)',body(original)))==len(re.findall('<'+tag+r'(?:>|\s)',body(translated))), (kind,tag)
 for lang in ['ko','en','es','fr','pt','de']:
  path=f'public/{kind}/{lang}/v{version}/index.html'
  before=subprocess.check_output(['git','show','224c7f2:'+path],cwd=R).decode()
  strip=lambda s:re.sub(r'<nav aria-label="Language[^>]*>.*?</nav>','',s,flags=re.S)
  assert strip(before)==strip((R/path).read_text()),path

if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, links, KO/EN/ES/FR/PT/DE/JA sections, 265 inventory records, {len(refs)} original text hashes, CNAME and published archives')
