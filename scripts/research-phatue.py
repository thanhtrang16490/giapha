import pathlib,json,urllib.request,concurrent.futures,hashlib
root=pathlib.Path(__file__).resolve().parent.parent
base='https://app.phatue.vn/assets/'
source=root/'tmp/phatue-public-assets.json'
assets=json.loads(source.read_text()) if source.exists() else [item['url'][len(base):] for item in json.loads((root/'reference/phatue/asset-manifest.json').read_text()) if item['url'].startswith(base)]
def download(asset):
 target=root/'reference/phatue'/asset;url=base+asset
 try:
  with urllib.request.urlopen(url,timeout=30) as response: data=response.read();mime=response.headers.get('Content-Type','')
  if 'text/html' in mime:raise ValueError('SPA fallback, not an asset')
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  return dict(path=str(target.relative_to(root)),url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),contentType=mime,status='downloaded',usage='reference-only',license='Not established by the public download')
 except Exception as e:return dict(url=url,status='unavailable',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor: results=list(executor.map(download,assets))
(root/'reference/phatue/asset-manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('Downloaded',sum(r['status']=='downloaded' for r in results),'of',len(results),'assets')
