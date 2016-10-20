function applyOperation(number1, number2, operator, estimator) {
  if (estimator === 'real') {
    return Number(eval(number1.concat(operator, number2)).toFixed(6)).toString();
  }
  let op_strings = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'};
  let path = '';
  console.log(window.hostname);
  if (window.hostname == 'http://armlessjohn404.github.io' ) {
     path = 'https://calcumlator.herokuapp.com';
  }
  let request = path+`/compute?n1=${number1}&n2=${number2}&op=${op_strings[operator]}&method=${estimator}`
  return new Promise((res, rej) => {$.getJSON(request).done((data => res(data.result.toFixed(6))));
  });
}
