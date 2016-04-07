// var report = JSON.parse(fs.readFileSync('../calcuMLator/report.json'));
$.getJSON('../calcuMLator/report.json', function(data) {
  var items = [];
  $.each(data, function(key0, val0) {
    items.push('<tr><td><h4>'+key0+' regression</h4></td><td><h4>r<sup>2</sup> score</h4></td></tr>')
    $.each(val0, function(key1, val1) {
      items.push('<tr><td>'+key1+'</td><td>'+val1.toPrecision(2)+'</td></tr>')
    });
  });
  $('#main_content').append(items);
});
