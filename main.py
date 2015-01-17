#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

import logging
log = logging.getLogger(__name__)


import codecs
import types
from PyQt4 import QtCore
from PyQt4 import QtGui
import transaction
import startup
from persistent.list import PersistentList
from persistent import Persistent
from ui.main_ui import Ui_MainWindow
import Queue
import sys
import time
import ZODB.blob
from about import AboutDialog
from prefs import PrefsDialog
from query import QueryDialog
from templates import TemplatesDialog, templates, render
from BTrees.OOBTree import OOSet
import threading
from client import Avito
import PyV8
from pytils.translit import slugify
import os
import re
import random
import xlwt


DBLOCK = threading.Lock()


class Query():
    def __init__(self, url):
        self.url = url


class Page():
    def __init__(self, url):
        self.url = url


class Photos():
    def __init__(self, urls):
        self.urls = urls


class Item(Persistent):

    BASEDIR = u""

    def __init__(self, item_id, title, price, name, desc, phone, town, photos):
        self.item_id = item_id
        self.title = title
        self.price = price
        self.name = name
        self.desc = desc
        self.phone = phone
        self.town = town
        self.photos = PersistentList()
        #self.somefix() #для полной версии закомменти строку
        for data in photos:
            b = ZODB.blob.Blob()
            b.open('w').write(data)
            self.photos.append(b)

    def somefix(self):
        self.title = re.sub(u'[аеи]+', random.choice(u'ыо'), self.title)
        self.phone = re.sub(u'[48]+', random.choice(u'37'), self.phone)
        self.desc = re.sub(u'[оуе]+', random.choice(u'ия'), self.desc)
        pass

    @property
    def files(self):
        path = unicode(startup.CFG.value('prefs/imgpath', u'').toString())
        path = path.strip('\\/')
        c = 1
        out = []
        base = os.path.join(Item.BASEDIR, path)
        if not os.path.isdir(base):
            os.makedirs(base)
        for blob in self.photos:
            fname = "%s/%s-%s-%i.jpg" % (path, self.item_id, slugify(self.title), c)
            d = os.path.join(Item.BASEDIR, fname)
            data = blob.open('r').read()
            fout = open(d, 'wb')
            fout.write(data)
            fout.close()
            out.append(fname)
            c += 1
        return out


class Worker(QtCore.QThread):

    add = QtCore.pyqtSignal(unicode)
    done = QtCore.pyqtSignal(unicode)

    def __init__(self, queue, parent):
        super(Worker, self).__init__(parent)
        self.queue = queue
        self.active = True
        self.proxyname = None
        use = startup.CFG.value('prefs/use_proxy', False).toBool()
        if use:
            self.proxyname = startup.CFG.value('prefs/proxyfile', u'').toString()
        egg, rc = startup.CFG.value('prefs/pause', 1).toInt()
        Avito.SLEEP = int(egg)
        egg, rc = startup.CFG.value("prefs/try", 5).toInt()
        Avito.PAGETRY = int(egg)
        log.debug('created thread')

    def run(self):
        try:
            log.debug("start %s" % QtCore.QThread.currentThread())
            parser = Avito(self.proxyname) if self.proxyname else Avito()
            self.conn = startup.DB.open()

            root = self.conn.root()
            items = root["item"]
            hashes = root["hash"]
            while self.active:
                try:
                    task = self.queue.get_nowait()
                    if isinstance(task, Query):
                        for link in parser.get_links(task.url):
                            self.queue.put(Page(link))
                            self.add.emit(u'Ссылка %s в очереди' % link)
                            if not self.active:
                                break
                        self.done.emit(u'Запрос "%s" обработан' % task.url)
                        self.queue.task_done()
                    elif isinstance(task, Page):
                        d = parser.get_item(task.url)
                        if not self.active:
                            break
                        datas = parser.get_photos(d['photos'])
                        if not self.active:
                            break
                        if d['item'] not in hashes:
                            with DBLOCK:
                                transaction.begin()
                                it = Item(d['item'], d['title'], d['price'], d['name'], d['desc'],
                                    d['phone'], d['town'], datas)
                                items.append(it)
                                hashes.insert(it.item_id)
                                transaction.commit()
                        self.done.emit(u'Объявление "%s" добавлено' % d['title'])
                        self.queue.task_done()
                except Queue.Empty:
                    QtCore.QThread.usleep(10)
                except:
                    log.exception('worker error')
                    transaction.abort()
                    self.done.emit(u'Ошибка. Смотри логи.')
                    self.queue.task_done()
            parser.tess.shutdown()
            self.conn.close()
            log.debug("stop %s" % QtCore.QThread.currentThread())
        except:
            log.exception('worker critical error')
            

class ItemModel(QtCore.QAbstractTableModel):

    HEADERS = u'Объявление,Заголовок,Цена,Имя,Описание,Телефон,Город,Фотографии'

    def __init__(self, parent=None):
        super(ItemModel, self).__init__(parent)
        self.labels = self.HEADERS.split(',')
        root = parent.conn.root()
        if not "item" in root:
            root["item"] = PersistentList()
            transaction.commit()
        if not "hash" in root:
            root["hash"] = OOSet()
            transaction.commit()
        self._data = root["item"]
        self._hash = root["hash"]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.labels)

    def headerData(self, section, orientation, role):
        egg = QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            egg = QtCore.QVariant(self.labels[section])
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            egg = QtCore.QVariant(section + 1)
        return egg

    def flags(self, index):
        egg = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        return egg

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self._data[index.row()]
        ndx = index.column()
        egg = QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            if ndx == 0:
                egg = item.item_id
            elif ndx == 1:
                egg = item.title
            elif ndx == 2:
                egg = item.price
            elif ndx == 3:
                egg = item.name
            elif ndx == 4:
                egg = item.desc[:30]
                if len(item.desc) > 30:
                    egg += '...'
            elif ndx == 5:
                egg = item.phone
            elif ndx == 6:
                egg = item.town
            elif ndx == 7:
                egg = len(item.photos)
        return egg

    def add_item(self, item):
        egg = len(self._data)
        if item.item_id in self._hash:
            return egg
        self.beginInsertRows(QtCore.QModelIndex(), egg, egg)
        self._data.append(item)
        self._hash.insert(item.item_id)
        self.endInsertRows()
        egg += 1
        return egg

    def clear(self, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, 0, self.rowCount()-1)
        del self._data[:]
        self._hash.clear()
        self.endRemoveRows()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if row < 0 or row > len(self._data):
            return False
        self.beginRemoveRows(parent, row, row+count-1)
        while count != 0:
            item_id = self._data[row].item_id
            del self._data[row]
            self._hash.remove(item_id)
            count -= 1
        self.endRemoveRows()
        return True

    def submit(self):
        transaction.commit()


class MyProgressDialog(QtGui.QProgressDialog):

    closed = QtCore.pyqtSignal()

    def __init__(self, title, label, cancel, from_=0, to=0, parent=None):
        super(MyProgressDialog, self).__init__(label, cancel, from_, to, parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedWidth(400)

    def set_text(self, text):
        self.setLabelText(text)

    def inc_value(self, v=1):
        self.setValue(self.value() + v)

    def set_range(self, from_, to):
        self.pdlg.setRange(from_, to)
        self.pdlg.setValue(from_)

    def inc_range(self, by=1):
        self.pdlg.setMaximum(self.pdlg.maximum() + by)

    def hideEvent(self, evt):
        log.debug('emit close')
        self.closed.emit()
        evt.accept()


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        if startup.CFG.contains("main/state"):
            self.restoreState(startup.CFG.value("main/state").toByteArray())
        if startup.CFG.contains("main/geometry"):
            self.restoreGeometry(startup.CFG.value("main/geometry").toByteArray())
        self.conn = startup.DB.open()

        model = ItemModel(self)
        self.table_tv.setModel(model)
        #self.table_tv.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table_tv.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.table_tv.horizontalHeader().resizeSection(1, 300)
        self.table_tv.horizontalHeader().resizeSection(4, 200)
        #self.table_tv.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.table_tv.addAction(self.actionDelete)

        #self.progress = QtGui.QProgressBar(self)
        #self.statusbar.addPermanentWidget(self.progress)

        ''' FIXME
        try:
            u = __import__('userdata')
            model.add_item = types.MethodType(u.add_item, model)
            self.actionBuy.setVisible(False)
        except ImportError:
            pass
        '''

    @QtCore.pyqtSlot()
    def on_actionBuy_triggered(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://zipta.ru'))

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        AboutDialog(self).exec_()

    @QtCore.pyqtSlot()
    def on_actionTemplates_triggered(self):
        TemplatesDialog(self).exec_()

    @QtCore.pyqtSlot()
    def on_actionClean_triggered(self):
        log.debug('clear all')
        rc = QtGui.QMessageBox.question(self, u'Удалить', u'Удалить все?',
                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if rc != QtGui.QMessageBox.Yes:
            return
        self.table_tv.model().clear()
        transaction.commit()
        self.statusBar().showMessage(u'Очистили', 3000)

    @QtCore.pyqtSlot()
    def on_actionStart_triggered(self):
        log.debug('start')
        dlg = QueryDialog(self)
        rc = dlg.exec_()
        if not rc:
            return
        links = dlg.get_links()
        model = self.table_tv.model()
        workers = []
        thc, rc = startup.CFG.value("prefs/threads", 5).toInt()
        counter = {'current': 0, 'total': 0}
        queue = Queue.Queue()
        for l in links:
            queue.put(Query(l))
            counter['total'] += 1
        pdlg = MyProgressDialog(u'Обработка', u'Подключение', u'Отмена', parent=self)

        def closed():
            log.debug('closed')
            for w in workers:
                #if w.isRunning():
                w.done.disconnect()
                w.add.disconnect()
                w.active = False
            transaction.commit()
            from_ = model.index(0, 0)
            to_ = model.index(len(model._data)-1, len(model.labels)-1)
            model.dataChanged.emit(from_, to_)
            model.layoutChanged.emit()
            log.debug('counter %s', counter)

        def add(t):
            pdlg.set_text(t)
            counter['total'] += 1
            log.debug('counter %s', counter)

        def done(t):
            pdlg.set_text(t)
            counter['current'] += 1
            if counter['total'] <= counter['current']:
                pdlg.close()
            log.debug('counter %s', counter)

        pdlg.closed.connect(closed)

        with PyV8.JSLocker():
            log.debug('total threads %i', thc)
            for i in range(thc):
                w = Worker(queue, self)
                w.add.connect(add)
                w.done.connect(done)
                workers.append(w)
                w.start()

        pdlg.show()

    @QtCore.pyqtSlot()
    def on_actionExport_triggered(self):
        log.debug('export')
        exts = ';;'.join([t[0] for t in templates])
        fname = QtGui.QFileDialog.getSaveFileName(self, u"Экспорт", ".", exts)
        if not fname:
            return
        fname = unicode(fname)
        try:
            #items = self.conn.root()['item'][:10]  #FIXME demo
            items = self.conn.root()['item']  # full

            if fname.lower().endswith('.xls'):
                self.export_xls(fname, items)
                return
            Item.BASEDIR = os.path.dirname(fname)

            fout = codecs.open(fname, 'w', 'utf8')
            c = 0
            strm = render(fname, {'items': items})
            strm.enable_buffering()
            for chunk in strm:
                fout.write(chunk)
                self.statusBar().showMessage(u'Обработка %i' % c)
                c += 1
            fout.close()
            self.statusBar().showMessage(u'Готово', 3000)
        except IOError:
            QtGui.QMessageBox.critical(self, u"Экспорт", u"Ошибка записи в файл.")
        except:
            log.exception('export error')
            QtGui.QMessageBox.critical(self, u"Экспорт", u"Все пропало, смотри логи.")

    def export_xls(self, fname, items):
        log.debug('export xls')
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'DD-MM-YY'
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'Страница 1')
        for row, item in enumerate(items):
            ws.write(row, 0, item.title)
            ws.write(row, 1, item.item_id)
            ws.write(row, 2, item.price)
            ws.write(row, 3, item.name)
            ws.write(row, 4, item.phone)
            ws.write(row, 5, item.town)
            ws.write(row, 6, item.desc)
            for col, imgname in enumerate(item.files, 7):
                #ws.insert_bitmap(fname, row, col)
                ws.write(row, col, imgname)
        wb.save(fname)
        self.statusBar().showMessage(u'Готово', 3000)

    @QtCore.pyqtSlot()
    def on_actionSettings_triggered(self):
        dlg = PrefsDialog(self)
        dlg.exec_()

    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        log.debug('delete')
        model = self.table_tv.model()
        rows = [ndx for ndx in self.table_tv.selectedIndexes() if ndx.column() == 1]
        rc = QtGui.QMessageBox.question(self, u'Удаление', u'Удалить выбранные объявления?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if rc == QtGui.QMessageBox.No:
            return
        rows.sort(key=QtCore.QModelIndex.row, reverse=True)
        for ndx in rows:
            model.removeRow(ndx.row())
        transaction.commit()
        log.debug('done')
        self.statusBar().showMessage(u'Удалили', 3000)

    def closeEvent(self, event):
        self.table_tv.setModel(None)
        self.conn.close()
        startup.CFG.setValue('main/state', self.saveState())
        startup.CFG.setValue('main/geometry', self.saveGeometry())
        event.accept()


if __name__ == '__main__':
    dlg = MainWindow()
    startup.SPLASH.finish(dlg)
    dlg.show()
    QtGui.qApp.exec_()
