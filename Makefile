build: clean
	python3 setup.py sdist bdist_wheel
.PHONY: build

clean:
	rm -rf *.egg-info build dist
.PHONY: clean

develop:
	python3 -m pip install .
	python3 -c "from flaskr import app; app.run('127.0.0.1');"
.PHONY: develop
