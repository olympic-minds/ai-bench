# ai-bench

Repository for storing AI benchmark problems.

```bash
source ./scripts/bootstrap
python3 eval.py ./tasks/assert-tasks/graph-task -h
```

To precompile headers use the following commands:

```bash
g++ -std=c++20 testlib/testlib.h
g++ -std=c++20 testlib/readwriter.h
```
