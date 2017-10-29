#!/usr/bin/env python

'''
test_intervals.py - Class for testing general intervals behaviour.

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

from nose.tools import assert_equal, assert_true, raises

from time_intervals.intervals import *
from datetime import datetime, timedelta

class TestIntervals(object):
    def setup(self):
        self.overlapping_interval_list = [(datetime(2016, 1, 1), datetime(2016, 3, 1)),
                                          (datetime(2016, 2, 1), datetime(2016, 4, 1)),
                                          (datetime(2016, 6, 1), datetime(2016, 7, 1))]

        self.non_overlapping_interval_list = [(datetime(2016, 2, 1), datetime(2016, 3, 1)),
                                              (datetime(2016, 4, 1), datetime(2016, 6, 1))]

    def test_adding_zero_intervals_to_empty_intervals(self):
        intervals = Intervals()
        intervals.add([])
        assert_true(intervals.is_empty())

    def test_adding_zero_intervals_to_existing_intervals(self):
        intervals = Intervals(self.non_overlapping_interval_list)
        intervals.add([])
        assert_equal(intervals.toTupleList(), self.non_overlapping_interval_list)

    @raises(IntervalsError)
    def test_adding_bad_intervals_throws_exception(self):
        intervals = Intervals(self.overlapping_interval_list)
        intervals.add('This is not a list')

    @raises(IntervalsError)
    def test_adding_mixed_intervals_throws_exception(self):
        intervals = Intervals(self.overlapping_interval_list)
        intervals_to_add = []
        intervals_to_add.extend(intervals.toDictList())
        intervals_to_add.extend(self.non_overlapping_interval_list)
        intervals.add(intervals_to_add)




