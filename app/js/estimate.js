// dependencies
var childProcess = require('child_process');
var fs = require('fs');

// globals
var estimator_conf = JSON.parse(fs.readFileSync('../calcuMLator/estimator_conf.json'))
var estimators = estimator_conf['estimators']
estimators.unshift('real');

// overwrite applyOperation from main.js
function applyOperation(number1, number2, operator, brain) {
  if (estimators.indexOf(brain) !== -1 && brain != 'real') {
    command = '../calcuMLator/estimate.py';
    args = [number1, operator, number2, brain];
    calculation = childProcess.spawnSync(command, args);
    result = Number(calculation.stdout.toString());
    return  Number(result.toFixed(6)).toString();
  } else {
    return  Number(eval(number1.concat(operator, number2)).toFixed(6)).toString();
  }
}
