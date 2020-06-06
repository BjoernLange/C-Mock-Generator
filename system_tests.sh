#!/bin/bash

echo "===== Executing system tests ====="

declare -a failed=()

for test in system_tests/*/; do
  echo "===== $test ====="
  cd "$test"
  make clean && make

  ret=$?
  if [ $ret -ne 0 ]; then
    failed+=("$test")
  fi
  cd ../..
done

if [ ${#failed[@]} -eq 0 ]; then
  echo "===== All tests passed! ====="
  exit 0
else
  echo "===== The following tests failed: ====="
  for test in "${failed[@]}"; do
    echo "$test"
  done
  exit 1
fi
