"""Régression du statut documentaire et de la correspondance des résultats."""
import hashlib
import json
import unittest

from academy_status import evidence_gaps


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.dumps({"extra": [
            {"script": "profil.py", "args": ["--audit"]},
            {"script": "profil.py", "args": ["--apply"]},
        ]}).encode()
        self.result = {"test": "script profil.py", "ok": True}

    def test_duplicate_label_requires_two_results(self):
        self.assertIn("1 résultat", evidence_gaps(self.spec, [self.result])[0])
        self.assertEqual(evidence_gaps(self.spec, [self.result, self.result]), [])

    def test_modified_specification_is_detected(self):
        old = {**self.result, "spec_sha256": "0" * 64}
        self.assertIn("spécification modifiée depuis les résultats", evidence_gaps(self.spec, [old, old]))
        fresh = {**self.result, "spec_sha256": hashlib.sha256(self.spec).hexdigest()}
        self.assertEqual(evidence_gaps(self.spec, [fresh, fresh]), [])

    def test_failure_does_not_count_as_validation(self):
        failed = {**self.result, "ok": False}
        self.assertIn("au moins un contrôle enregistré en échec",
                      evidence_gaps(self.spec, [self.result, failed]))


if __name__ == "__main__":
    unittest.main()
