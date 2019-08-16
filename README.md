# Subscription system

A simple subscription system, wrote in django.

## To run project (with docker):

#### Dependencies needeed: docker

    $ git clone <repo_url>
    $ cd <project_dir>
    # Will setup the django webserver on http://0.0.0.0:8000
    $ docker-compose up 

    # To run the tests inside the container
    $ docker exec web bash
    $ pytest

## To run project (with local computer):

#### Dependencies needeed: python 3 and pipenv.

    $ git clone <repo_url>
    $ cd <project_dir>
    $ pipenv install
    $ pipenv shell

    # To start django webserver on http://127.0.0.1:8000
    $ cd src && ./manage.py runserver
    
    # To run the tests
    $ pytest

### To login, use the already available user: "admin" and password: "admin"

# MIT License

Copyright (c) [2019] [Nuno Diogo da Silva diogosilva.nuno@gmail.com]

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
