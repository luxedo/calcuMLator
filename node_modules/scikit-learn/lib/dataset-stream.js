var spawn    = require('child_process').spawn;
var Readable = require('readable-stream').Readable;
var Through  = require('stream').PassThrough;
var util     = require('util');

var JSONStream = require('JSONStream');

var Dataset = function (options) {
  Readable.call(this, { objectMode: true });
  this._options = options;
  this._isSpawned = false;
};
util.inherits(Dataset, Readable);

Dataset.prototype._read = function () {
  if (this._pyError) { return; }
  if (!this._isSpawned) {
    this._spawn();
    this._pipifyStdio();
    this._isSpawned = true;

    var params = JSON.stringify(this._options.params || {}) + '\n';
    this._pyProcess.stdin.write(params);
  }
};

Dataset.prototype._spawn = function() {
  var self = this;
  var args = [
    'scikit.py',
    '--module', self._options.module,
    '--method', self._options.method,
    '--field',  self._options.field
  ];
  self._pyProcess = spawn('python2', args, {
    cwd: __dirname,
    stdio: ['pipe', 'pipe', 'pipe']
  });
  self._pyProcess.on('error', function (err) {
    self._pyError = err;
    self.emit('error', err);
  });
  self._pyProcess.on('exit', function (code, signal) {
    var message;

    if (code) {
      var pyerr = self._pyError ? ('Python stderr:\n' + self._pyError) : '';
      message = 'Python crashed with code ' + code +
        ' and signal ' + signal + '\n' + pyerr;
      self._pyError = new Error(message);
      self.emit('error', self._pyError);
    }
  });
};

Dataset.prototype._pipifyStdio = function() {
  this._pipifyStderr();
  this._pipifyStdout();
};

Dataset.prototype._pipifyStdout = function() {
  var self = this;
  // TODO Read from stdout in pull fashion
  self._pyProcess.stdout
    .pipe(JSONStream.parse('*'))
    .pipe(new Through({ objectMode: true }))
    .on('readable', function () {
      var item;
      while ((item = this.read()) !== null) {
        self.push(item);
      }
    })
    .on('end', function () {
      self.push(null);
    });
};

Dataset.prototype._pipifyStderr = function() {
  var self = this;
  self._pyProcess.stderr.setEncoding('utf8');
  self._pyProcess.stderr.on('data', function (data) {
    if (/^execvp\(\)/.test(data)) {
      self._pyError = new Error(' Failed to run python');
    } else {
      self._pyError = self._pyError || new Error();
      self._pyError.message += data;
    }
  });
};

module.exports = function (options) {
  return new Dataset(options);
};

