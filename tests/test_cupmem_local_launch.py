"""Local launcher contracts with tiny files and mocked processes; no model calls."""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import unittest
from unittest.mock import Mock, call, patch

from evaluation.cupmem.local_launch import (
    NoRedirect, local_env, server_command, stage_model, stop_child,
)


class LocalLaunchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.shared, self.local = self.root / "shared", self.root / "node-local"
        self.shared.mkdir()
        self.contents = {"config.json": b'{"model_type":"qwen3"}',
                         "model.safetensors": b"tiny deterministic fixture, not weights"}
        self.hashes = {name: hashlib.sha256(raw).hexdigest() for name, raw in self.contents.items()}
        self.config = dict(model_path=str(self.local), model_shared=str(self.shared),
                           model_repo="Qwen/Qwen3-8B", model_revision="a" * 40,
                           model_files_sha256=self.hashes.copy())
        for name, raw in self.contents.items():
            (self.shared / name).write_bytes(raw)
        self.ready = dict(repository=self.config["model_repo"], revision=self.config["model_revision"],
                          files_sha256=self.hashes)
        (self.shared / "READY.json").write_text(json.dumps(self.ready))
        self.env = patch.dict(os.environ, {"SLURM_JOB_ID": "12345"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_stage_exact_manifest_and_reverify_existing_local_bytes(self):
        self.assertEqual(stage_model(self.config), self.hashes)
        self.assertEqual({p.name for p in self.local.iterdir()}, set(self.contents))
        for name, raw in self.contents.items():
            self.assertEqual((self.local / name).read_bytes(), raw)
        with patch("evaluation.cupmem.local_launch.shutil.copyfile") as copy:
            self.assertEqual(stage_model(self.config), self.hashes)
            copy.assert_not_called()
        (self.local / "model.safetensors").write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "Existing local model hash mismatch"):
            stage_model(self.config)
        self.assertEqual((self.local / "model.safetensors").read_bytes(), b"tampered")

    def test_stage_rejects_shared_tamper_preserving_partial_copy(self):
        (self.shared / "config.json").write_bytes(b"changed upstream bytes")
        with self.assertRaisesRegex(ValueError, "staging hash mismatch"):
            stage_model(self.config)
        self.assertFalse((self.local / "config.json").exists())
        self.assertEqual((self.local / "config.json.stage-12345").read_bytes(), b"changed upstream bytes")

    def test_stage_rejects_changed_ready_revision_or_manifest(self):
        for field, value in [("revision", "b" * 40), ("repository", "another/model"),
                             ("files_sha256", {"other": "0" * 64})]:
            (self.shared / "READY.json").write_text(json.dumps({**self.ready, field: value}))
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "frozen revision/hashes"):
                stage_model(self.config)
        self.assertFalse(self.local.exists())

    def test_stage_unknown_loadable_file_refused_before_copy(self):
        self.local.mkdir()
        for suffix in (".json", ".py", ".jinja", ".safetensors", ".bin", ".model"):
            extra = self.local / ("unmanifested" + suffix)
            extra.write_text("untrusted extra")
            with self.subTest(suffix=suffix), self.assertRaisesRegex(ValueError, "Unmanifested loadable"):
                stage_model(self.config)
            self.assertFalse((self.local / "config.json").exists())
            self.assertEqual(extra.read_text(), "untrusted extra")
            extra.unlink()

    def test_stage_preserves_existing_partial_and_blocks_nested_manifest(self):
        self.local.mkdir()
        partial = self.local / "config.json.stage-12345"
        partial.write_text("earlier failed copy")
        with self.assertRaisesRegex(FileExistsError, "Partial stage already exists"):
            stage_model(self.config)
        self.assertEqual(partial.read_text(), "earlier failed copy")
        manifest = {"../outside.json": "0" * 64}
        self.config["model_files_sha256"] = manifest
        (self.shared / "READY.json").write_text(json.dumps({**self.ready, "files_sha256": manifest}))
        with self.assertRaisesRegex(ValueError, "flat filenames"):
            stage_model(self.config)
        self.assertFalse((self.root / "outside.json").exists())

    def test_command_pinned_long_context_non_thinking_compatible_flags(self):
        rope = dict(rope_type="yarn", factor=4.0, original_max_position_embeddings=32768)
        config = dict(model_path="/local_datasets/qwen3", actor="Qwen/Qwen3-8B",
                      base_url="http://127.0.0.1:8141/v1", max_model_len=131072,
                      serving=dict(tensor_parallel_size=2, max_num_seqs=1, gpu_memory_utilization=0.90,
                                   max_num_batched_tokens=4096, rope_scaling=rope, seed=314159))
        command = server_command(config)
        self.assertEqual(command[:3], [sys.executable, "-m", "vllm.entrypoints.openai.api_server"])
        expected = {"--model": config["model_path"], "--served-model-name": config["actor"],
                    "--host": "127.0.0.1", "--port": "8141", "--dtype": "bfloat16",
                    "--tensor-parallel-size": "2", "--distributed-executor-backend": "mp",
                    "--max-model-len": "131072", "--gpu-memory-utilization": "0.90",
                    "--max-num-seqs": "1", "--max-num-batched-tokens": "4096",
                    "--guided-decoding-backend": "xgrammar", "--generation-config": "vllm",
                    "--seed": "314159"}
        for flag, value in expected.items():
            self.assertEqual(command[command.index(flag) + 1], value)
        self.assertEqual(json.loads(command[command.index("--rope-scaling") + 1]), rope)
        self.assertIn("--enable-chunked-prefill", command)
        self.assertIn("--enforce-eager", command)
        self.assertNotIn("--enable-reasoning", command)
        self.assertNotIn("--reasoning-parser", command)
        self.assertNotIn("--quantization", command)
        for field, value in [("tensor_parallel_size", 1), ("max_num_seqs", 2),
                             ("gpu_memory_utilization", 0.95), ("max_num_batched_tokens", 8192)]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                server_command({**config, "serving": {**config["serving"], field: value}})

    def test_cleanup_signals_owned_group_even_after_parent_has_exited(self):
        process = Mock(pid=54321)
        process.poll.return_value = 1
        with patch("evaluation.cupmem.local_launch.os.killpg", side_effect=[None, ProcessLookupError]) as kill, \
             patch("evaluation.cupmem.local_launch.time.monotonic", side_effect=[0, 1]), \
             patch("evaluation.cupmem.local_launch.time.sleep") as sleep:
            result = stop_child(process)
        self.assertEqual(kill.call_args_list, [call(54321, signal.SIGTERM), call(54321, 0)])
        self.assertTrue(result["signal_sent"])
        self.assertEqual(result["errors"], [])
        process.wait.assert_called_once_with(timeout=10)
        sleep.assert_not_called()

    def test_cleanup_exit_race_and_absent_process_are_nonfatal(self):
        process = Mock(pid=54321)
        with patch("evaluation.cupmem.local_launch.os.killpg", side_effect=ProcessLookupError) as kill:
            result = stop_child(process)
        self.assertEqual(result, dict(signal_sent=False, errors=[]))
        kill.assert_called_once_with(54321, signal.SIGTERM)
        process.poll.assert_called_once()
        process.wait.assert_not_called()
        with patch("evaluation.cupmem.local_launch.os.killpg") as kill:
            self.assertEqual(stop_child(None), dict(signal_sent=False, errors=[]))
            kill.assert_not_called()

    def test_cleanup_fixed_deadline_forces_only_owned_group(self):
        process = Mock(pid=54321)
        with patch("evaluation.cupmem.local_launch.os.killpg") as kill, \
             patch("evaluation.cupmem.local_launch.time.monotonic", side_effect=[0, 21]), \
             patch("evaluation.cupmem.local_launch.time.sleep") as sleep:
            result = stop_child(process)
        self.assertEqual(kill.call_args_list, [call(54321, signal.SIGTERM), call(54321, signal.SIGKILL)])
        self.assertTrue(result["forced_group_kill"])
        self.assertEqual(result["errors"], [])
        process.wait.assert_called_once_with(timeout=10)
        sleep.assert_not_called()

    def test_cleanup_records_errors_without_masking_original_failure(self):
        process = Mock(pid=54321)
        with patch("evaluation.cupmem.local_launch.os.killpg", side_effect=PermissionError("fixture denial")):
            result = stop_child(process)
        self.assertEqual(result["errors"], [dict(type="PermissionError", message="fixture denial")])

    def test_child_environment_removes_hosted_credentials_and_readiness_no_redirect(self):
        source = dict(OPENAI_API_KEY="fake-test-only", BAZE_API_KEY="fake-test-only",
                      HF_TOKEN="fake-test-only", HUGGING_FACE_HUB_TOKEN="fake-test-only",
                      CUDA_VISIBLE_DEVICES="0,1", SLURM_JOB_ID="12345")
        with patch.dict(os.environ, source, clear=True):
            cleaned = local_env()
            self.assertEqual(dict(os.environ), source)
        self.assertTrue(all(name not in cleaned for name in source if name.endswith("KEY") or "TOKEN" in name))
        self.assertEqual(cleaned["CUDA_VISIBLE_DEVICES"], "0,1")
        self.assertEqual(cleaned["SLURM_JOB_ID"], "12345")
        self.assertEqual(cleaned["HF_HUB_DISABLE_IMPLICIT_TOKEN"], "1")
        with self.assertRaisesRegex(RuntimeError, "must not redirect"):
            NoRedirect().redirect_request(None, None, 302, "redirect", {}, "https://example.invalid")


if __name__ == "__main__":
    unittest.main()
