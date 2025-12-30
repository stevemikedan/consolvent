.PHONY: v1-analysis v2-analysis all-analysis plots migrate

PYTHONPATH=.

migrate:
	python maintenance/migrate_logs.py

v1-analysis:
	python analysis/summarize_runs.py --validation v1

v2-analysis:
	python analysis/summarize_runs.py --validation v2

all-analysis:
	python analysis/summarize_runs.py --validation all

plots:
	python plots/plot_summary_panels.py --validation v1
	python plots/plot_summary_panels.py --validation v2

reify: migrate all-analysis plots
