# time_intervals: A class for specifying and manipulating time intervals.

© 2017 Sotiria Lampoudi (slampoud@gmail.com)

**An interval is a contiguous section of time, defined by its start & end time. time_intervals allows you to construct these intervals and perform operations on them.**

Some of the possible operations include:

*   Set operations: intersection, union, difference
*   Informational: total time, empty checks, interval of length
*   Manipulation: trimming, addition

## Examples

Create two overlapping `Intervals`:

```python
from time_intervals.intervals import Intervals

time1 = Intervals([(datetime(2017, 1, 1), datetime(2017,2, 1))])
time2 = Intervals([(datetime(2017, 1, 15), datetime(2017,2, 28))])
```

Let's find the intersection:

```python
time1.intersect([time2])
>> {'timepoints': "[
        {'time': datetime.datetime(2017, 1, 15, 0, 0), 'type': 'start'},
        {'time': datetime.datetime(2017, 2, 1, 0, 0), 'type': 'end'}]",
    'label': 'None'}
```

We can also output the result as a list of tuples:

```python
time1.intersect([time2]).toTupleList()
>> [(datetime.datetime(2017, 1, 15, 0, 0), datetime.datetime(2017, 2, 1, 0, 0))]
```

We can perform union operations on an arbitrary number of `Intervals`:

```python
time3 = Intervals([(datetime(2017, 2, 28), datetime(2017, 3, 15))])
time1.union([time2, time3])
>>> [(datetime.datetime(2017, 1, 1, 0, 0), datetime.datetime(2017, 3, 15, 0, 0))]
```

Finding the total time of an interval is as simple as:

```python
time1.get_total_time()
>>> datetime.timedelta(31)
```

We can find the start of the first interval in a `Intervals` object that meets a minimum length criterion:

```python
two_intervals = Intervals([(datetime(2017, 1, 1), datetime(2017,1, 2)), (datetime(2017, 3, 1), datetime(2017, 3, 3))])
two_intervals.find_interval_of_length(timedelta(days=2))
>>> datetime.datetime(2017, 3, 1, 0, 0)
```

Intervals can be instantiated using different time classes/types. For example:

```python
[{'time': datetime.datetime(2016, 1, 1, 0, 0), 'type': 'start'},

{'time': datetime.datetime(2016, 1, 4, 0, 0), 'type': 'end'}]
```

or

```python
[{'time': 1506299116, 'type': 'start'},

{'time': 1506299119, 'type': 'end'}]
```
or

```python
[{'time': 2.3, 'type': 'start'}, {'time': 3.4, 'type': 'end'}]
```

## About

Each Intervals object holds from zero to many intervals, and permits their manipulation.

Intervals can be based on any time class/type that supports comparison, addition and subtraction (e.g. datetime or int). The times are used intact, without transforming them into an internal representation, so Intervals with different underlying time classes/types cannot be mixed.

Intervals can additionally have a label: busy or free. This can be useful in some situations, for example in developing scheduling code.

Below is a list of interface methods. There are more class and static methods than these, but we consider the rest to be utility methods.

Methods for getting information about Intervals (read-only):
* `is_empty`
* `get_total_time`
* `find_interval_of_length`

Methods for manipulating Intervals (write):
* `trim_to_time`
* `remove_intervals_smaller_than`
* `complement`: switch the labels (busy <-> free) of the intervals
* `add`: adds timepoints

Methods for working with multiple Intervals objects (produce new Intervals object):
* `intersect`: returns a new Intervals object that is the intersection of Self
with the arguments
* `union`: returns a new Intervals object that is the union of Self and arguments
* `subtract`: returns a new Intervals object that is those intervals in Self that are not in Other

The Intervals class makes a deep copy of the data passed to it during initialization. Once instantiated the Intervals object works in one of two modes: normal or paranoid. In normal mode the internal representation is "normalized" after every write-function (those are the functions in the second group above). Normalization includes sorting the timepoints, merging intervals that overlap or are adjacent, and checking for inconsistencies. In normal mode it is assumed that between write-function calls the internals of the object are read but not written to.
Paranoid mode is useful when that assumption may not be true. In paranoid mode, to guard against the possible disturbance of the ordered and consistent state of the object, the internals of the object are normalized before every operation, read or write, as well as at the end of write operations.
