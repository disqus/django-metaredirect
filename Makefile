lint:
	pip install --use-mirrors flake8
	flake8 ./metaredirect

clean:
	find . -name *.pyc -delete

test: clean
	python setup.py test

test-matrix: clean
	pip install --use-mirrors tox
	tox

publish: lint test-matrix
	git tag $$(python setup.py --version)
	git push --tags
	python setup.py sdist upload

.PHONY: clean lint test test-matrix publish
