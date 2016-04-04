// globals
var stored = null;
var operator = null;
var clearOperand = false;
var lastPressed = false;
var code = null;

// setup handlers
$(document).ready(function() {
  // clear greetings
  setTimeout( function() {
    doComment('Ok! let\'s do it!');
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
      // case 46:
      //   code = 'dac'
      //   break;
      case 127: // delete charCode
        code = 'dac'
        break;
      default:
        break;
    }
    pressButton(code);
    code = null
  });
});

// functions
function pressButton(button) {
  // execute operation
  // get input
  switch (button) {
    case 'ddot':
     if ($('#calcDisplay').text().indexOf('.') !== -1) {
       doComment('Enough dots...');
       break;
     }
     else {
       button = 'd.'
     }
    //key pressed a number
    case 'ds':
      $('#calcDisplay').text(-Number($('#calcDisplay').text()));
      break;
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
        doComment('Looking good!');
        $('#calcDisplay').text(number);
      }
      else if (number.replace('.', '').length < 7) {
        doComment('Dude! I\'m totally missing this one!');
        $('#calcDisplay').text(number);
      }
      else {
        doComment('Man! I\'m done! NO MORE DIGITS!');
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
  }
  // sanity check
  displayString = $('#calcDisplay').text();
  if (displayString.charAt(0) === '0' && displayString.length > 1 && displayString.charAt(1) !== '.') {
    $('#calcDisplay').text(displayString.slice(1));
  }
  lastPressed = true
}

function applyOperation(number1, number2, operator) {
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

function commitOperation() {
  if (stored !== null && operator !== null) {
    value = applyOperation(stored, $('#calcDisplay').text(), operator);
    $('#calcDisplay').text(value).
    operator = null;
    stored = null;
  }
}

function doComment(text) {
  $('#calcComment').text(text)
}
