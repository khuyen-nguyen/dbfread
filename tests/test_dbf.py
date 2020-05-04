# -*- coding: utf-8 -*-

from pathlib import Path
from dbfread import DBF

TESTCASE_PATH = Path(__file__).parent.parent / "testcases"

class TestDBF:
    """Validate the DBF interface"""

    def check_alice_bob(self, alice, bob):
        """Make sure Alice and Bob are accurate."""
        assert alice["NAME"] == "Alice"
        assert alice["BIRTHDATE"].year == 1987
        assert alice["BIRTHDATE"].month == 3
        assert alice["BIRTHDATE"].day == 1

        assert bob["NAME"] == "Bob"
        assert bob["BIRTHDATE"].year == 1980
        assert bob["BIRTHDATE"].month == 11
        assert bob["BIRTHDATE"].day == 12

    def test_classic_open(self):
        """Make sure the classic interface works."""
        memotest = str(TESTCASE_PATH / "memotest.dbf")
        alice, bob = list(DBF(memotest))

        self.check_alice_bob(alice, bob)

        assert alice["MEMO"] == "Alice memo"
        assert bob["MEMO"] == "Bob memo"

    def test_classic_open_memoless(self):
        """Make sure the classic interface works without a memofile."""
        memoless = str(TESTCASE_PATH / "no_memofile.dbf")
        alice, bob = list(DBF(memoless, ignore_missing_memofile=True))
        self.check_alice_bob(alice, bob)

        assert alice["MEMO"] is None
        assert bob["MEMO"] is None

    def test_file_object_open(self):
        """Make sure we can open by passing file objects."""
        memotest = TESTCASE_PATH / "memotest.dbf"
        memomemo = TESTCASE_PATH / "memotest.FPT"

        with memotest.open("rb") as mt:
            with memomemo.open("rb") as mm:
                data = DBF.from_file_object(mt, mm)

        assert data.__class__ is DBF

        dataset = list(data)
        self.check_alice_bob(dataset[0], dataset[1]) 
