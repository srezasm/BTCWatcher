from time import gmtime, strftime
from globaldic import *


# returns current time with feed format
def get_current_time():
    # https://datatracker.ietf.org/doc/html/rfc2822
    return strftime('%a, %d %b %Y %X GMT', gmtime())


# prevents possible errors if the called entry doesn't exist
def get_entry(item, enty_name: str, is_list=False):
    return item[enty_name] if hasattr(item, enty_name) else ([] if is_list else '')


def fetch_new_items(name, items: list):
    with open(filedic['ids']) as fr:
        oldlines = fr.read().splitlines()
        oldids = []
        newlines = oldlines.copy()

        isn = False
        for ol in oldlines:
            if ol.startswith(name):
                isn = True

        if not isn:
            ii = []
            for i in items:
                ii.append(i.id)

            newlines.append(name + '::' + '::'.join(ii))
            with open(filedic['ids'], 'w') as fw:
                fw.write('\n'.join(newlines))
            return items

        # fill the old_ids with current feed ids
        for ol in oldlines:
            if ol.startswith(name):
                oldids.extend(ol.split('::'))
                oldids.pop(0)

        # fill new_items
        newitems = items.copy()
        for id in oldids:
            for it in items:
                if id == it.id:
                    newitems.remove(it)

        # fill new_ids
        newids = []
        for ni in newitems:
            newids.append(ni.id)

        # fill new_lines
        for i in range(len(newlines)):
            nl = newlines[i]

            if nl.startswith(name):
                newlines[i] = nl + '::' + '::'.join(newids)

        # write new_lines into ids.text
        with open(filedic['ids'], 'w') as fw:
            fw.write('\n'.join(newlines))

        return newitems


def write_etag(name, etag):
    with open(filedic['etags']) as fr:
        lines = fr.read().splitlines()

        for ni in len(lines):
            if lines[ni].startswith(name):
                lines[ni] = 'name' + '::' + 'etag'

        fw = open(filedic['etags'], 'w')
        fw.write('\n'.join(lines))
        fw.close()


def get_etag(name):
    with open(filedic['etags']) as fr:
        lines = fr.read().splitlines()

        if name not in fr.read():
            return ''

        else:
            for l in lines:
                if l.startswith(name):
                    return l.split('::')[1]


def write_modified(name, modified):
    with open(filedic['modifieds']) as fr:
        lines = fr.read().splitlines()

        for ni in len(lines):
            if lines[ni].startswith(name):
                lines[ni] = 'name' + '::' + 'modified'

        fw = open(filedic['modifieds'], 'w')
        fw.write('\n'.join(lines))
        fw.close()


def get_modified(name):
    with open(filedic['modifieds']) as fr:
        lines = fr.read().splitlines()

        if name not in fr.read():
            return ''

        else:
            for l in lines:
                if l.startswith(name):
                    return l.split('::')[1]
