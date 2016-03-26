var spawn     = require('child_process').spawn;
var Transform = require('readable-stream').Transform;
var util      = require('util');

var stringify = require('streaming-json-stringify');

var predict = require('./predict-stream');

var Fit = function (options) {
  var self = this;
  Transform.call(this, { objectMode: true });
  self._options = options;
  self._isSpawned = false;

  self._model = new Buffer('');
};
util.inherits(Fit, Transform);

Fit.prototype.predict = function() {
  return predict({ model: this._model });
};

Fit.prototype._write = function (obj, _, done) {
  if (this._pyError) { return done(this._pyError); }
  var serialize = this._serialize;
  if (!this._isSpawned) {
    this._spawn();
    this._pipifyStdio();
    this._isSpawned = true;
    serialize = this._serialize;
    serialize.write(this._options.params, 'utf-8', function () {
      serialize.write(obj, 'utf-8', done);
    });
  } else {
    serialize.write(obj, 'utf-8', done);
  }
};

Fit.prototype._spawn = function() {
  var self = this;
  var args = [
    'scikit.py',
    '--module', this._options.module,
    '--method', this._options.method
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

Fit.prototype._pipifyStdio = function() {
  var self = this;

  self._pipifyStderr();
  self._pipifyStdout();
  self._pipifyStdin();

  //self._pyProcess.stdin.on('error', function (err) {
    //if (self._pyError.message) {
      //err.message = self._pyError.message + '\n' + err.message;
    //}
    //self._pyError = err;
  //});
  //self._pyProcess.stdout.on('readable', function () {});
};

Fit.prototype._pipifyStdout = function() {
  var self = this;
  self._pyProcess.stdout
    .on('readable', function () {
      var chunk;
      while ((chunk = this.read()) !== null) {
        self._model = Buffer.concat([self._model, chunk]);
      }
    })
    .on('end', function () {
      self.emit('model', self._model);
      // Needs for emiting 'end'
      self.read();
    });
};

Fit.prototype._pipifyStdin = function() {
  var serialize = this._serialize = stringify();
  serialize.open      = '';
  serialize.seperator = '\n';
  serialize.close     = '\n';
  serialize.pipe(this._pyProcess.stdin);
  this.once('finish', function onFinish () {
    serialize.end();
  });
};

Fit.prototype._pipifyStderr = function() {
  var self = this;
  self._pyProcess.stderr.setEncoding('utf8');
  self._pyProcess.stderr.on('data', function (data) {
    if (/^execvp\(\)/.test(data)) {
      self._pyError = new Error(' Failed to run python');
    } else {
      self._pyError = self._pyError || new Error();
      self._pyError.message += data;
      self.emit('error', self._pyError);
    }
  });
};

module.exports = function (options) {
  return new Fit(options);
};

