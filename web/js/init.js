var finance = {};

(function($){
  finance.registerListeners = function() {
    $('.flipcontent').hide();
    $('.fliplink').click(function(e){
      current = $($(e.currentTarget).attr('href'));
      $('.flipcontent').not(current).slideUp('fast');
      current.slideToggle('fast');
      e.preventDefault();
    });

    // Note: add/toogle/removeClass does not work reliably on svg elements
    var svg = $('#chart svg');
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

    // svg.on('load', function() {$('.loader').hide();});

    $('#content').on('click', function() {
      if($('.flipcontent').is(':visible')) {
        $('.flipcontent').slideUp('fast');
      }
    });
  };

  $(document).ready(function() {
    finance.draw();
    // finance.data();
    $('#chart').hide().fadeIn('slow');
    $('.loader').fadeOut('slow');
    finance.registerListeners();
  });

}(jQuery));
