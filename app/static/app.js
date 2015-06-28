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
        },
        load: {
          sort: 'random'
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
