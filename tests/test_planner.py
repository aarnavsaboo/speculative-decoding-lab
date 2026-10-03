import unittest

from speculative_decoding_lab.planner import expand


class Tests(unittest.TestCase):
    def test_baselines_and_speculative_jobs(self):
        rows = expand({
            "target_models": ["t"],
            "draft_models": ["d"],
            "prompt_files": ["p"],
            "draft_n_max": [2, 4],
            "output_tokens": [64],
            "repeats": 2,
        })
        baseline = [x for x in rows if x.baseline]
        speculative = [x for x in rows if not x.baseline]
        self.assertEqual(len(baseline), 2)
        self.assertEqual(len(speculative), 4)
        self.assertEqual(len({x.id for x in rows}), 6)


if __name__ == "__main__":
    unittest.main()
