#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

import logging
from urlparse import urljoin
from StringIO import StringIO

from grab import Grab
import PyV8
from PIL import Image
from PyQt4 import QtCore

from tesseract import Tesseract, TessPageSegMode
import startup


log = logging.getLogger(__name__)


class Avito():
    PAGETRY = 3
    SLEEP = 1

    def __init__(self, proxy=None):
        self.PAGETRY, rc = startup.CFG.value('pagetry', Avito.PAGETRY).toInt()
        self.SLEEP, rc = startup.CFG.value('sleep', Avito.SLEEP).toInt()

        self.g = Grab()
        self.g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (5, 10)))
        if __name__ == '__main__':
            self.g.setup(log_dir='dump')
        if proxy:
            self.g.load_proxylist(proxy, 'text_file', 'http', auto_init=True, auto_change=False)
        self.tess = Tesseract()
        self.tess.set_pagemode(TessPageSegMode.PSM_SINGLE_LINE)

    def _go3(self, url, tag):
        c = self.PAGETRY
        while c:
            try:
                self.g.change_proxy()
                self.g.go(url)
                self.g.assert_substring(u'content="51a6d66a02fb23c7"')
                break
            except:
                log.exception('%s left %i', tag, c)
                c -= 1
                QtCore.QThread.sleep(self.SLEEP)
        else:
            raise Exception('%s error' % tag)

    def get_links(self, url):
        self._go3(url, 'start page')
        c = 999
        while True:
            links = self.g.doc.select('//h3[@class="title"]/a/@href')
            if not links:
                raise Exception('no links')
            for link in links:
                c -= 1
                if not c:
                    return
                yield urljoin(url, link.text())
            next = self.g.doc.select('//a[@class="next"]/@href')
            if not next:
                log.debug('last page?')
                break
            QtCore.QThread.sleep(self.SLEEP)
            nurl = urljoin(url, next.text())
            log.debug('open next page %s', nurl)
            self._go3(nurl, 'next page')

    def get_photos(self, photos):
        g = self.g.clone()
        datas = []
        for url in photos:
            if not url.startswith('http:'):
                url = 'http:' + url
            c = self.PAGETRY
            while c:
                try:
                    rc = g.go(url)
                    g.assert_substring('JFIF', byte=True)
                    datas.append(rc.body)
                    break
                except:
                    log.exception('get_item left %i', c)
                    c -= 1
                    g.change_proxy()
                    QtCore.QThread.sleep(self.SLEEP)
            else:
                raise Exception('get photo error')
        return datas

    def get_item(self, url):
        g = self.g.clone()
        c = self.PAGETRY
        while c:
            try:
                g.change_proxy()
                g.go(url)
                g.assert_substring(u'content="499bdc75d3636c55"') # avitos ya id
                break
            except:
                log.exception('get_item left %i', c)
                c -= 1
                QtCore.QThread.sleep(self.SLEEP)
        else:
            raise Exception('get item error')
        doc = g.doc
        title = doc.select('//h1[@itemprop="name"]').text()
        gallery = doc.select('//div[@class="gallery-item"]')
        photos = [s.text() for s in gallery.select('.//a[@class="gallery-link"]/@href')]
        if not photos:
            egg = doc.select('//img[contains(@class,"j-zoom-gallery-init")]/@src')
            if egg:
                photos.append(egg.text())
        item = doc.select('//div[@itemprop="offers"]')
        #price = item.select('.//strong[@itemprop="price"]').text()
        price = item.select('.//span[@itemprop="price"]').text()
        name = item.select('.//strong[@itemprop="name"]').text()

        try:
            town = item.select('.//span[@id="toggle_map"]/span[@itemprop="name"]').text()
        except:
            log.warning('xpath town not found, try another way')
            town = item.select('.//div[@id="map"]/span[@itemprop="name"]').text()
        #desc = item.select('.//div[@id="desc_text"]').text()
        desc = doc.select("//div[contains(@class,\"description-text\")]").text()
        #<span id="item_id">348967351</span>
        item_id = doc.select('//span[@id="item_id"]').text()
        _url = g.rex_text("avito.item.url = '([^>]+?)'")
        _phone = g.rex_text("avito.item.phone = '([^>]+?)'")

        loc = {
            'item_phone': _phone,
            'item': {'id': item_id, 'url': _url}
        }
        log.debug('jslock enter <--')
        with PyV8.JSContext(loc) as ctx:
            ctx.enter()
            ctx.eval('''function phoneDemixer(key){var
    pre=key.match(/[0-9a-f]+/g),mixed=(item.id%2===0?pre.reverse():pre).join(''),s=mixed.length,r='',k;for(k=0;k<s;++k){if(k%3===0){r+=mixed.substring(k,k+1);}}
    return r;}''')

            #http://www.avito.ru/items/phone/348967351?pkey=6fec07a9bb9902ad4ccbd87c240cfdc4
            egg = ctx.eval("'/items/phone/'+item.id+'?pkey='+phoneDemixer(item_phone)")
            #egg = ctx.eval("'/items/phone/'+item.url+'?pkey='+phoneDemixer(item_phone)")
            log.debug('js rc %s', egg)
            ctx.leave()
        log.debug('jslock leave -->')
        phone = ''
        c = self.PAGETRY
        while c:
            log.debug('read phone image')
            try:
                rc = g.go(urljoin(url, egg))
                img = Image.open(StringIO(rc.body))
                phone = self.tess.from_image(img, basewidth=300, whitelist='0123456789-')
                break
            except:
                g.change_proxy()
                log.exception('get_phone left %i', c)
                c -= 1
                QtCore.QThread.sleep(self.SLEEP)
        else:
            log.debug('get phone error')

        return dict(item=item_id, title=title, photos=photos, price=price, name=name, town=town,
                    desc=desc, phone=phone)


def main():
    p = Avito()  # r"d:\work\proxycheck2\rusarticles.txt")

    item = p.get_item('http://www.avito.ru/krasnodar/kvartiry/3-k_kvartira_103_m_1718_et._457340825')
    print item['town']
    print item['phone']
    print len(p.get_photos(item['photos']))

    '''
    c = 0
    for link in p.get_links('http://www.avito.ru/lipetsk/noutbuki'):
        c += 1
        print "%i.%s" % (c, link)
        if c > 10:
            break
    '''


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
