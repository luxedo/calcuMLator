$(document).ready(function() {
  // buttons feedback
  $('.digit').mousedown(function() {
    $(this).css('opacity', '0.5');
  });
  $('.digit').mouseup(function() {
    $(this).css('opacity', '');
  })
  // buttons logic;
  $('.digit').click(function() {
    console.log(this.id);
  });
});
