import json, sys, urllib.request
import xml.etree.ElementTree as ET

FEEDS = {
    'if': 'channel_id=UCSK7Wg-KdLMJKnKltVT7Agg',
    'og': 'channel_id=UC8zkG_RahgwuSPBHLIBGnAA',
    'golf': 'channel_id=UCjx2WMa005Avcttt9Uam-3Q',
    'tws': 'channel_id=UCenLJNk7CNBMQhRczBYQb5Q',
    'sfh': 'playlist_id=PLihC6TAafKWcDbvIlAMc87HibcOlDYf8c',
    'ipwt': 'playlist_id=PLbMWADTq4QL4',
}
NS = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}

out = {}
for key, q in FEEDS.items():
    try:
        req = urllib.request.Request('https://www.youtube.com/feeds/videos.xml?' + q, headers={'User-Agent': 'Mozilla/5.0'})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
        eps = []
        for e in root.findall('a:entry', NS):
            link = e.find('a:link', NS)
            if link is not None and '/shorts/' in link.get('href', ''):
                continue
            eps.append({'id': e.find('yt:videoId', NS).text, 'title': e.find('a:title', NS).text, 'published': e.find('a:published', NS).text})
        if eps:
            eps.sort(key=lambda x: x['published'], reverse=True)
            out[key] = eps[0]
    except Exception as ex:
        print(key, 'failed:', ex)

with open(sys.argv[1], 'w') as f:
    json.dump(out, f)
print(json.dumps(out, indent=1))
