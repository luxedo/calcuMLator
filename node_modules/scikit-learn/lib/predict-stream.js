var spawn     = require('child_process').spawn;
var Transform = require('readable-stream').Transform;
var Through   = require('readable-stream').PassThrough;
var util      = require('util');

var stringify = require('streaming-json-stringify');
var JSONStream = require('JSONStream');

var Predict = function (options) {
  var self = this;
  Transform.call(this, { objectMode: true });
  self._options = options;
  self._isSpawned = false;
};
util.inherits(Predict, Transform);

Predict.prototype._transform = function (obj, _, done) {
  if (this._pyError) { return done(this._pyError); }
  var serialize = this._serialize;
  if (!this._isSpawned) {
    this._spawn();
    this._pipifyStdio();
    this._isSpawned = true;
    serialize = this._serialize;
    this._pyProcess.stdin.write(this._options.model, 'utf-8', function () {
      serialize.write(obj, 'utf-8', done);
    });
  } else {
    serialize.write(obj, 'utf-8', done);
  }
};

Predict.prototype._flush = function(done) {
  if (this._realyFinished) {
    done();
  } else {
    this.once('realyFinished', function () {
      done();
    });
  }
};

Predict.prototype._spawn = function() {
  var self = this;
  var args = [
    'scikit.py', '--predict'
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

Predict.prototype._pipifyStdio = function() {
  this._pipifyStderr();
  this._pipifyStdout();
  this._pipifyStdin();
};

Predict.prototype._pipifyStdout = function() {
  var self = this;
  self._pyProcess.stdout
    .pipe(JSONStream.parse('*'))
    // For compatibility with stream2
    .pipe(new Through({ objectMode: true }))
    .on('readable', function () {
      var label;
      while ((label = this.read()) !== null) {
        self.push(label);
      }
    })
    .on('end', function () {
      self._realyFinished = true;
      self.emit('realyFinished');
    });
};

Predict.prototype._pipifyStdin = function() {
  var serialize = this._serialize = stringify();
  serialize.open      = '\n\n';
  serialize.seperator = '\n';
  serialize.close     = '\n';
  serialize.pipe(this._pyProcess.stdin);
  this.on('finish', function () {
    serialize.end();
  });
};

Predict.prototype._pipifyStderr = function() {
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
  return new Predict(options);
};

