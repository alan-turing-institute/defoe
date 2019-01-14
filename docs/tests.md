# Run unit tests

To run unit tests, run:

```bash
pytest defoe
```

You should see:

```
============================= test session starts ==============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /.../<REPOSITORY-DIRECTORY>, inifile

collected 17 items

defoe/test/books/test_archive.py ..                                        [ 11%]
defoe/test/books/test_book.py ........                                     [ 58%]
defoe/test/books/test_page.py .                                            [ 64%]
defoe/test/papers/test_article.py ..                                       [ 76%]
defoe/test/papers/test_issue.py ....                                       [100%]

========================== 17 passed in 8.62 seconds ===========================
```
