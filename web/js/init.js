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
    svg.load(function() {
      $(this).find('rect').hover(function() {
        var clsList = $(this).parent().attr('class'),
            cls;
        if(clsList.match('node_[0-9]+')) {
          cls = 'node_' + clsList.split('_')[1];
          svg.find('path.' + cls).each(function() {
            $(this).attr('class', $(this).attr('class') + ' highlight');
          });
        }
      }, function(e) {
        svg.find('.highlight').each(function() {
          $(this).attr('class', $(this).attr('class').replace(' highlight', ''));
        });
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
