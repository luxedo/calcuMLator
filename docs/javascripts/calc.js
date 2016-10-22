// globals
let stored = null;
let operator = null;
let clearOperand = false;
let lastPressed = false;
let code = null;
let estimator_index = 0;
let estimators = ['real', 'linear', 'ridge', 'lasso', 'elastic', 'bayesian', 'theil', 'PAR', 'SVR', 'bagging', 'dtree', 'gaussian', 'PLS', 'MLP', 'knnr', 'k_ridge', 'forest'];
let thinkLow = -9999;
let thinkHi = 9999;

// setup handlers
$(document).ready(function() {
  // put calc on page
  cloneTo('calc-template', 'calcGoesHere')
  // clear greetings
  setTimeout( function() {
    $('#calcDisplay').text('0');
  }, 1000)
  // buttons feedback
  $('.digit').mousedown(function() {
    $(this).css('opacity', '0.5');
  });
  $('.digit').mouseup(function() {
    $(this).css('opacity', '');
  });
  // buttons logic;
  $('.digit').click(function() {
    // clear greetings
    pressButton(this.id);
  });
  // add keyboard support
  addKeyboard();

  // check for CORS. Disables other modes if CORS is not avaliable
  //Detect browser support for CORS
  if ('withCredentials' in new XMLHttpRequest()) {
      /* supports cross-domain requests */
  }
  else if(typeof XDomainRequest !== "undefined"){
    //Use IE-specific "CORS" code with XDR
  }else{
    //Time to retreat with a fallback or polyfill
    estimators = ['real'];
    $('#calcTitle').append(" - not working");
  }
});

// functions
function pressButton(button) {
  // execute operation
  // get input
  switch (button) {
    case 'ds':
      $('#calcDisplay').text(-Number($('#calcDisplay').text()));
      break;
    case 'ddot':
     if ($('#calcDisplay').text().indexOf('.') !== -1) {
       break;
     }
     else {
       button = 'd.'
     }
    //key pressed a number
    case 'd0':
    case 'd1':
    case 'd2':
    case 'd3':
    case 'd4':
    case 'd5':
    case 'd6':
    case 'd7':
    case 'd8':
    case 'd9':
    case 'd.':
      lastPressed = false;
      // display and store
      if (clearOperand) {
        $('#calcDisplay').text('0');
        clearOperand = false;
      }
      number = $('#calcDisplay').text()+button.slice(1)
      if (number.length < 4) {
        $('#calcDisplay').text(number);
      }
      else if (number.replace('.', '').length < 7) {
        $('#calcDisplay').text(number);
      }
      break;
    // clear screen
    case 'dc':
      $('#calcDisplay').text('0');
    case 'dac':
      operator = null;
      stored = null;
      $('#calcDisplay').text('0');
      break;
    // operators
    case 'dadd':
      pressOperator('+');
      break;
    case 'dsub':
      pressOperator('-');
      break;
    case 'dmul':
      pressOperator('*');
      break;
    case 'ddiv':
      pressOperator('/');
      break;
    case 'deq':
      commitOperation();
      break;
    // change estimator
    case 'dtoggle':
      estimator_index = (estimator_index+1)%estimators.length;
      $('#dtoggle').text(estimators[estimator_index]);
      console.log();
      break;
  }
  // fix buggy display
  displayString = $('#calcDisplay').text();
  if (displayString.charAt(0) === '0' && displayString.length > 1 && displayString.charAt(1) !== '.') {
    $('#calcDisplay').text(displayString.slice(1));
  }
  lastPressed = true
}

function applyOperation(number1, number2, operator, estimator) {
  // estimator is useless for now
  return  Number(eval(number1.concat(operator, number2)).toFixed(6)).toString();
}

function pressOperator(new_op) {
  if (operator !== null && new_op !== operator && !lastPressed) {
    commitOperation()
  }
  operator = new_op
  stored = $('#calcDisplay').text();
  clearOperand = true;
}

function calcThinking() {
    return setInterval(() => {
      $('#calcDisplay').text((Math.random()*(thinkHi-thinkLow)+thinkLow).toPrecision(8));
  }, 200);
}

function commitOperation() {
  if (stored !== null && operator !== null) {
    value = applyOperation(stored, $('#calcDisplay').text(), operator, estimators[estimator_index]);
    let think = calcThinking();
    Promise.resolve(value).then((data) => {
      clearTimeout(think);
      $('#calcDisplay').text(data);
      operator = null;
      stored = null;
    });
  }
}

function addKeyboard() {
  $(document).keypress(function(e) {
    switch (e.which) {
      case '0'.charCodeAt(0):
      case '1'.charCodeAt(0):
      case '2'.charCodeAt(0):
      case '3'.charCodeAt(0):
      case '4'.charCodeAt(0):
      case '5'.charCodeAt(0):
      case '6'.charCodeAt(0):
      case '7'.charCodeAt(0):
      case '8'.charCodeAt(0):
      case '9'.charCodeAt(0):
        code = 'd'+String.fromCharCode(e.which)
        break;
     case '.'.charAt(0):
        code = 'ddot'
        break;
      case '+'.charCodeAt(0):
        code = 'dadd'
        break;
      case '-'.charCodeAt(0):
        code = 'dsub'
        break;
      case '*'.charCodeAt(0):
        code = 'dmul'
        break;
      case '/'.charCodeAt(0):
        code = 'ddiv'
        break;
      case 13: // enter charCode
        code = 'deq'
        break;
      case 127: // delete charCode
        code = 'dac'
        break;
      default:
        break;
    }
    pressButton(code);
    code = null
  });
}
