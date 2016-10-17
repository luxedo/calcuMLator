function applyOperation(number1, number2, operator, estimator) {
  if (estimator === 'real') {
    return Number(eval(number1.concat(operator, number2)).toFixed(6)).toString();
  }

  let op_strings = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'};
  return new Promise((res, rej) => {
    $.getJSON(`/compute?n1=${number1}&n2=${number2}&op=${op_strings[operator]}&method=${estimator}`)
      .done((data => res(data.result.toFixed(6))));
  });
}
