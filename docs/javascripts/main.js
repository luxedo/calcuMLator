// globals
let estimatorsPages = ['linear', 'ridge', 'lasso', 'elastic', 'bayesian',
                       'theil', 'PAR', 'SVR', 'bagging', 'dtree', 'gaussian', 'PLS',
                       'MLP', 'knnr', 'k_ridge', 'forest'];
let estimatorsNames = ['Linear regression', 'Ridge Regression', 'Lasso Regression',
                       'Elastic Net Regression', 'Bayesian Ridge Regression',
                       'Theil-Sen Regression', 'Passive Agressive Regression',
                       'Support Vector Regression', 'Bagging Regression',
                       'Decision Tree Regression', 'Gaussian Process Regression',
                       'Partial Least Squares Regression', 'Multi-layer Perceptron',
                       'K Nearest Neighbors Regression', 'Kernel Ridge Regression',
                       'Random Forest Regression'];

// add templates to head
estimatorsPages.forEach((value) => {
  var link = document.createElement('link');
  link.rel = 'import';
  link.id = `${value}-template`;
  link.href = `templates/${value}.html`
  document.head.appendChild(link);
});
// setup handlers
$(document).ready(function() {
  // Scroll behavior
  setBackground();
  $(window).scroll(setBackground);
  estimatorsPages.forEach((value, index) => {
    let element =
    `<li id="${value}-anchor">
      <p><a href="#${value}-anchor" onclick="toggleTemplate('${value}');">${estimatorsNames[index]}</a></p>
      <div id="${value}-estimator-content">
    </li>`
    $("#regressors-list").append(element)
    cloneTo(`${value}-template`, `${value}-estimator-content`);
  });
  hideTemplates();

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
    opacityVal = (s / 150.0);
    $('.blurred-bg').css('opacity', opacityVal);
}

function cloneTo(idSource, idDest) {
  var link = document.getElementById(idSource);
  var template = link.import.querySelector('template');
  var clone = document.importNode(template.content, true);
  document.getElementById(idDest).appendChild(clone)
}

function hideTemplates() {
  estimatorsPages.forEach((value) => {
    $(`#${value}-estimator-content`).hide();
  });
}
