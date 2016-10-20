# CalcuMLator

`CalcuMLator` is a calculator that utilizes <b>Machine Learning</b> to predict the values.

![calculator](docs/images/calculatorv2.png "calculator")

#### Check if it's online [here](https://calcumlator.herokuapp.com/) or [here](http://armlessjohn404.github.io/calcuMLator/)

I'm hosting the backend of the project at [heroku](https://www.heroku.com/
) with a free plan. It may take a little to fire up the servers there. The page contains more information about the calculator.

If you wish to run the project locally, clone the repository and install the dependencies. Then you can start a web server with [gunicorn](http://gunicorn.org/). If you don't want to install the dependencies globally, try running inside a [virtualenv](https://virtualenv.pypa.io/en/stable/)
```bash
$ git clone https://github.com/ArmlessJohn404/calcuMLator.git
$ cd calcuMLator
$ pip install -r requirements.txt
$ gunicorn server:app
```

Thanks to `Rafael Hamasaki` for the help with the UI.
