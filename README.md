# ai-bench

Repository for storing AI benchmark problems.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
git submodule update --init --recursive
python3 eval.py ./tasks/assert-tasks/graph-task gpt 4 -t 3 -w 10 -v -p 1
```

To precompile headers use the following commands:

```bash
g++ -std=c++20 testlib/testlib.h
g++ -std=c++20 testlib/readwriter.h
```
