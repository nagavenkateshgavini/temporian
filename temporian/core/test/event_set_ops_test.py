from absl.testing import absltest
from temporian.core.data.node import EventSetNode
from temporian.implementation.numpy.data.event_set import EventSet

from temporian.implementation.numpy.data.io import event_set


class EventSetOpsTest(absltest.TestCase):
    """Tests that all expected operators are available and work on EventSet and
    EventSetNode and that they return the correct type."""

    def setUp(self):
        self.evset = event_set(
            timestamps=[0.1, 0.2, 0.3, 0.4, 0.5],
            features={
                "a": [1, 2, 3, 7, 8],
                "b": [4, 5, 6, 9, 10],
                "x": [1, 1, 1, 2, 2],
                "y": ["hello", "hello", "hello", "world", "world"],
            },
            indexes=["x", "y"],
        )
        self.other_evset = event_set(
            timestamps=[0.4, 0.5, 0.6, 0.7],
            features={
                "c": [11, 12, 13, 14],
                "x": [1, 1, 1, 2],
                "y": ["hello", "hello", "hello", "world"],
            },
            indexes=["x", "y"],
        )
        self.node = self.evset.node()
        self.other_node = self.other_evset.node()

    def test_add_index(self):
        self.assertTrue(isinstance(self.evset.add_index("a"), EventSet))
        self.assertTrue(isinstance(self.node.add_index("a"), EventSetNode))

    def test_begin(self):
        self.assertTrue(isinstance(self.evset.begin(), EventSet))
        self.assertTrue(isinstance(self.node.begin(), EventSetNode))

    def test_cast(self):
        self.assertTrue(isinstance(self.evset.cast({"a": float}), EventSet))
        self.assertTrue(isinstance(self.node.cast({"a": float}), EventSetNode))

    def test_drop_index(self):
        self.assertTrue(isinstance(self.evset.drop_index("x"), EventSet))
        self.assertTrue(isinstance(self.node.drop_index("x"), EventSetNode))

    def test_end(self):
        self.assertTrue(isinstance(self.evset.end(), EventSet))
        self.assertTrue(isinstance(self.node.end(), EventSetNode))

    def test_enumerate(self):
        self.assertTrue(isinstance(self.evset.enumerate(), EventSet))
        self.assertTrue(isinstance(self.node.enumerate(), EventSetNode))

    def test_filter(self):
        self.assertTrue(
            isinstance(self.evset.filter(self.evset["a"] > 3), EventSet)
        )
        self.assertTrue(
            isinstance(self.node.filter(self.node["a"] > 3), EventSetNode)
        )

    def test_join(self):
        self.assertTrue(isinstance(self.evset.join(self.other_evset), EventSet))
        self.assertTrue(
            isinstance(self.node.join(self.other_node), EventSetNode)
        )

    def test_lag(self):
        self.assertTrue(isinstance(self.evset.lag(3), EventSet))
        self.assertTrue(isinstance(self.node.lag(3), EventSetNode))

    def test_leak(self):
        self.assertTrue(isinstance(self.evset.leak(3), EventSet))
        self.assertTrue(isinstance(self.node.leak(3), EventSetNode))

    def test_prefix(self):
        self.assertTrue(isinstance(self.evset.prefix("a"), EventSet))
        self.assertTrue(isinstance(self.node.prefix("a"), EventSetNode))

    def test_propagate(self):
        self.assertTrue(
            isinstance(
                self.evset.drop_index("x").propagate(self.evset), EventSet
            )
        )
        self.assertTrue(
            isinstance(
                self.node.drop_index("x").propagate(self.node), EventSetNode
            )
        )

    def test_set_index(self):
        self.assertTrue(isinstance(self.evset.set_index("a"), EventSet))
        self.assertTrue(isinstance(self.node.set_index("a"), EventSetNode))


if __name__ == "__main__":
    absltest.main()
