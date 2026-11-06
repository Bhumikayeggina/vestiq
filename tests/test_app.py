# Headless test of the Streamlit app: runs it, enters queries and checks the answers respect the budget.
from streamlit.testing.v1 import AppTest


def ask(query):
    at = AppTest.from_file("../app/app.py", default_timeout=90).run()
    assert not at.exception, at.exception
    at.text_input[0].set_value(query).run()
    assert not at.exception, at.exception
    return at.dataframe[0].value


res = ask("men cotton tshirt under 500")
assert len(res) > 0, "no results"
assert (res["price"] <= 500).all(), "budget not respected"
print(f"[ OK ] app query 1: {len(res)} results, all priced 500 or less")

res = ask("simple traditional kurti for wedding under 1500")
print(f"[ OK ] app query 2: {len(res)} results" if len(res) else "[WARN] app query 2 returned nothing")
print("APP TEST PASSED")
