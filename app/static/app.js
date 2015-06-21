var App = function() {
  var projectsEl = $('#projects');

  initProjects();
  initAffix();

  window.onresize = initAffix;

  // mark ios
  if (/(iPad|iPhone|iPod)/g.test(navigator.userAgent)) {
    document.body.dataset.os = 'ios';
  }

  function initProjects() {
    projectsEl
      .mixItUp({
        animation: {
          duration: 400,
          effects: 'fade translateZ(-360px) stagger(34ms)',
          easing: 'ease'
        }
      });
  }

  function initAffix() {
    $('#affix').affix({
      offset: {
        top: function () {
          return (this.top = $('header').outerHeight(true))
        }
      }
    })
  }

  var filter = function(name, forceFilter) {
    if (projectsEl.mixItUp('isMixing')) return;

    var state = projectsEl.mixItUp('getState');
    var currTag = $('[data-tag="'+state.activeFilter+'"]');
    var newTag = $('[data-tag="'+name+'"]');
    var toggleClassName = "active";

    if (state.activeFilter == name) {
      if (forceFilter) { return; }
      projectsEl.mixItUp('filter', 'all');
    } else {
      projectsEl.mixItUp('filter', name);
      currTag.toggleClass(toggleClassName);
    }
    newTag.toggleClass(toggleClassName);
  };

  return {
    filter: filter
  };
};

//Handlebars.registerHelper('color', function(str) {
//  return getMaterialColor(str);
//});
//
//Handlebars.registerHelper('rgb', function(str) {
//  var color = getMaterialColor(str);
//  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(color);
//  color = parseInt(result[1], 16)+','+parseInt(result[2], 16)+','+parseInt(result[3], 16);
//  return color;
//});
//
//// swaps errornous chars with '-'
//Handlebars.registerHelper('escape', function(str) {
//  if (str)
//    return str.replace(/:|;|\\|\//, '-');
//  return str;
//});
