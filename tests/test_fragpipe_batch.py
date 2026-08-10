import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.search_engine import (
    build_manifest,
    generate_fp_search_result_fn,
    prepare_workflow,
    read_file_list,
)


class FragPipeBatchTests(unittest.TestCase):
    def test_one_column_file_list_becomes_batch_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            sample_a = root / "sample a.mzML"
            sample_b = root / "sample_b.mzML"
            sample_a.touch()
            sample_b.touch()
            file_list = root / "file_list.txt"
            file_list.write_text(
                f"# inputs\n{sample_a}\n{sample_b}\n", encoding="utf-8"
            )

            entries = read_file_list(file_list)
            manifest = build_manifest(entries, root / "results")

            self.assertEqual(len(entries), 2)
            self.assertEqual(
                manifest.read_text(encoding="utf-8").splitlines(),
                [
                    f"{sample_a}\texp\t\tDDA",
                    f"{sample_b}\texp\t\tDDA",
                ],
            )

    def test_official_four_column_manifest_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            sample = root / "sample.d"
            sample.mkdir()
            file_list = root / "file_list.tsv"
            file_list.write_text(
                f"{sample}\tcontrol\t2\tDDA\n", encoding="utf-8"
            )

            entries = read_file_list(file_list)

            self.assertEqual(entries[0].experiment, "control")
            self.assertEqual(entries[0].bioreplicate, "2")
            self.assertEqual(entries[0].data_type, "DDA")

    def test_workflow_copy_keeps_percolator_tsv_and_updates_database(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "default.workflow"
            destination = root / "run.workflow"
            source.write_text(
                "database.db-path=/old/db.fasta\n"
                "percolator.keep-tsv-files=false\n"
                "percolator.run-percolator=true\n",
                encoding="utf-8",
            )

            prepare_workflow(source, destination, root / "decoy.fasta")

            self.assertIn(
                f"database.db-path={root / 'decoy.fasta'}",
                destination.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "percolator.keep-tsv-files=true",
                destination.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "percolator.keep-tsv-files=false",
                source.read_text(encoding="utf-8"),
            )

    def test_fragpipe_search_reads_all_inputs_from_file_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            samples = [root / "sample_a.mzML", root / "sample_b.mzML"]
            for sample in samples:
                sample.touch()
            file_list = root / "file_list.txt"
            file_list.write_text(
                "\n".join(str(sample) for sample in samples) + "\n",
                encoding="utf-8",
            )
            workflow = root / "default.workflow"
            workflow.write_text("percolator.run-percolator=true\n", encoding="utf-8")
            fasta = root / "database.fasta"
            fasta.write_text(">P1\nPEPTIDE\n", encoding="utf-8")
            workdir = root / "results"
            observed_manifest_lines = []

            def fake_run_fragpipe(manifest_path, *args):
                observed_manifest_lines.extend(
                    Path(manifest_path).read_text(encoding="utf-8").splitlines()
                )
                result_dir = Path(args[1]) / "exp"
                result_dir.mkdir(parents=True)
                for sample in samples:
                    (result_dir / f"{sample.stem}_edited.pin").touch()

            with patch("scripts.search_engine.run_fragpipe", fake_run_fragpipe):
                state = generate_fp_search_result_fn(
                    {
                        "file_list": str(file_list),
                        "workdir": str(workdir),
                        "fasta_path": str(fasta),
                        "workflow_path": str(workflow),
                        "thread_num": 4,
                    }
                )

            self.assertEqual(state, 0)
            self.assertEqual(len(observed_manifest_lines), 2)


if __name__ == "__main__":
    unittest.main()
