#!/usr/bin/env python
import wapiti
import re
import bottle
from bottle import route, run, request
from flup.server.fcgi import WSGIServer


def section_stats(title, limit=80000):
    revs = wapiti.get_revision_texts(page_title=title, limit=limit)
    section_header = re.compile(r'((^[\=]+).*?\2)', flags=re.MULTILINE)  # does not check matching
    stats = []
    depth = 1
    for i, rev in enumerate(revs):
        sections = re.split(section_header, rev.content)
        rev_stats = []
        cur_section = 'Intro'
        depth = 0
        for sec in sections:
            if len(sec.strip('=')) > 0:
                if sec.startswith('='):
                    depth = sec.count('=') / 2
                    cur_section = sec.strip('=')
                else:
                    length = len(sec)
                    if i > 0:
                        prev_len = [r['length'] for r in stats[i - 1].sections
                        if r['name'] == cur_section]
                        if prev_len:
                            diff = length - prev_len[0]
                        else:
                            diff = length
                    else:
                        diff = length
                    rev_stats.append({'name': cur_section,
                                      'depth': depth,
                                      'length': length,
                                      'diff': diff})
        stats.append({'page_title': rev.page_title,
                    'page_id': rev.page_id,
                    'rev_id': rev.rev_id,
                    'rev_parent_id': rev.rev_parent_id,
                    'user_text': rev.user_text,
                    'user_id': rev.user_id,
                    'time': rev.time,
                    'length': rev.length,
                    'sha1': rev.sha1,
                    'comment': rev.comment,
                    'tags': rev.tags,
                    'sections': rev_stats})
    return stats


@route('/section/<title>')
def get_sec_stats(title):
    return section_stats(title)

@route('/test')
def test():
    return 'hello'

app = bottle.default_app()
if __name__ == '__main__':
    WSGIServer(app).run()
