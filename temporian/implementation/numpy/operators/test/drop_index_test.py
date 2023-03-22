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

from temporian.core.data.event import Event
from temporian.core.data.event import Feature
from temporian.core.data.sampling import Sampling
from temporian.core.operators.drop_index import DropIndexOperator
from temporian.implementation.numpy.data.event import NumpyEvent
from temporian.implementation.numpy.operators.drop_index import (
    DropIndexNumpyImplementation,
)


class DropIndexNumpyImplementationTest(absltest.TestCase):
    def setUp(self) -> None:
        # input event
        self.input_evt = Event(
            features=[Feature("sales", dtype=float)],
            sampling=Sampling(index=["store_id", "item_id"]),
        )
        # input NumPy event
        self.numpy_input_evt = NumpyEvent.from_dataframe(
            pd.DataFrame(
                [
                    [0, 1, 0.4, 10.0],
                    [0, 1, 0.5, 11.0],
                    [0, 1, 0.6, 12.0],
                    [0, 2, 0.1, 13.0],
                    [0, 2, 0.2, 14.0],
                    [1, 2, 0.3, 15.0],
                    [1, 2, 0.4, 16.0],
                    [1, 3, 0.3, 17.0],
                ],
                columns=["store_id", "item_id", "timestamp", "sales"],
            ),
            index_names=["store_id", "item_id"],
        )

    def test_drop_all(self) -> None:
        # output NumPy event
        expected_numpy_output_evt = NumpyEvent.from_dataframe(
            pd.DataFrame(
                [
                    [0, 2, 0.1, 13.0],
                    [0, 2, 0.2, 14.0],
                    [1, 2, 0.3, 15.0],
                    [1, 3, 0.3, 17.0],
                    [0, 1, 0.4, 10.0],
                    [1, 2, 0.4, 16.0],
                    [0, 1, 0.5, 11.0],
                    [0, 1, 0.6, 12.0],
                ],
                columns=["store_id", "item_id", "timestamp", "sales"],
            ),
            index_names=None,
        )
        # instance core operator
        operator = DropIndexOperator(self.input_evt)

        # instance operator implementation
        operator_impl = DropIndexNumpyImplementation(operator)

        # call operator
        op_numpy_output_evt = operator_impl(event=self.numpy_input_evt)["event"]

        # validate output
        self.assertEqual(op_numpy_output_evt, expected_numpy_output_evt)

    def test_drop_item(self) -> None:
        # output NumPy event. Need to do some re-ordering due to timestamp
        # collisions in sort
        expected_numpy_output_evt = NumpyEvent.from_dataframe(
            pd.DataFrame(
                [
                    [0, 2, 0.1, 13.0],
                    [0, 2, 0.2, 14.0],
                    [1, 2, 0.3, 15.0],
                    [1, 3, 0.3, 17.0],
                    [0, 1, 0.4, 10.0],
                    [1, 2, 0.4, 16.0],
                    [0, 1, 0.5, 11.0],
                    [0, 1, 0.6, 12.0],
                ],
                columns=["store_id", "item_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        # instance core operator
        operator = DropIndexOperator(self.input_evt, labels="item_id")

        # instance operator implementation
        operator_impl = DropIndexNumpyImplementation(operator)

        # call operator
        op_numpy_output_evt = operator_impl(event=self.numpy_input_evt)["event"]

        # validate output
        self.assertEqual(op_numpy_output_evt, expected_numpy_output_evt)

    def test_drop_store(self) -> None:
        # output NumPy event
        expected_numpy_output_evt = NumpyEvent.from_dataframe(
            pd.DataFrame(
                [
                    [0, 2, 0.1, 13.0],
                    [0, 2, 0.2, 14.0],
                    [1, 2, 0.3, 15.0],
                    [1, 3, 0.3, 17.0],
                    [0, 1, 0.4, 10.0],
                    [1, 2, 0.4, 16.0],
                    [0, 1, 0.5, 11.0],
                    [0, 1, 0.6, 12.0],
                ],
                columns=["store_id", "item_id", "timestamp", "sales"],
            ),
            index_names=["item_id"],
        )
        # instance core operator
        operator = DropIndexOperator(self.input_evt, labels="store_id")

        # instance operator implementation
        operator_impl = DropIndexNumpyImplementation(operator)

        # call operator
        op_numpy_output_evt = operator_impl(event=self.numpy_input_evt)["event"]

        # validate output
        self.assertEqual(op_numpy_output_evt, expected_numpy_output_evt)

    def test_drop_nothing(self) -> None:
        # output NumPy event
        expected_numpy_output_evt = NumpyEvent.from_dataframe(
            pd.DataFrame(
                [
                    [0, 2, 0.1, 13.0],
                    [0, 2, 0.2, 14.0],
                    [1, 2, 0.3, 15.0],
                    [1, 3, 0.3, 17.0],
                    [0, 1, 0.4, 10.0],
                    [1, 2, 0.4, 16.0],
                    [0, 1, 0.5, 11.0],
                    [0, 1, 0.6, 12.0],
                ],
                columns=["store_id", "item_id", "timestamp", "sales"],
            ),
            index_names=["store_id", "item_id"],
        )
        # instance core operator
        operator = DropIndexOperator(self.input_evt, labels=[])

        # instance operator implementation
        operator_impl = DropIndexNumpyImplementation(operator)

        # call operator
        op_numpy_output_evt = operator_impl(event=self.numpy_input_evt)["event"]

        # validate output
        self.assertEqual(op_numpy_output_evt, expected_numpy_output_evt)

    def test_bad_inputs(self) -> None:
        # single, non-existing label
        with self.assertRaisesRegex(KeyError, r"\['dept_id'\]"):
            operator = DropIndexOperator(self.input_evt, labels="dept_id")

        # one non-existing label
        with self.assertRaisesRegex(KeyError, r"\['dept_id'\]"):
            operator = DropIndexOperator(
                self.input_evt, labels=["store_id", "item_id", "dept_id"]
            )


if __name__ == "__main__":
    absltest.main()
