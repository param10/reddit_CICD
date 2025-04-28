import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

import reddit_ETL


def test_run_etl_functionality():
    try:
        reddit_ETL.run_ETL()
    except Exception as e:
        assert False, f"ETL failed with error: {e}"
