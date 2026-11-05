"""Source/legacy-boundary checks; no model, network, or server is used."""
from copy import deepcopy
from hashlib import sha256
import json
import subprocess
import unittest

from evaluation.cupmem.legacy_inputs import (
    GIT, HERE, LEGACY, PEPS, ROOT, STORE, WORK, fingerprint, model_payload, reconstruct,
)
from evaluation.team_pilot.pilot import UPSTREAM, dev_sources
from team_memory.store import digest


class LegacyInputsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = HERE / "legacy-inputs.json"
        cls.data = json.loads(cls.path.read_text())
        cls.manifest = json.loads((HERE / "legacy-inputs-manifest.json").read_text())
        cls.legacy = json.loads(LEGACY.read_text())

    def test_full_reconstruction_replays_all_twenty_actual_legacy_outputs(self):
        required = [GIT, PEPS, STORE] + [WORK / name for name in self.manifest["source_file_sha256"]
                                       if not name.startswith("evidence-bounded-team-memory/")]
        if not all(path.exists() for path in required):
            self.skipTest("Full reconstruction requires the separately archived campaign inputs and upstream caches")
        rebuilt = reconstruct()
        self.assertEqual(rebuilt, self.data)
        self.assertEqual(set(self.legacy["rows"]), {c["id"] for c in self.data["cases"]})
        check = rebuilt["provenance"]["archived_replay"]
        self.assertEqual(check["historical_rows_identical"], 20)
        self.assertEqual(check["actual_reader_call_hashes_checked"], 50)
        self.assertEqual(check["inference_calls"], 0)

    def test_manifest_binds_generator_data_and_original_inputs(self):
        self.assertEqual(self.manifest["sha256"], sha256(self.path.read_bytes()).hexdigest())
        self.assertEqual(self.manifest["builder_sha256"], sha256((HERE / "legacy_inputs.py").read_bytes()).hexdigest())
        for name, expected in self.manifest["source_file_sha256"].items():
            if name.startswith("evidence-bounded-team-memory/"):
                path = ROOT / name.removeprefix("evidence-bounded-team-memory/")
                self.assertEqual(sha256(path.read_bytes()).hexdigest(), expected, name)

    def test_archived_campaign_inputs_match_manifest(self):
        archived = {name: expected for name, expected in self.manifest["source_file_sha256"].items()
                    if not name.startswith("evidence-bounded-team-memory/")}
        if not all((WORK / name).is_file() for name in archived):
            self.skipTest("Original campaign inputs are stored separately from the public repository")
        for name, expected in archived.items():
            self.assertEqual(sha256((WORK / name).read_bytes()).hexdigest(), expected, name)

    def test_gold_and_old_model_answers_cannot_cross_model_boundary(self):
        poisoned = deepcopy(self.data)
        poisoned["evaluation_only"] = {"answer": "DO_NOT_SEND_THIS_GOLD"}
        poisoned["provenance"] = {"prior_model_answer": "DO_NOT_SEND_THIS_GOLD"}
        for case in poisoned["cases"]:
            case["expected_answer"] = "DO_NOT_SEND_THIS_GOLD"
        for doc in poisoned["documents"].values():
            doc["gold_relation"] = "DO_NOT_SEND_THIS_GOLD"
            doc["source"]["selected_by_gold"] = "DO_NOT_SEND_THIS_GOLD"
        for case in self.data["cases"]:
            before = model_payload(self.data, case["id"], order="historical")
            after = model_payload(poisoned, case["id"], order="historical")
            self.assertEqual(before, after)
            self.assertEqual(set(after), {"question", "history", "as_of"})
            self.assertEqual(fingerprint(after), case["model_payload_sha256"]["historical"])
            self.assertNotIn("DO_NOT_SEND_THIS_GOLD", json.dumps(after))

    def test_all_528_natural_records_and_metadata_are_preserved(self):
        if not STORE.exists():
            self.skipTest("Original natural-QA cache is stored separately from the public repository")
        original = {sid: env for sid, (env, _) in dev_sources(STORE).items()}
        self.assertEqual(len(original), 528)
        for case in self.data["cases"]:
            if not case["id"].startswith("F_SH_"):
                continue
            records = model_payload(self.data, case["id"], order="historical")["history"]
            self.assertEqual([r["source_id"] for r in records], list(original))
            self.assertEqual({r["source_id"]: {k: v for k, v in r.items() if k != "source_id"}
                              for r in records}, original)

    def test_full_pep_scope_and_unfiltered_histories(self):
        peps = {sid: env for sid, env in self.data["documents"].items()
                if env["source"]["location"].startswith("https://github.com/python/peps/")}
        self.assertEqual(len(peps), 16)
        for sid, env in peps.items():
            self.assertEqual(sid, digest(env))
        counts = {c["id"]: len(model_payload(self.data, c["id"], order="historical")["history"])
                  for c in self.data["cases"]}
        self.assertEqual(counts["q04-ordinary/legacy"], 229)
        self.assertEqual(counts["d01/premise"], 230)
        self.assertEqual(counts["d07/premise"], 239)
        self.assertEqual(counts["pep-680/clean/candidate"], 16)
        self.assertEqual(counts["old-pep-572-conflict/premise"], 17)
        self.assertEqual(self.data["sizing"]["unique_histories"], 7)
        self.assertEqual(self.data["sizing"]["unique_source_prefix_states"]["historical"], 1015)

    def test_pep_sources_match_original_git_objects(self):
        if not PEPS.is_dir():
            self.skipTest("Original PEP Git cache is stored separately from the public repository")
        for env in self.data["documents"].values():
            if not env["source"]["location"].startswith("https://github.com/python/peps/"):
                continue
            path = env["source"]["location"].split(UPSTREAM + "/", 1)[1]
            raw = subprocess.check_output(["git", "--git-dir", str(PEPS), "show", UPSTREAM + ":" + path]).decode()
            self.assertEqual(env["source"]["text"], "\n".join(raw.splitlines()[:140]).strip())

    def test_legacy_citations_resolve_to_exact_raw_spans_and_both_sides_survive(self):
        for case in self.data["cases"]:
            records = {r["source_id"]: r for r in model_payload(self.data, case["id"], order="historical")["history"]}
            evaluation = self.data["evaluation_only"][case["id"]]
            for cited in evaluation["historical_citations"]:
                source = records[cited["source_id"]]["source"]
                self.assertEqual(source["text"][cited["start"]:cited["end"]], cited["quote"])
                self.assertEqual(source["location"], cited["location"])
        for case in ("d01/premise", "d07/premise", "old-pep-572-conflict/premise", "old-pep-618-conflict/premise"):
            self.assertEqual(len(self.data["evaluation_only"][case]["expected_sides"]), 2)
            self.assertEqual(len(self.data["evaluation_only"][case]["historical_citations"]), 2)
        # Native reference hits are contextual candidates for one natural answer.
        self.assertEqual(len(self.data["evaluation_only"]["F_SH_Top01_033/premise"]["expected_sides"]), 1)

    def test_no_implicit_chronology_variant(self):
        case = "F_SH_Top01_002/premise"
        with self.assertRaises(TypeError):
            model_payload(self.data, case)
        self.assertEqual(self.data["provenance"]["canonical_order"], "historical")
        a = model_payload(self.data, case, order="historical")
        b = model_payload(self.data, case, order="chronological")
        self.assertNotEqual(a["history"], b["history"])
        self.assertEqual({r["source_id"] for r in a["history"]}, {r["source_id"] for r in b["history"]})


if __name__ == "__main__":
    unittest.main()
