# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Calendar minute operator class and public API function definitions."""

from temporian.core import operator_lib
from temporian.core.compilation import compile
from temporian.core.data.node import EventSetNode
from temporian.core.operators.calendar.base import BaseCalendarOperator
from temporian.core.typing import EventSetOrNode


class CalendarMinuteOperator(BaseCalendarOperator):
    @classmethod
    def operator_def_key(cls) -> str:
        return "CALENDAR_MINUTE"

    @classmethod
    def output_feature_name(cls) -> str:
        return "calendar_minute"


operator_lib.register_operator(CalendarMinuteOperator)


@compile
def calendar_minute(sampling: EventSetOrNode) -> EventSetOrNode:
    """Obtain the minute the timestamps in an
    [`EventSet`][temporian.EventSet]'s sampling are in.

    Features in `input` are ignored, only the timestamps are used and
    they must be unix timestamps (`is_unix_timestamp=True`).

    Output feature contains numbers between
    0 and 59.

    Usage example:
        ```python
        >>> from datetime import datetime
        >>> a = tp.event_set(
        ...    timestamps=[datetime(2020,1,1,18,30), datetime(2020,1,1,23,59)],
        ...    name='random_hours'
        ... )
        >>> b = tp.calendar_minute(a)
        >>> b
        indexes: ...
        features: [('calendar_minute', int32)]
        events:
            (2 events):
                timestamps: [...]
                'calendar_minute': [30 59]
        ...

        ```

    Args:
        sampling: EventSet to get the minutes from.

    Returns:
        EventSet with a single feature with the minute each timestamp in
        `sampling` belongs to.
    """
    assert isinstance(sampling, EventSetNode)

    return CalendarMinuteOperator(sampling).outputs["output"]
