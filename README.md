# FarmHash

My own implementation of Google's FarmHash. Atm only `hash32` is implemented. Implementation based on: https://github.com/google/farmhash. Using existing implementation of Google's FarmHash as a reference while testing: https://pypi.org/project/pyfarmhash/.

---

Setting up **virtualenv** (https://docs.python.org/3/library/venv.html):

1. `virtualenv venv`

2. `source venv/bin/activate`

3. `pip install -r requirements.txt`

---

To run tests use:

```shell
python main.py test
```

To run in interactive mode (enter custom message to hash) use:

```shell
python main.py
```
