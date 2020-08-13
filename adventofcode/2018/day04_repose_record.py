"""
--- Day 4: Repose Record ---
You've sneaked into another supply closet - this time,
it's across from the prototype suit manufacturing lab.
You need to sneak inside and fix the issues with the suit,
but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help,
you discover that you're not the first person to want to sneak in.
Covering the walls, someone has spent an hour starting every midnight
for the past few months secretly observing this guard post!
They've been writing down the ID of the one guard on duty that night - the Elves seem to
have decided that one guard was enough for the overnight shift - as well as when they
fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records,
which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format.
The guard falling asleep or waking up is always the one whose shift most recently started.
Because all asleep/awake times are during the midnight hour (00:00 - 00:59),
only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day;
ID, which shows the guard on duty that day; and Minute,
which shows the minutes during which the guard was asleep within the midnight hour.
(The Minute column's header shows the minute's ten's digit in the first row
and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep,
and they count as awake on the minute they wake up.
For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time,
you might be able to trick that guard into working tonight
so you can have the best chance of sneaking in.
You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep.
What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5),
while Guard #99 only slept for a total of 30 minutes (10+10+10).
Guard #10 was asleep most during minute 24
(on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order,
your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose?
(In the above example, the answer would be 10 * 24 = 240.)
"""

import numpy as np
import re
from datetime import datetime as DT
from datetime import date as D
from unittest import TestCase as TC
from misc import run_testsuite
from typing import *  # noqa
from attr import attrs


@attrs(slots=True, auto_attribs=True)
class Record:
    datetime: DT
    body: str


@attrs(slots=True, auto_attribs=True)
class Shift:
    guard_id: int
    date: D
    sleep: Tuple[int, int]


@attrs(slots=True, auto_attribs=True)
class Guard:
    guard_id: int
    table: np.ndarray


def literal_parser(lit: str) -> Record:
    matched = re.search(r'\[(.+)\]\s(.+)', lit)
    datetime = DT.strptime(matched.group(1), '%Y-%m-%d %H:%M')
    body = matched.group(2)

    return Record(datetime=datetime, body=body)


def record_parser(sorted_records: Iterable[Record]) -> Iterable[Shift]:

    current_guard = -1
    fall_asleep = False
    start_sleep, end_sleep = None, None
    shifts = []
    for record in sorted_records:
        if not fall_asleep:
            if record.body.startswith('Guard'):
                current_guard = int(re.search(r'\d+', record.body).group(0))
            elif record.body.startswith('fall'):
                fall_asleep = True
                start_sleep = record.datetime.minute
            else:
                raise AssertionError(
                    'Only guard-shifting or falling-asleep are possible in awake state.'
                )
        else:
            if record.body.startswith('wake'):
                fall_asleep = False
                end_sleep = record.datetime.minute
                if end_sleep <= start_sleep:
                    raise ValueError(
                        f'Ended minute(got {end_sleep}) should be larger then started minute(got {start_sleep}).'
                    )
                shifts.append(
                    Shift(
                        guard_id=current_guard,
                        date=record.datetime.date(),
                        sleep=(start_sleep, end_sleep)))
            else:
                raise AssertionError(
                    'Only awaking is possible during fall-asleep state.')

    return shifts


def find_tired_gaurd(shifts: Iterable[Shift]) -> Guard:
    guards = {}
    for shift in shifts:
        s, e = shift.sleep
        if shift.guard_id not in guards:
            guards[shift.guard_id] = Guard(
                guard_id=shift.guard_id, table=np.zeros(60))

        guards[shift.guard_id].table[s:e] += 1.0

    tired_guard = sorted(guards.values(), key=lambda g: g.table.sum())[-1]

    return tired_guard


class Part01Test(TC):
    @property
    def lit_shifts(self):
        return [
            '[1518-11-01 00:00] Guard #10 begins shift',
            '[1518-11-01 00:05] falls asleep', '[1518-11-01 00:25] wakes up',
            '[1518-11-01 00:30] falls asleep', '[1518-11-01 00:55] wakes up',
            '[1518-11-01 23:58] Guard #99 begins shift',
            '[1518-11-02 00:40] falls asleep', '[1518-11-02 00:50] wakes up',
            '[1518-11-03 00:05] Guard #10 begins shift',
            '[1518-11-03 00:24] falls asleep', '[1518-11-03 00:29] wakes up',
            '[1518-11-04 00:02] Guard #99 begins shift',
            '[1518-11-04 00:36] falls asleep', '[1518-11-04 00:46] wakes up',
            '[1518-11-05 00:03] Guard #99 begins shift',
            '[1518-11-05 00:45] falls asleep', '[1518-11-05 00:55] wakes up'
        ]

    def test_literal_parser(self):
        expects = [
            Record(
                datetime=DT(1518, 11, 1, 0, 0), body='Guard #10 begins shift'),
            Record(datetime=DT(1518, 11, 1, 0, 5), body='falls asleep'),
            Record(datetime=DT(1518, 11, 1, 0, 25), body='wakes up'),
        ]

        for lit, exp in zip(self.lit_shifts[:3], expects):
            self.assertEqual(literal_parser(lit), exp)

    def test_record_parser(self):
        expects = [
            Shift(10, date=D(1518, 11, 1), sleep=(5, 25)),
            Shift(10, date=D(1518, 11, 1), sleep=(30, 55)),
            Shift(99, date=D(1518, 11, 2), sleep=(40, 50)),
            Shift(10, date=D(1518, 11, 3), sleep=(24, 29)),
            Shift(99, date=D(1518, 11, 4), sleep=(36, 46)),
            Shift(99, date=D(1518, 11, 5), sleep=(45, 55)),
        ]

        records = [literal_parser(lit) for lit in self.lit_shifts]

        for shift, exp in zip(record_parser(records), expects):
            self.assertEqual(shift, exp)

    def test_find_tired_gaurd(self):

        records = [literal_parser(lit) for lit in self.lit_shifts]

        tired_guard: Guard = find_tired_gaurd(record_parser(records))
        tired_minute = tired_guard.table.argmax()

        self.assertEqual(tired_guard.guard_id, 10)
        self.assertEqual(int(tired_guard.guard_id * tired_minute), 240)


def part01(path: str):

    run_testsuite(Part01Test)

    with open(path, 'r') as f:
        records = [literal_parser(lit) for lit in f]

    sorted_records = sorted(records, key=lambda r: r.datetime)

    tired_guard: Guard = find_tired_gaurd(record_parser(sorted_records))
    tired_minute = tired_guard.table.argmax()

    print('- Part01 Answer:', int(tired_guard.guard_id * tired_minute))


"""
--- Part Two ---
Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than
any other guard or minute - three times in total. (In all other cases,
any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose?
(In the above example, the answer would be 99 * 45 = 4455.)
"""


def find_tired_gaurd2(shifts: Iterable[Shift]) -> Guard:
    guards = {}
    for shift in shifts:
        s, e = shift.sleep
        if shift.guard_id not in guards:
            guards[shift.guard_id] = Guard(
                guard_id=shift.guard_id, table=np.zeros(60))

        guards[shift.guard_id].table[s:e] += 1.0

    tired_guard = sorted(guards.values(), key=lambda g: g.table.max())[-1]

    return tired_guard


class Part02Test(TC):
    @property
    def lit_shifts(self):
        return [
            '[1518-11-01 00:00] Guard #10 begins shift',
            '[1518-11-01 00:05] falls asleep', '[1518-11-01 00:25] wakes up',
            '[1518-11-01 00:30] falls asleep', '[1518-11-01 00:55] wakes up',
            '[1518-11-01 23:58] Guard #99 begins shift',
            '[1518-11-02 00:40] falls asleep', '[1518-11-02 00:50] wakes up',
            '[1518-11-03 00:05] Guard #10 begins shift',
            '[1518-11-03 00:24] falls asleep', '[1518-11-03 00:29] wakes up',
            '[1518-11-04 00:02] Guard #99 begins shift',
            '[1518-11-04 00:36] falls asleep', '[1518-11-04 00:46] wakes up',
            '[1518-11-05 00:03] Guard #99 begins shift',
            '[1518-11-05 00:45] falls asleep', '[1518-11-05 00:55] wakes up'
        ]

    def test_find_tired_gaurd2(self):

        records = [literal_parser(lit) for lit in self.lit_shifts]

        tired_guard: Guard = find_tired_gaurd2(record_parser(records))
        tired_minute = tired_guard.table.argmax()

        self.assertEqual(tired_guard.guard_id, 99)
        self.assertEqual(int(tired_guard.guard_id * tired_minute), 4455)


def part02(path: str):

    run_testsuite(Part02Test)

    with open(path, 'r') as f:
        records = [literal_parser(lit) for lit in f]

    sorted_records = sorted(records, key=lambda r: r.datetime)

    tired_guard: Guard = find_tired_gaurd2(record_parser(sorted_records))
    tired_minute = tired_guard.table.argmax()

    print('- Part02 Answer:', int(tired_guard.guard_id * tired_minute))


if __name__ == "__main__":
    part01('day04_input.txt')  # 118599
    part02('day04_input.txt')  # 33949