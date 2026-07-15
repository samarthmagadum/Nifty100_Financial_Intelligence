load:
	python src/etl/loader.py

ratios:
	python src/analytics/ratios.py

test:
	pytest

dashboard:
	streamlit run app.py

api:
	uvicorn src.api.main:app --reload

clean:
	rm -rf __pycache__