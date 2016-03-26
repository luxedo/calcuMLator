# scikit-learn

Node.js wrapper of scikit-learn

## Installation

`npm install scikit-learn`

## Usage

`var scikit = require('scikit-learn')`

## Example

```js
var inspect = require('inspect-stream');

var arrayify = require('arrayify-merge.s');
var slice    = require('slice-flow.s');

var scikit = require('scikit-learn');

var features = scikit.dataset('load_digits.data'); //stream of features
var labels   = scikit.dataset('load_digits.target'); //stream of labels

// arrayify is transform stream that turns two input streams
// into one stream by wraping packets of inputs in array.
// So trainingSet outputs arrays [<feature>, <label>]
var trainingSet = arrayify();
features.pipe(trainingSet);
labels.pipe(trainingSet);

var clf = scikit.svm('SVC', {
  gamma: 0.001,
  C:     100
});

trainingSet
  .pipe(slice([0, -1])) //passes all packets except last one
  .pipe(clf)
  .on('error', function (err) {
    console.log(err);
  })
  .on('end', function () {
    // now we have trained model

    var predict = clf.predict();
    var features = scikit.dataset('load_digits.data');
    features.pipe(slice(-1)) //passes only last packet
      .pipe(predict)
      .pipe(inspect());
  });
```

## API

### scikit.dataset(name, options)

* name `String` Name of method of `sklearn.datasets` on python side
                concatenated by dot with name of dataset's subset
                Ex: 'load_digits.target'
* options `Object` Options of method

Returns readable stream of dataset

### Fit streams

All fit streams are transform streams that acts like writable.
So you must listen on `end` event instead of `finish`
to be sure that training finished

Accepts flow of arrays like [features, label]
where 'features' is array of features and label is... label

Also fit stream have event 'model' that emits with trained model.
Model is `Buffer` containing pickled object

Fit stream have method `predict` that returns Predict stream

#### scikit.svm(name, options)

* name `String` Name of method of `sklearn.svm` 
* options `Object` Options for estimator

### Predict streams

Predict stream is transform stream that accepts flow of arrays of features
and outputs predictions
