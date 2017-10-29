#!/usr/bin/env python

'''
test_intervals_tuple_int.py - Class for testing intervals constructed with tuples and ints

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

class TestIntervalsTupleInt(object):
    
    def setup(self):
        # 1 ----  3 
        #    2 ----- 4 
        #            4 ---- 5
        self.i1=Intervals([(1,3), (4,5)], 'free')
        self.i3=Intervals([(1,3), (4,5), (1,2)])
        self.i4=Intervals([(1,3), (4,5), (6,7)], 'free')
        self.i6=Intervals([(1,3), (4,5), (2,2)])
        self.i8=Intervals([])


    def test_create1(self):
        assert_equal(self.i1.timepoints[0]['time'], 1)
        assert_equal(self.i1.timepoints[0]['type'], 'start')
        assert_equal(self.i1.timepoints[1]['time'], 3)
        assert_equal(self.i1.timepoints[1]['type'], 'end')
        assert_equal(self.i1.timepoints[2]['time'], 4)
        assert_equal(self.i1.timepoints[2]['type'], 'start')
        assert_equal(self.i1.timepoints[3]['time'], 5)
        assert_equal(self.i1.timepoints[3]['type'], 'end')
        assert_equal(self.i1.label, 'free')

    def test_create3(self):
        assert_equal(self.i3.timepoints[0]['time'], 1)
        assert_equal(self.i3.timepoints[0]['type'], 'start')
        assert_equal(self.i3.timepoints[1]['time'], 3)
        assert_equal(self.i3.timepoints[1]['type'], 'end')
        assert_equal(self.i3.timepoints[2]['time'], 4)
        assert_equal(self.i3.timepoints[2]['type'], 'start')
        assert_equal(self.i3.timepoints[3]['time'], 5)
        assert_equal(self.i3.timepoints[3]['type'], 'end')

    def test_create6(self):
        assert_equal(self.i6.timepoints[0]['time'], 1)
        assert_equal(self.i6.timepoints[0]['type'], 'start')
        assert_equal(self.i6.timepoints[1]['time'], 3)
        assert_equal(self.i6.timepoints[1]['type'], 'end')
        assert_equal(self.i6.timepoints[2]['time'], 4)
        assert_equal(self.i6.timepoints[2]['type'], 'start')
        assert_equal(self.i6.timepoints[3]['time'], 5)
        assert_equal(self.i6.timepoints[3]['type'], 'end')

    def test_totuplelist(self):
        tl = self.i1.toTupleList()
        assert_equal(tl, [(1,3), (4,5)])

    def test_add_1(self):
        self.i1.add([(6, 7)])
        assert_equal(self.i1.timepoints[4]['time'], 6)
        assert_equal(self.i1.timepoints[4]['type'], 'start')
        assert_equal(self.i1.timepoints[5]['time'], 7)
        assert_equal(self.i1.timepoints[5]['type'], 'end')


    def test_add_2(self):
        '''
        Tests an add() that introduced two start-ends for removal
        by normalize()
        '''
        self.i4.add([(5,6)])
        assert_equal(self.i4.timepoints[3]['time'], 7)
        assert_equal(self.i4.timepoints[3]['type'], 'end')
