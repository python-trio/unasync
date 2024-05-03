#!/bin/bash

set -ex

BLACK_VERSION=24.4.2

python -m pip install -U pip setuptools wheel

python setup.py sdist --formats=zip
pip install dist/*.zip

if [ "$CHECK_FORMATTING" = "1" ]; then
    pip install black==${BLACK_VERSION} isort>=5
    if ! black --diff setup.py src tests; then
        cat <<EOF
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Formatting problems were found (listed above). To fix them, run

   pip install black==$BLACK_VERSION
   black setup.py src tests

in your local checkout.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
EOF
        exit 1
    fi

    # required for isort to order test imports correctly
    pip install -Ur test-requirements.txt

    if ! isort --check-only --diff . ; then
        cat <<EOF
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Formatting problems were found (listed above). To fix them, run

   pip install isort
   isort .

in your local checkout.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
EOF
        exit 1
    fi
    exit 0
fi

# Actual tests
pip install -Ur test-requirements.txt

pytest -W error -ra -v tests --cov --cov-config=.coveragerc --cov-fail-under=93
