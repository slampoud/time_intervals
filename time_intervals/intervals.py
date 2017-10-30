#!/usr/bin/env python

'''
intervals.py - Class for specifying and manipulating time intervals.

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

import math
import copy
from datetime import datetime, timedelta

class IntervalsError(Exception):
    pass

class IntervalsConstructionError(Exception):
    pass

class Intervals(object):
    __version__ = '1.0.0'

    def __init__(self, timepoints=[], label=None, paranoid=False):
        ''' 
        timepoints: This can be a list of:
        1. dicts, where each dict contains 2 keys: time and type. The type 
        value must be 'start' or 'end', or
        2. tuples, where each tuple contains 2 times, the first being the 
        start time, which must be less than or equal to the second, the end
        time.
        N intervals can be represented using 2N timepoint dicts or N interval 
        tuples.
        The time value can be any class/type that supports comparison, 
        addition and subtraction.  
        label (optional): one of the strings 'busy' or 'free'.
        paranoid (optional): a boolean telling the class to normalize its 
        contents before every operation. The default is False, in which case
        they are normalized after every write operation.
        '''
        # validate timepoints (not validating type/class of time)
        # 1. check that we have a list
        if not isinstance(timepoints, list):
            raise IntervalsConstructionError('not a list')
        elif not timepoints: # empty list
            self.timepoints=[]
        else:
            # 2. confirm list contents are all dicts or all tuples
            (dict_init, tuple_init) = Intervals.validate_intervals(timepoints)
            # initialize from either all dicts or all tuples
            if timepoints and dict_init and not tuple_init: # all dicts
                self.timepoints = copy.deepcopy(timepoints)
            elif timepoints and tuple_init and not dict_init: # all tuples
                self.timepoints = Intervals.convert_tuples_to_dicts(timepoints)
            elif timepoints: # mixed dicts and tuples
                raise IntervalsConstructionError('mixed list elements')

        # validate label
        self.label = None
        if label == 'busy' or label == 'free':
            self.label = label
        else: # fail quietly, this could be an intended usage
            pass
        # if paranoid is set to true, we'll sort & normalize before every op
        self.paranoid = paranoid
        # sort & normalize the internal representation
        self.normalize(sort=True)

    @staticmethod
    def validate_intervals(timepoints):
        dict_init=1
        tuple_init=1
        for tp in timepoints:
            # 3.1. dicts must have the right fields
            if Intervals.check_dict(tp):
                dict_init*=1
                tuple_init*=0
            # 3.2. tuples must have start <= end
            elif isinstance(tp, tuple) and tp[0] <= tp[1]:
                dict_init*=0
                tuple_init*=1
            else: 
                raise IntervalsConstructionError('bad list element')
        return (dict_init, tuple_init)

    @staticmethod
    def check_dict(tp):
        ''' Utility function for checking if a timepoint dict is well-formed'''
        if isinstance(tp, dict) and \
                'time' in tp and 'type' in tp and \
                (tp['type'] == 'start' or tp['type'] == 'end'):
            return True
        else:
            return False

    @staticmethod
    def convert_tuples_to_dicts(tuplel):
        ''' Utility function for converting tuple inputs to dict inputs.'''
        dictl = []
        for elt in tuplel:
            dictl.append({'type':'start', 'time':copy.deepcopy(elt[0])})
            dictl.append({'type':'end', 'time':copy.deepcopy(elt[1])})
        return dictl

    def toDictList(self):
        ''' Output the intervals in timepoint dict form.'''
        if self.paranoid: self.normalize()
        return self.timepoints

    def toTupleList(self):
        '''Output the intervals in interval tuple form.'''
        tuplel = []
        if self.paranoid: self.normalize()
        if self.timepoints:
            start = None
            for tp in self.timepoints:
                if tp['type'] == 'start':
                    start = tp['time']
                else:
                    tuplel.append((start, tp['time']))
        return tuplel

    @staticmethod
    def sort_timepoints(tps):
        ''' Sorts timepoints (list of dicts format) according to time. If 
        a start & end have the same time, the end will appear before the 
        start.'''
        # sort ends before starts in the first pass (lexicographic)
        tps.sort(key=lambda x: x['type'])
        # sort by time in the second pass (it's stable so it ensures 
        # end before start if times are equal)
        tps.sort(key=lambda x: x['time'])    

    def sort(self):
        ''' Sorts timepoints according to time. If a start & end have the
        same time, the end will appear before the start.'''
        if self.timepoints:
            Intervals.sort_timepoints(self.timepoints)

    def normalize(self, sort=False):
        ''' Normalizes timepoints, meaning it optionally sorts them,  merges 
        overlapping and adjacent intervals, and sanity checks the output.'''
        if self.timepoints:
            # Unless sort is set to True, assume the input is already sorted
            if sort or self.paranoid:
                self.sort()
            # remove end & start with same time -- they cancel
            previous_tp   = None
            clean_tps     = []
            for t in self.timepoints:
                if (previous_tp and
                    (previous_tp['time'] == t['time']) and
                    (previous_tp['type'] == 'end') and
                    (t['type'] == 'start')):
                    clean_tps.pop()
                    if clean_tps:
                        previous_tp = clean_tps[-1]
                    else:
                        previous_tp = None
                else:
                    clean_tps.append(t)
                    previous_tp = t
            # remove nested intervals
            self.timepoints = clean_tps
            clean_tps = []
            flag      = 0
            for t in self.timepoints:
                if t['type'] == 'start':
                    if flag < 1:
                        clean_tps.append(t)
                    flag += 1
                elif t['type'] == 'end':
                    if flag == 1:
                        clean_tps.append(t)
                    flag -= 1
            self.timepoints = clean_tps
            self.sanity_check()

    def sanity_check(self):
        ''' Sanity checks timepoints for various error conditions.'''
        if self.timepoints:
            if len(self.timepoints)%2 == 1:
                raise IntervalsError('odd number of timepoints in Intervals')
            if self.timepoints[0]['type'] == 'end':
                raise IntervalsError('Intervals starting with END')
            if self.timepoints[-1]['type'] == 'start':
                raise IntervalsError('Intervals ending with START')

    def __str__(self):
        string = ""
        for t in self.timepoints:
            if t['type'] == 'start':
                string += repr(t['time']) + "(start) "
            else:
                string += repr(t['time']) + "(end) "
        return string

    def __repr__(self):
        return str(self.serialise())

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def serialise(self):
        return dict(
            timepoints  = str(self.timepoints),
            label       = str(self.label),
            )

    def is_empty(self):
        if self.paranoid: self.normalize()
        if self.timepoints == []:
            return True
        else:
            return False

    def add(self, timepoints):
        ''' Adds interval(s), expressed as a list of timepoint dicts or a list
        of interval tuples, to the Intervals object.'''
        # no need for a normalization, it will happen in the end
        # validate input
        if not timepoints:
            return

        if isinstance(timepoints, list):
            (dict_init, tuple_init) = Intervals.validate_intervals(timepoints)
            if dict_init and not tuple_init:
                self.timepoints.extend(copy.deepcopy(timepoints))
                # sort and normalize
                self.normalize(sort=True)
            elif tuple_init and not dict_init:
                self.timepoints.extend(Intervals.convert_tuples_to_dicts(timepoints))
                # sort and normalize
                self.normalize(sort=True)
            else: 
                raise IntervalsError('Mixed input to add')
        else:
            raise IntervalsError('Ill formatted input to add')

    def union(self, list_of_others):
        ''' Returns a new Intervals object that is the union of self and 
        list_of_others, a list of Intervals objects.'''
        merged_timepoints = list(self.timepoints)
        # merge all lists of timepoints
        for other in list_of_others:
            merged_timepoints.extend(other.timepoints)
        # sorting and cleaning up will be done by the constructor
        return Intervals(merged_timepoints, self.label)

    def get_total_time(self):
        ''' Returns the total amount of time in the intervals. When it
        operates on an empty Intervals it always returns 0, irrespective of
        what type/class of the times are supposed to be, since the the 
        type/class cannot be ascertained.'''
        if self.paranoid: self.normalize()
        sum_val = 0
        if self.timepoints:
            if self.timepoints[0]['type']=='start':
                start = self.timepoints[0]['time']
                # This is poor but unavoidable design: we have to return total
                # time in whatever type/class the times are in, and there is
                # no way to do it without this explicit check. So this will
                # break with novel types/classes I haven't tested for here.
                if isinstance(start, datetime):
                    sum_val = timedelta()
            else:
                raise IntervalsError()
            for t in self.timepoints[1:]:
                if t['type'] == 'start':
                    start = t['time']
                else:
                    sum_val += t['time'] - start
        return sum_val

    def find_interval_of_length(self, length):
        '''Returns the start time of an interval that is equal to or greater
        than length, or -1 if one does not exist. Length has to be of the
        whatever class/type is returned by differencing the time type/class.'''
        if self.paranoid: self.normalize()
        start = 0
        for t in self.timepoints:
            if t['type'] == 'start':
                start = t['time']
            else:
                duration = t['time'] - start
                if duration >= length:
                    return start
        return -1

    def trim_to_time(self, total_time):
        ''' Trims the intervals from the beginning, so they sum up to
        total_time. Alters the Intervals object itself, returns nothing.'''
        if self.paranoid: self.normalize()
        if not self.timepoints:
            return
        trimmed_tps = []
        sum_val     = 0
        # Here we have the same unavoidable problem as in get_total_time,
        # namely we need to start summing with the right type/class, so we 
        # have to check it explicitly.
        if self.timepoints[0]['type']=='start':
            start = self.timepoints[0]['time']
            if isinstance(start, datetime):
                sum_val = timedelta()
        else:
            raise IntervalsError()
        for t in self.timepoints: # redoing the first timepoint
            if t['type'] == 'start':
                start = t['time']
                trimmed_tps.append(t)
            else:
                sum_val = sum_val + (t['time'] - start)
                if sum_val > total_time:
                    trim_time = sum_val-total_time
                    trimmed_tps.append({'time':t['time']-trim_time, 'type':'end'})
                    self.timepoints = trimmed_tps
                    # no sort or norm required
                    return
                else:
                    trimmed_tps.append(t)
                if sum_val == total_time:
                    # no sort or norm required
                    self.timepoints = trimmed_tps
                    return
        if sum_val < total_time:
            raise IntervalsError('Requested to trim intervals to more than their total time')

    def remove_intervals_smaller_than(self, duration):
        ''' Filters out intervals that are smaller than a threshold'''
        if self.paranoid: self.normalize()
        toremove = []
        for tp in self.timepoints:
            if tp['type'] == 'start':
                previous = tp
            else:
                d = tp['time'] - previous['time']
                if d < duration:
                    toremove.append(previous)
                    toremove.append(tp)
        for tp in toremove:
            self.timepoints.remove(tp)
            # no sort or norm required

    def complement(self, absolute_start, absolute_end):
        ''' Turns a list of intervals denoting free times
        into a list denoting busy times and vice versa.
        Replaces self.timepoints and returns nothing.
        absolute_start and absolute_end must be defined, so we know
        how to close off the ends. '''
        if self.paranoid: self.normalize()
        if self.timepoints:
            # figure out the start
            if self.timepoints[0]['time'] == absolute_start:
                start = self.timepoints[1]['time']
                self.timepoints.pop(0)
                self.timepoints.pop(0)
            else:
                start = absolute_start
            complemented_tps = [{'time':start, 'type':'start'}]
            for t in self.timepoints:
                if t['type'] == 'start':
                    complemented_tps.append({'time':t['time'], 'type':'end'})
                else:
                    complemented_tps.append({'time':t['time'], 'type':'start'})
            if complemented_tps[-1]['type'] == 'start':
                if complemented_tps[-1]['time'] == absolute_end:
                    complemented_tps.pop()
                else:
                    complemented_tps.append({'time':absolute_end, 'type':'end'})
            # store complemented_timepoints
            self.timepoints = complemented_tps
            # no sort or norm required
        else:
            self.timepoints.append({'time':absolute_start, 'type':'start'})
            self.timepoints.append({'time':absolute_end, 'type':'end'})
            # no sort or norm required
        self.swap_label()

    def swap_label(self):
        ''' Utility function to toggle label free<->busy.'''
        # if the label is defined, swap it
        if self.label == 'free':
            self.label = 'busy'
        elif self.label == 'busy':
            self.label = 'free'

    def intersect(self, list_of_others):
        ''' Intersects Intervals in list_of_others with self. Returns
        a new Intervals object containing only those intervals that
        were in the intersection of everything. If the intersection
        was empty, it returns None.'''
        if self.paranoid: self.normalize()
        intersection = []
        merged_timepoints = list(self.timepoints)
        # merge all lists of timepoints
        for other in list_of_others:
            merged_timepoints.extend(other.timepoints)
        # sort the merged list
        Intervals.sort_timepoints(merged_timepoints)
        # walk through merged list popping up flags
        flag     = 0
        max_flag = len(list_of_others)+1
        # This loop requires a sorted list as input to work correctly
        for t in merged_timepoints:
            if t['type'] == 'start':
                if flag == max_flag:
                    intersection.append({'time':t['time'], 'type':'end'})
                flag += 1
                if flag == max_flag:
                    intersection.append({'time':t['time'], 'type':'start'})
            elif t['type'] == 'end':
                if flag == max_flag:
                    intersection.append({'time':t['time'], 'type':'end'})
                flag -= 1
                if flag == max_flag:
                    intersection.append({'time':t['time'], 'type':'start'})
        if intersection:
            return Intervals(intersection, self.label)
        else:
            return Intervals([])

    def subtract(self, other):
        ''' Returns a new Intervals object containing those intervals in self
        that are not in other (i.e. the relative complement of other in self).
        '''
        mykey = 'intervals_id'
        if self.paranoid: self.normalize()
        if (other == None) or other.is_empty() or self.is_empty():
            return self
        rc = []
        for t in other.timepoints:
            t[mykey]=1
        for t in self.timepoints:
            t[mykey]=2
        
        merged_timepoints = list(self.timepoints)
        # merge the two lists
        merged_timepoints.extend(other.timepoints)
        # sort the merged list
        Intervals.sort_timepoints(merged_timepoints)
        # walk through merged list popping up flags
        flag = 0
        for t in merged_timepoints:
            if t['type'] == 'start':
                if flag == 2:
                    rc.append({'time':t['time'], 'type':'end'})
                flag = flag + t[mykey]
                if flag == 2:
                    rc.append({'time':t['time'], 'type':'start'})
            elif t['type'] == 'end':
                if flag == 2:
                    rc.append({'time':t['time'], 'type':'end'})
                flag = flag - t[mykey]
                if flag == 2:
                    rc.append({'time':t['time'], 'type':'start'})
        # walk thru & clean id fields
        # TODO: make mykey a class parameter, in case of collision?
        for tp in merged_timepoints:
            if mykey in tp:
                del tp[mykey]
        # in case of label disagreement, use None
        label = None 
        if self.label == other.label:
            label = self.label
        return Intervals(rc, label)

