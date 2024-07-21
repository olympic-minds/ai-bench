# ai-bench

Repository for benchmarking AI models on code-understanding problems.
Some example problems are in folder `tasks/assert-tasks`

To set up repository execute following commands:

```bash
source ./scripts/bootstrap
python3 eval.py -h
```

To precompile headers use the following commands:

```bash
g++ -std=c++20 testlib/testlib.h
g++ -std=c++20 testlib/readwriter.h
```
