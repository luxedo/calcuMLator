var dataset = require('./dataset-stream.js');
var fit     = require('./fit-stream.js');

module.exports = {
  dataset: function (name, options) {
    name = name || 'digits';
    var path = name.split('.');
    var method = path[0];
    var field  = path[1];
    return dataset({
      module: 'datasets',
      method: method,
      field:  field,
      params: options
    });
  },
  svm: function (algorithm, options) {
    return fit({
      module: 'svm',
      method: algorithm,
      params: options
    });
  }
};

