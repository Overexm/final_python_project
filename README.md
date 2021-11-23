# final_python_project


## Title
This is our final project from python.Here we have our login page for authorization and coin page for summarizing the coin datas.
```html
Done by: Orynbassar Merey, Kiyubayeva Kamila
Group:SE-2010
```

### Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#lisense)

---

## Installation

* ### Create a virtual environment:
```python $ virtualenv env```
* ### Activate a virtual environment:
For Windows:
```python env\Scripts\activate```

For Mac OS,Linux:
```python source env/bin/activate```

* ### Flask
```python $ pip install flask```

* ### SQLAlchemy
```python $ pip install SQLAlchemy ```

* ### pyjwt
```python $ pip install pyjwt ```

* ### BeautifulSoup
```python $ pip install beautifulsoup4```

* ### Tensorflow
```python $ pip install tensorflow ```

* ### Transformers
```python $ pip install transformers ```

* ### WTForms
```python $ pip install WTForms ```

* ### Flask-WTF
```python $ pip install Flask-WTF ```

* ### PostgreSQL Database [Download](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)



[Back To The Top](#final_python_project)

## Usage

```python
from flask import Flask, render_template, redirect 
from flask import request
from flask.json import jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import requests
from transformers import pipeline
```
[Back To The Top](#final_python_project)
## Examples
```html
Datas:
login:Merey password:123asd

Coin news:
Bitcoin: all data about bitcoin with summary
Ethereum: all data about ethereum with summary
```
[Back To The Top](#final_python_project)

## License

MIT License

Copyright (c) 2021 Overexm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back To The Top](#final_python_project)

