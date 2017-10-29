#!/usr/bin/env python

'''
test_intervals_dict_int.py - Class for testing intervals constructed with dicts and ints

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

class TestIntervalsDictInt(object):
    
    def setup(self):
        # t1(1) ----  t2(3) 
        #       t3(2) ----- t4(4) 
        #                   t5(4) t6(5)
        t1={'time':1, 'type':'start'}
        t2={'time':3, 'type':'end'}
        
        t3={'time':2, 'type':'start'}
        t4={'time':4, 'type':'end'}

        t5={'time':4, 'type':'start'}
        t6={'time':5, 'type':'end'}

        self.i1=Intervals([t1, t2, t5, t6], 'free')
        self.i2=Intervals([t3, t4])
        self.i3=Intervals([t1, t2, t5, t6, t1, {'time':2,'type':'end'}])
        self.i4=Intervals([t1, t2, t5, t6, {'time':6, 'type':'start'}, {'time':7, 'type':'end'}], 'free')
        self.i5=Intervals([t1, t6])
        self.i6=Intervals([t1, t2, t5, t6, {'time':2, 'type':'start'}, {'time':2,'type':'end'}])
        self.i8=Intervals([])


    def test_remove_intervals_smaller_than_1(self):
        self.i1.remove_intervals_smaller_than(2)
        assert_equal(self.i1.timepoints[0]['time'], 1)
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], 3)
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(len(self.i1.timepoints), 2)


    def test_remove_intervals_smaller_than_2(self):
        self.i1.remove_intervals_smaller_than(3)
        assert_equal(len(self.i1.timepoints), 0)
            

    def test_create(self):
        assert_equal(self.i1.timepoints[0]['time'], 1)
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], 3)
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(self.i1.timepoints[2]['time'], 4)
        assert_equal(self.i1.timepoints[2]['type'], 'start')
        assert_equal(self.i1.timepoints[3]['time'], 5)
        assert_equal(self.i1.timepoints[3]['type'], 'end')


    def test_add_1(self):
        self.i1.add([{'time':6, 'type':'start'}, {'time':7, 'type':'end'}])
        assert_equal(self.i1.timepoints[4]['time'], 6)
        assert_equal(self.i1.timepoints[4]['type'], 'start')
        assert_equal(self.i1.timepoints[5]['time'], 7)
        assert_equal(self.i1.timepoints[5]['type'], 'end')


    def test_add_2(self):
        '''
        Tests an add() that introduced two start-ends for removal
        by normalize()
        '''
        self.i4.add([{'time':5, 'type':'start'}, {'time':6, 'type':'end'}])
        assert_equal(self.i4.timepoints[3]['time'], 7)
        assert_equal(self.i4.timepoints[3]['type'], 'end')


    def test_intersect_1(self):
        i = self.i1.intersect([self.i1])
        assert_equal(i.timepoints[0]['time'], 1)
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], 3)
        assert_equal(i.timepoints[1]['type'], 'end')
        assert_equal(i.timepoints[2]['time'], 4)
        assert_equal(i.timepoints[2]['type'], 'start')
        assert_equal(i.timepoints[3]['time'], 5)
        assert_equal(i.timepoints[3]['type'], 'end')


    def test_intersect_2(self):
        i = self.i1.intersect([self.i2])
        assert_equal(i.timepoints[0]['time'], 2)
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], 3)
        assert_equal(i.timepoints[1]['type'], 'end')


    def test_intersect_empty(self):
        i = self.i1.intersect([self.i8])
        assert_equal(i.timepoints, [])


    def test_complement(self):
        self.i1.complement(0,10)
        assert_equal(self.i1.timepoints[0]['time'], 0)
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], 1)
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(self.i1.timepoints[2]['time'], 3)
        assert_equal(self.i1.timepoints[2]['type'], 'start')
        assert_equal(self.i1.timepoints[3]['time'], 4)
        assert_equal(self.i1.timepoints[3]['type'], 'end')
        assert_equal(self.i1.timepoints[4]['time'], 5)
        assert_equal(self.i1.timepoints[4]['type'], 'start')
        assert_equal(self.i1.timepoints[5]['time'], 10)
        assert_equal(self.i1.timepoints[5]['type'], 'end')
        

    def test_subtract_1(self):
        i = self.i1.subtract(self.i2)
        assert_equal(i.timepoints[0]['time'], 1)
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], 2)
        assert_equal(i.timepoints[1]['type'], 'end')
        assert_equal(i.timepoints[2]['time'], 4)
        assert_equal(i.timepoints[2]['type'], 'start')
        assert_equal(i.timepoints[3]['time'], 5)
        assert_equal(i.timepoints[3]['type'], 'end')


    def test_subtract_2(self):
        interval = Intervals([{'time':1,'type':'start'}, {'time':2, 'type':'end'}])
        i = self.i5.subtract(interval)
        assert_equal(i.timepoints[0]['time'], 2)
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], 5)
        assert_equal(i.timepoints[1]['type'], 'end')
        

    def test_subtract_empty(self):
        i = self.i1.subtract(Intervals([]))
        assert_equal(i.timepoints[0]['time'], 1)
        assert_equal(i.timepoints[0]['type'], 'start')
        assert_equal(i.timepoints[1]['time'], 3)
        assert_equal(i.timepoints[1]['type'], 'end')
        assert_equal(i.timepoints[2]['time'], 4)
        assert_equal(i.timepoints[2]['type'], 'start')
        assert_equal(i.timepoints[3]['time'], 5)
        assert_equal(i.timepoints[3]['type'], 'end')
        

    def test_subtract_from_empty(self):
        i = self.i8.subtract(self.i1)
        assert_equal(i.timepoints, [])


    def test_normalize_1(self):
        ''' 
        Nested interval clean up 
        '''
        self.i3.normalize()
        assert_equal(self.i3.timepoints[0]['time'], 1)
        assert_equal(self.i3.timepoints[0]['type'], 'start')
        assert_equal(self.i3.timepoints[1]['time'], 3)
        assert_equal(self.i3.timepoints[1]['type'], 'end')
        assert_equal(self.i3.timepoints[2]['time'], 4)
        assert_equal(self.i3.timepoints[2]['type'], 'start')
        assert_equal(self.i3.timepoints[3]['time'], 5)
        assert_equal(self.i3.timepoints[3]['type'], 'end')


    def test_normalize_2(self):
        '''
        Empty interval clean up
        '''
        self.i6.normalize()
        assert_equal(self.i6.timepoints[0]['time'], 1)
        assert_equal(self.i6.timepoints[0]['type'], 'start')
        assert_equal(self.i6.timepoints[1]['time'], 3)
        assert_equal(self.i6.timepoints[1]['type'], 'end')
        assert_equal(self.i6.timepoints[2]['time'], 4)
        assert_equal(self.i6.timepoints[2]['type'], 'start')
        assert_equal(self.i6.timepoints[3]['time'], 5)
        assert_equal(self.i6.timepoints[3]['type'], 'end')


    def test_normalize_empty(self):
        self.i8.normalize()
        assert_equal(self.i8.timepoints, [])


    def test_get_total_time(self):
        t = self.i1.get_total_time()
        assert_equal(t, 3)


    def test_get_total_time_empty(self):
        t = self.i8.get_total_time()
        assert_equal(t,0)


    def test_trim_to_time(self):
        self.i1.trim_to_time(2)
        assert_equal(self.i1.timepoints[0]['time'], 1)
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], 3)
        assert_equal(self.i1.timepoints[1]['type'], 'end')
