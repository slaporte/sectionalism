import wapiti
import re
import bottle
from bottle import route, run, JSONPlugin
from functools import partial
from datetime import datetime, timedelta


def section_stats(title, limit=80000):
    revs = wapiti.get_revision_texts(page_title=title, limit=limit)
    section_header = re.compile(r'((^[\=]+).*?\2)', flags=re.MULTILINE)
    stats = []
    for i, rev in enumerate(revs):
        sections = re.split(section_header, rev.content)
        rev_stats = []
        cur_section = 'Intro'
        depth = 1
        for sec in sections:
            if len(sec.strip('=')) > 0:
                if sec.startswith('='):
                    depth = sec.count('=') / 2
                    cur_section = sec.strip('=')
                else:
                    length = len(sec)
                    if i > 0:
                        prev = [r['length'] for r in stats[i - 1]['sections'] \
                                if r['name'] == cur_section]
                        if prev:
                            diff = length - prev[0]
                        else:
                            diff = length
                    else:
                        diff = length
                    rev_stats.append({'name': cur_section,
                                      'depth': depth,
                                      'length': length,
                                      'length_diff': diff})
        if i > 0:
            time_delta = rev.time - datetime.strptime(stats[i - 1]['time'], \
                                                     '%Y-%m-%d %H:%M:%S')
        else:
            time_delta = timedelta(0)
        stats.append({'page_title': rev.page_title,
                    'page_id': rev.page_id,
                    'rev_id': rev.rev_id,
                    'rev_parent_id': rev.rev_parent_id,
                    'user_text': rev.user_text,
                    'user_id': rev.user_id,
                    'time': str(rev.time),
                    'time_delta': time_delta.total_seconds(),
                    'length': rev.length,
                    'sha1': rev.sha1,
                    'comment': rev.comment,
                    'tags': rev.tags,
                    'sections': rev_stats})
    return {'title': title, 'revisions': stats, 'total_revs': len(revs)}


@route('/<title>')
def get_sec_stats(title):
    return section_stats(title)


if __name__ == '__main__':
    better_dumps = partial(bottle.json_dumps, indent=2,
                            sort_keys=True, default=repr)
    bottle.debug(True)
    bottle.install(JSONPlugin(better_dumps))
    run(port=8080)
