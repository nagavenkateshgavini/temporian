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

from absl.testing import absltest

import pandas as pd
import numpy as np
import math
from temporian.core.data.sampling import Sampling
from temporian.core.operators.sample import Sample
from temporian.implementation.numpy.operators.sample import (
    SampleNumpyImplementation,
)
from temporian.implementation.numpy.data.event import NumpyEvent, NumpyFeature
from temporian.implementation.numpy.data.sampling import NumpySampling
from temporian.core.data import event as event_lib
from temporian.core.data import feature as feature_lib
from temporian.core.data import dtype as dtype_lib
from temporian.implementation.numpy.evaluator import run_with_check


class SampleOperatorTest(absltest.TestCase):
    def setUp(self):
        pass

    def test_base(self):
        event_data = NumpyEvent.from_dataframe(
            pd.DataFrame(
                {
                    "timestamp": [1, 5, 8, 9, 1, 1],
                    "a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                    "b": [5, 6, 7, 8, 9, 10],
                    "c": ["A", "B", "C", "D", "E", "F"],
                    "x": [1, 1, 1, 1, 2, 2],
                }
            ),
            index_names=["x"],
        )
        event = event_data.schema()

        sampling_data = NumpyEvent.from_dataframe(
            pd.DataFrame(
                {
                    "timestamp": [-1, 1, 6, 10, 2, 2],
                    "x": [1, 1, 1, 1, 2, 2],
                }
            ),
            index_names=["x"],
        )
        sampling = sampling_data.schema()

        expected_output = NumpyEvent.from_dataframe(
            pd.DataFrame(
                {
                    "timestamp": [-1, 1, 6, 10, 2, 2],
                    "a": [math.nan, 1.0, 2.0, 4.0, 6.0, 6.0],
                    "b": [0, 5, 6, 8, 10, 10],
                    "c": ["", "A", "B", "D", "F", "F"],
                    "x": [1, 1, 1, 1, 2, 2],
                }
            ),
            index_names=["x"],
        )

        # Run op
        op = Sample(event=event, sampling=sampling)
        instance = SampleNumpyImplementation(op)
        output = run_with_check(
            op, instance, {"event": event_data, "sampling": sampling_data}
        )["event"]

        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    absltest.main()
