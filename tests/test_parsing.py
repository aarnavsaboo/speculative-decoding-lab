import unittest

from speculative_decoding_lab.parsing import parse_perf
from speculative_decoding_lab.pairing import pair_with_baseline


class Tests(unittest.TestCase):
    def test_parser_acceptance(self):
        out = parse_perf("drafted = 20, accepted = 15")
        self.assertEqual(out["drafted_tokens"], 20)
        self.assertEqual(out["accepted_tokens"], 15)
        self.assertEqual(out["acceptance_ratio"], .75)

    def test_pairing(self):
        common = {
            "pair_key": ["t", "p", 100, 0, 0.0],
            "target_model": "t",
            "prompt_file": "p",
            "repeat": 0,
            "temperature": 0.0,
            "ok": True,
        }
        rows = [
            {**common, "job_id": "b", "baseline": True, "elapsed_seconds": 10},
            {
                **common,
                "job_id": "s",
                "baseline": False,
                "elapsed_seconds": 5,
                "draft_model": "d",
                "spec_type": "draft-simple",
                "draft_n_max": 4,
            },
        ]
        out = pair_with_baseline(rows)
        self.assertEqual(out[0]["speedup"], 2)


if __name__ == "__main__":
    unittest.main()
