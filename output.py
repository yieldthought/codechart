# Copyright 2011, 2012 Mark O'Connor. This program is distributed under the terms of the GNU General Public License v3.

from pyratemp import Template
from json import dumps, loads
import re
import random
from colorsys import hsv_to_rgb, rgb_to_hsv

def format_output(output):
    for trace in output:
        for i in xrange(len(trace['data'])):
            x, snapshot = trace['data'][i]
            if len(snapshot) == 4:
                cpu, mem, io, stack = snapshot
                stack.reverse()
                snapshot = cpu, mem, io, stack, colours(stack)
                trace['data'][i] = (x, snapshot)
    data = { 'traces': output, 'palette': [ '#%x' % c for c in current_palette() ]  }
    t = Template(filename='report-template.html', data=data)
    html = u'%s' % t
    max_length = max(o['data'][-1][0] for o in output) if len(output) else 0
    json = dumps(output)
    html = html % (json, max_length)
    return (json, expand_scripts(html).encode('utf-8'))

def expand_scripts(html):
    return re.sub(r'<script src="([\w\.\-_\d]+)"></script>', lambda f: u'<script>%s</script>' % open(f.group(1)).read().decode('utf-8'), html)
    
def colours(stack):
    return [ '#%x' % colour_from_palette(*find_names(frame)) for frame in stack ]

def find_names(frame):
    full = frame.split(' in ', 1)[1] if ' in ' in frame else frame
    name = full.split('(', 1)[0].strip()
    if '::' in name:
        return name.split('::', 1)
    else:
        return ('', name)

def colour_from_palette(base_name, function_name):
    palette = current_palette()
#            index = (base_name + "." + function_name).__hash__() % len(palette)
    if len(base_name) == 0:
        index = function_name.__hash__() % len(palette)
    else:
        index = base_name.__hash__() % len(palette)
    return palette[index]

def current_palette():
    storm = [0xc1000f, 0x8d1155, 0x64008a, 0x200085, 0x005e92, 0x0088ac, 0x00d2b7, 0x00a08a, 0x7ccd6c, 0xdc754c, 0xd5954b]
    juicy = [0xe88c88, 0xcc90ad, 0xb986c5, 0x9086c2, 0x78b0c9, 0x68c4d6, 0x26e9db, 0x58d0c5, 0xc2e4b7, 0xf1bba8, 0xebcba6]
    codechart = [0xc1000f, 0x8d1155, 0x74009a, 0x200085, 0x207eb2, 0x0088ac, 0x00c2a7, 0x00a08a, 0x6cbd5c]
    urban = [0xab685a, 0xd57a5d, 0xc18b73, 0x7b9254, 0x9fa668, 0x8fb596, 0x6a6768, 0x7e8c8d, 0x92b4b9, 0x867a6a, 0x9f867c, 0xaaa096, 0xb16671, 0xa27893, 0xb97c92, 0x9b8768, 0xcaa566, 0xc6b27b]
    spring_frost = [0x7eaeb8, 0x889fbf, 0x87a07a, 0xa6bd9b, 0x49bdcf, 0xa6c1e9, 0x7cae95, 0xbcd29d, 0x8c9494, 0xb3ad94, 0x937f6a, 0xc69e85]
    harvest = [0xd9bb6d, 0xe4c38b, 0xd7a085, 0xc4686e, 0xd1845d, 0xbc665d, 0x868289, 0xa0a6a4, 0x869e9a, 0xa69595, 0xa99086, 0xa79178]
    # rainbow
    # return rainbow(base_name, function_name)
    num_colours = 16
    rainbow = [ convert_hsv(float(i) / num_colours, 0.6, 0.875) for i in range(num_colours) ]
    grey = [ convert_hsv(0.5, float(i) / num_colours, 1) for i in range(num_colours) ]
    return rainbow

def convert_hsv(h, s, v):
    r, g, b = hsv_to_rgb(h, s, v)
    return (int(r*255.0) << 16) + (int(g*255.0) << 8) + int(b*255.0)

def boost(icol, sb, vb):
    r = (icol & 0xff0000) >> 16
    g = (icol & 0x00ff00) >> 8
    b = (icol & 0x0000ff)
    h, s, v = rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    s = min(1.0, s + sb)
    v = min(1.0, v + vb)
    return convert_hsv(h, s, v)

def rainbow(base_name, function_name):
    """ We really want to do this in the client; flash doesn't have random with seed,
        but maybe we can do it via a javascript call """
    if function_name == '??':
        return 0xe0e0e0
    if base_name == '':
        random.seed(function_name)
    else:
        random.seed(base_name)
    random.random()
    h = (int(random.random() * (360.0 - 50.0)) / 20) * 20.0
    if h>30: h += 50 # skip nasty green-yellow hues
    random.seed(function_name)
    random.random()
#            if "ThreadContext" in base_name:
#                print "Colour for %s:%s - %d" % (base_name, function_name, h)
    h /= 360.0
    s = random.random() * 0.00 + 0.30
    v = random.random() * 0.00 + 0.885
    return convert_hsv(h, s, v)

if __name__ == '__main__':
    json = open('ddt.bin.json').read()
    output = loads(json)
    open('ddt.bin.html', 'w').write(format_output(output)[1])
