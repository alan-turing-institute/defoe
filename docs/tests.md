# Run unit tests

To run unit tests, run:

```bash
pytest lwm
```

You should see:

```
============================= test session starts ==============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /.../books-papers-code, inifile:
collected 17 items

lwm/test/books/test_archive.py ..                                        [ 11%]
lwm/test/books/test_book.py ........                                     [ 58%]
lwm/test/books/test_page.py .                                            [ 64%]
lwm/test/papers/test_article.py ..                                       [ 76%]
lwm/test/papers/test_issue.py ....                                       [100%]

========================== 17 passed in 8.62 seconds ===========================
```
