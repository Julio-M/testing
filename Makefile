default: help

.PHONY: help, run, cleanup, format, lint, test

test-health:
	# make test
	@ source setup.sh ; health

# Show this help.
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

run: # make run
	@ source setup.sh ; runLocally

cleanup: # make cleanup:
	@ echo "$(ccso)--> Cleaning up all auxiliary files $(ccend)"
	@ source setup.sh ; cleanup

format: # format code
	black *.py tests/*.py

lint: # pylint test
	pylint --disable=R,C *.py

test: # run tests for script
	python3 -m pytest tests/test_*.py