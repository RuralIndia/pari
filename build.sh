run_functional_tests() {
	typeset arg1
	arg1=$1
	if [[ "$arg1" == "functional" ]]; then
		py.test
		exit $?
	fi
}

run_functional_tests $1

flake8 --exclude=migrations --ignore=E501,E225,E128,E126 .
python manage.py test pari