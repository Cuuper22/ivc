# Reproduce the checks and the deterministic research outputs.
#
#   python -m pip install -r requirements.txt
#   make check audit verify db      # a few minutes on a laptop, no network
#   make campaign                   # full 4-route rerun, long; rewrites files under research/campaigns/
#   make all                        # check audit verify db
#
# Set IVC_REPO_ROOT if you run the campaign scripts from outside the checkout.

PYTHON   ?= python3
NODE     ?= node
CAMPAIGN := research/campaigns/integrated_20260906
BUILD    ?= build

.PHONY: all check audit campaign verify db clean

all: check audit verify db

define CHECK_PY
import ast, pathlib, sys
skip = {"evidence", "build", "node_modules", ".git"}
files = [p for p in pathlib.Path(".").rglob("*.py") if not skip & set(p.parts)]
bad = 0
for p in files:
    try:
        ast.parse(p.read_bytes(), str(p))
    except SyntaxError as e:
        print("SYNTAX ERROR", p, e)
        bad += 1
print("python files parsed:", len(files), "errors:", bad)
sys.exit(1 if bad else 0)
endef
export CHECK_PY

# Syntax-check every Python file we own (ast.parse, writes no .pyc) and every site/db script.
check:
	@$(PYTHON) -c "$$CHECK_PY"
	@for f in docs/*.js db/*.mjs; do $(NODE) --check $$f || exit 1; done; echo "node --check ok: $$(ls docs/*.js db/*.mjs | wc -l) files"

# Mahadevan 1977 constraint audit (stdlib only). Output is byte-identical to research/data/mahadevan_20260905/.
audit:
	$(PYTHON) research/tools/mahadevan_constraint_audit.py \
	  --input research/data/mahadevan_20260905/concordance_documents.json.gz \
	  --output $(BUILD)/audit

# Full campaign rerun. Restores the packed payload files first. Rewrites tracked outputs in place.
campaign:
	$(PYTHON) $(CAMPAIGN)/restore_payload.py
	$(PYTHON) $(CAMPAIGN)/run_campaign.py --route all

# Verification stage of the reconstructed completion pass (restores payload automatically).
verify:
	$(PYTHON) $(CAMPAIGN)/completion/run_completion.py --stage verify

# Rebuild the SQLite database and audit report under build/. Does not touch db/ivc.sqlite. Needs Node >= 22.5.
db:
	$(NODE) --no-warnings db/build_db.mjs --db $(BUILD)/ivc.sqlite

clean:
	rm -rf $(BUILD)
