// Calculator base size
calcWidth = 25;
calcHeight = 30;
calcFont = 12;
calcIncreaseSize = 0.5; // increase 30% in size if on top

// setup handlers
$(document).ready(function() {
  // Scroll behavior
  setBackground();
  $(window).scroll(setBackground);
  $(`.estimator-content`).hide();
  $("a[href='#']").click(event => event.preventDefault());

  // smooth scroll behavior
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

function toggleTemplate(templateName) {
  $(`#${templateName}-estimator-content`).fadeToggle();
}

// functions
function setBackground() {
    let s = $(window).scrollTop(),
    opacityVal = (s / 300.0);
    sizeVal = 1-(2/(1+Math.exp(-s))-2)*calcIncreaseSize;
    $('.fade-bg').css('opacity', opacityVal);
    $('#calc').css('font-size', `${calcFont*sizeVal}pt`);
}
