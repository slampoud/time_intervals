#!/usr/bin/env python

'''
test_intervals_dict_datetime.py - Class for testing intervals constructed with dicts and datetime objects

Copyright (C) 2017 Sotiria Lampoudi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from nose.tools import assert_equal

from time_intervals.intervals import *
from datetime import datetime, timedelta

class TestIntervalsDictDatetime(object):

    def setup(self):
        # t1(1) ----  t2(3)
        #       t3(2) ----- t4(4)
        #                   t5(4) t6(5)
        t1={'time':datetime(2017,1,1,1,0,0), 'type':'start'}
        t2={'time':datetime(2017,1,1,3,0,0), 'type':'end'}

        t3={'time':datetime(2017,1,1,2,0,0), 'type':'start'}
        t4={'time':datetime(2017,1,1,4,0,0), 'type':'end'}

        t5={'time':datetime(2017,1,1,4,0,0), 'type':'start'}
        t6={'time':datetime(2017,1,1,5,0,0), 'type':'end'}

        self.i1=Intervals([t1, t2, t5, t6], 'free')
        self.i2=Intervals([t3, t4])
        self.i3=Intervals([t1, t2, t5, t6, t1, {'time':datetime(2017,1,1,2,0,0),'type':'end'}])
        self.i4=Intervals([t1, t2, t5, t6, {'time':datetime(2017,1,1,6,0,0), 'type':'start'}, {'time':datetime(2017,1,1,7,0,0), 'type':'end'}], 'free')
        self.i5=Intervals([t1, t6])
        self.i6=Intervals([t1, t2, t5, t6, {'time':datetime(2017,1,1,2,0,0), 'type':'start'}, {'time':datetime(2017,1,1,2,0,0),'type':'end'}])
        self.i8=Intervals([])


    def test_remove_intervals_smaller_than_1(self):
        self.i1.remove_intervals_smaller_than(timedelta(hours=2))
        assert_equal(self.i1.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(len(self.i1.timepoints), 2)


    def test_remove_intervals_smaller_than_2(self):
        self.i1.remove_intervals_smaller_than(timedelta(hours=3))
        assert_equal(len(self.i1.timepoints), 0)


    def test_create(self):
        assert_equal(self.i1.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(self.i1.timepoints[2]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(self.i1.timepoints[2]['type'], 'start')
        assert_equal(self.i1.timepoints[3]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(self.i1.timepoints[3]['type'], 'end')


    def test_add_1(self):
        self.i1.add([{'time':datetime(2017,1,1,6,0,0), 'type':'start'}, {'time':datetime(2017,1,1,7,0,0), 'type':'end'}])
        assert_equal(self.i1.timepoints[4]['time'], datetime(2017,1,1,6,0,0))
        assert_equal(self.i1.timepoints[4]['type'], 'start')
        assert_equal(self.i1.timepoints[5]['time'], datetime(2017,1,1,7,0,0))
        assert_equal(self.i1.timepoints[5]['type'], 'end')


    def test_add_2(self):
        '''
        Tests an add() that introduced two start-ends for removal
        by normalize()
        '''
        self.i4.add([{'time':datetime(2017,1,1,5,0,0), 'type':'start'}, {'time':datetime(2017,1,1,6,0,0), 'type':'end'}])
        assert_equal(self.i4.timepoints[3]['time'], datetime(2017,1,1,7,0,0))
        assert_equal(self.i4.timepoints[3]['type'], 'end')


    def test_intersect_1(self):
        i = self.i1.intersect([self.i1])
        assert_equal(i.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(i.timepoints[1]['type'], 'end')
        assert_equal(i.timepoints[2]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(i.timepoints[2]['type'], 'start')
        assert_equal(i.timepoints[3]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(i.timepoints[3]['type'], 'end')


    def test_intersect_2(self):
        i = self.i1.intersect([self.i2])
        assert_equal(i.timepoints[0]['time'], datetime(2017,1,1,2,0,0))
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(i.timepoints[1]['type'], 'end')


    def test_intersect_empty(self):
        i = self.i1.intersect([self.i8])
        assert_equal(i.timepoints, [])


    def test_complement(self):
        self.i1.complement(datetime(2017,1,1,0,0,0),datetime(2017,1,1,10,0,0))
        assert_equal(self.i1.timepoints[0]['time'], datetime(2017,1,1,0,0,0))
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(self.i1.timepoints[2]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(self.i1.timepoints[2]['type'], 'start')
        assert_equal(self.i1.timepoints[3]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(self.i1.timepoints[3]['type'], 'end')
        assert_equal(self.i1.timepoints[4]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(self.i1.timepoints[4]['type'], 'start')
        assert_equal(self.i1.timepoints[5]['time'], datetime(2017,1,1,10,0,0))
        assert_equal(self.i1.timepoints[5]['type'], 'end')


    def test_subtract_1(self):
        i = self.i1.subtract(self.i2)
        assert_equal(i.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], datetime(2017,1,1,2,0,0))
        assert_equal(i.timepoints[1]['type'], 'end')
        assert_equal(i.timepoints[2]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(i.timepoints[2]['type'], 'start')
        assert_equal(i.timepoints[3]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(i.timepoints[3]['type'], 'end')


    def test_subtract_2(self):
        interval = Intervals([{'time':datetime(2017,1,1,1,0,0),'type':'start'}, {'time':datetime(2017,1,1,2,0,0), 'type':'end'}])
        i = self.i5.subtract(interval)
        assert_equal(i.timepoints[0]['time'], datetime(2017,1,1,2,0,0))
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(i.timepoints[1]['type'], 'end')


    def test_subtract_empty(self):
        i = self.i1.subtract(Intervals([]))
        assert_equal(i.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(i.timepoints[1]['type'], 'end')
        assert_equal(i.timepoints[2]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(i.timepoints[2]['type'], 'start')
        assert_equal(i.timepoints[3]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(i.timepoints[3]['type'], 'end')


    def test_subtract_from_empty(self):
        i = self.i8.subtract(self.i1)
        assert_equal(i.timepoints, [])


    def test_normalize_1(self):
        '''
        Nested interval clean up
        '''
        self.i3.normalize()
        assert_equal(self.i3.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(self.i3.timepoints[0]['type'], 'start')
        assert_equal(self.i3.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(self.i3.timepoints[1]['type'], 'end')
        assert_equal(self.i3.timepoints[2]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(self.i3.timepoints[2]['type'], 'start')
        assert_equal(self.i3.timepoints[3]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(self.i3.timepoints[3]['type'], 'end')


    def test_normalize_2(self):
        '''
        Empty interval clean up
        '''
        self.i6.normalize()
        assert_equal(self.i6.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(self.i6.timepoints[0]['type'], 'start')
        assert_equal(self.i6.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(self.i6.timepoints[1]['type'], 'end')
        assert_equal(self.i6.timepoints[2]['time'], datetime(2017,1,1,4,0,0))
        assert_equal(self.i6.timepoints[2]['type'], 'start')
        assert_equal(self.i6.timepoints[3]['time'], datetime(2017,1,1,5,0,0))
        assert_equal(self.i6.timepoints[3]['type'], 'end')


    def test_normalize_empty(self):
        self.i8.normalize()
        assert_equal(self.i8.timepoints, [])


    def test_get_total_time(self):
        t = self.i1.get_total_time()
        assert_equal(t, timedelta(hours=3))


    def test_get_total_time_empty(self):
        t = self.i8.get_total_time()
        assert_equal(t,0)


    def test_trim_to_time(self):
        self.i1.trim_to_time(timedelta(hours=2))
        assert_equal(self.i1.timepoints[0]['time'], datetime(2017,1,1,1,0,0))
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], datetime(2017,1,1,3,0,0))
        assert_equal(self.i1.timepoints[1]['type'], 'end')
