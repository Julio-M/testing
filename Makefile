
test-health:
	# make test
	@ source setup.sh ; health


run:
	# make run
	@ source setup.sh ; runLocally

cleanup:
	# make cleanup:
	@ echo "$(ccso)--> Cleaning up all auxiliary files $(ccend)"
	@ source setup.sh ; cleanup

format:
	#format code
	black *.py tests/*.py

lint:
	#flake8 or pylint disable R,C disables warnings recommended and configuration because they are too verbose for built purposes
	pylint --disable=R,C *.py

test:
	#test
	python3 -m pytest tests/test_*.py