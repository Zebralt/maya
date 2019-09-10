import os
import sys
import textwrap
import yaml
import time
import re
# A text game uh
from functools import partial
from cachetools import cached
from cachetools.lru import LRUCache


def recook(d):
    
    d = d.strip()
    d = d.replace(' ', ' ?')

    return d


class Scene:

    @classmethod
    @cached(cache=LRUCache(maxsize=32))
    def fromfile(cls, filepath):
        filepath = os.fspath(filepath)
        c = cls(
            **yaml.safe_load(open(filepath))
        )
        c.origin = filepath
        return c

    def __init__(self, title, content, author='', choices=[]):
        self.title = title
        self.content = content
        self.author = author
        self.choices = {
            recook(c['capture']): c['to']
            for c in choices
        }

    def pick(self, key):
        
        next_ = self.choices[key]
        if type(next_) is str:
            next_ = self.fromfile(next_)

        return next_

    def examine(self, ans):

        for k in self.choices:
            if re.match(k, ans):
                return self.pick(k)
        
        return None

    def reload(self):
        if 'origin' in self.__dict__:
            print('\0337\033[1;200H[Reloaded]\0338')
            return self.fromfile(self.origin)
        return self


d = Scene(
    title='Smelling',
    content="""
    This and that
    """
)

WIDTH = 70
textwrap.fill = partial(textwrap.fill, width=WIDTH)
textwrap.wrap = partial(textwrap.wrap, width=WIDTH)

if __name__ == "__main__":

    print('\033[2J')
        
    s = Scene.fromfile('scene.yaml')
    title = s.title or 'placeholder_title'
    content = s.content or 'placeholder_content'
    content = textwrap.fill(content)

    while 1:

        print('\033[1;2H', end='')
        sys.stdout.flush()

        idd = ''
        idd = os.get_terminal_size(0).columns / 2 - WIDTH / 2
        idd = ' ' * int(idd)
        # idd = '\033[4m%s\033[m' % idd

        print()
        # print(idd + ('_ ' + title + ' _').center(WIDTH))
        print(idd + ('\033[1;93m_ ' + title + ' _\033[m').center(WIDTH + 10))
        print()
        print('\n'.join(
            idd + line
            for line in content.split('\n')
        ))

        try:
            print('\033[92m')
            ans = input(idd + '')
        except EOFError:
            print()
            break
        print('\033[m')

        if ans.casefold().strip() == 'r':
            s = s.reload()
            continue

        if ans.casefold() == 'exit':
            break

        print(
            '\033[A' * (2 + 1 + 1 + len(s.content.split('\n'))),
            '\033[J'
        )
        
        ns = s.examine(ans)

        if ns is not None:
            s = ns
            title = s.title or title
            content = s.content or content
            content = textwrap.fill(content)

        else:

            sys.stdout.write('\033[1900f\033[91m This no work! \033[m')
            sys.stdout.flush()


    print('\033[J')