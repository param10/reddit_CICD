import os
import sys
import reddit_ETL

# Add etl/ folder to sys.path after imports
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'etl'
    )
)


def test_run_etl_functionality():
    try:
        reddit_ETL.run_ETL()
    except Exception as e:
        assert False, f"ETL failed with error: {e}"
