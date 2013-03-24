var finance = {};

(function($){
  finance.setup = function() {
    $('.flipcontent').hide();
    $('.fliplink').click(function(evt){
      current = $($(evt.currentTarget).attr('href'));
      $('.flipcontent').not(current).slideUp();
      current.slideToggle();
      evt.preventDefault();
    });
  };

  finance.registerListeners = function(svg) {
    // Note: add/toogle/removeClass does not work reliably on svg elements
    svg.on('mouseenter', 'rect', function() {
      var clsList = $(this).parent().attr('class');
      if(clsList.match('node_[0-9]+')) {
        svg.find('path.' + 'node_' + clsList.split('_')[1]).each(function() {
          $(this).attr('class', $(this).attr('class') + ' highlight');
        });
      }
    });
    svg.on('mouseleave', 'rect', function() {
      svg.find('.highlight').each(function() {
        $(this).attr('class', $(this).attr('class').replace(' highlight', ''));
      });
    });
  };

  $(document).ready(function() {
    finance.setup();
    finance.draw();
    // finance.data();

    finance.registerListeners($('#chart svg'));
  });

}(jQuery));
