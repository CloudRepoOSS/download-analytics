build: clean
	python3 setup.py sdist bdist_wheel
.PHONY: build

clean:
	rm -rf *.egg-info build dist
.PHONY: clean
