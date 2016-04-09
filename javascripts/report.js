// Add scores
$.getJSON('../calcuMLator/report.json', function(data) {
  var items = [];
  $.each(data, function(key0, val0) {
    items.push('<tr><td><h4>'+key0+' regression</h4></td><td><h4>r<sup>2</sup> score Train</h4></td><td><h4>r<sup>2</sup> score Test</h4></td></tr>')
    $.each(val0, function(key1, val1) {
      items.push('<tr><td>'+key1+'</td><td>'+val1[0].toPrecision(2)+'</td><td>'+val1[1].toPrecision(2)+'</td></tr>')
    });
  });
  $('#results_table').append(items);
});
// Add coefficients
$.getJSON('../calcuMLator/coef.json', function(data) {
  var items = [];
  $.each(data, function(key0, val0) {
    items.push('<tr><td><h4>'+key0+' regression</h4></td><td><h4>Coefficients</h4></td></tr>')
    $.each(val0, function(key1, val1) {
      $.each(val1, function(key2, val2) {
        if (val2.constructor === Array) {
          val2 = (val2.map(function(obj) {
            return obj.toPrecision(2);
          }));
          items.push('<tr><td>'+key1+'_'+key2+'</td><td>'+val2+'</td></tr>');
        } else {
          items.push('<tr><td>'+key1+'_'+key2+'</td><td>'+val2.toPrecision(3)+'</td></tr>');
        }
      });
      items.push('<tr><td></td></tr>');
    });
  });
  $('#coefficients_table').append(items);
});
