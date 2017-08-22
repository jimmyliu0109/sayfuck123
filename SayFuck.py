#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import re
import json
import urllib2
 
from PlurkAPI import PlurkAPI
 
plurk = PlurkAPI('khAJMYUl812R', 'FQhBjxhszGESKiM0FaoTsVzFoDZOL1OA')
plurk.authorize('poWyWHtNnD92', 'Vg6HCEqy0XPCKW0WSNaVZRamUwoH0poa')
 
comet = plurk.callAPI('/APP/Realtime/getUserChannel')
comet_channel = comet.get('comet_server') + "&amp;new_offset=%d"
jsonp_re = re.compile('CometChannel.scriptCallback\((.+)\);\s*');
new_offset = -1
while True:
    plurk.callAPI('/APP/Alerts/addAllAsFriends')
    req = urllib2.urlopen(comet_channel % new_offset, timeout=80)
    rawdata = req.read()
    match = jsonp_re.match(rawdata)
    if match:
        rawdata = match.group(1)
    data = json.loads(rawdata)
    new_offset = data.get('new_offset', -1)
    msgs = data.get('data')
    if not msgs:
        continue
    for msg in msgs:
        if msg.get('type') == 'new_plurk':
            pid = msg.get('plurk_id')
            content = msg.get('content_raw')
            if content.find("罵人") != -1:
                plurk.callAPI('/APP/Responses/responseAdd',
                              {'plurk_id': pid,
                               'content': '直娘賊',
                               'qualifier': ':' })