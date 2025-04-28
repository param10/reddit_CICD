import run_ETL

def test_run_etl_functionality():
    try:
        run_ETL.run_ETL()
    except Exception as e:
        assert False, f"ETL failed with error: {e}"
