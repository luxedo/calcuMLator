childProcess = require('child_process')
function applyOperation(number1, number2, operator) {
  // calculation = eval(number1.concat(operator, number2))
  command = 'calcuMLator/compute.py '+number1+' '+operator+' '+number2+' 2>/dev/null'
  calculation = Number(childProcess.execSync(command).toString());
  return  Number(calculation.toFixed(6)).toString();
}
