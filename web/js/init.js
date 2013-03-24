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

    $('#content').on('click', function() {
      if($('.flipcontent').is(':visible')) {
        $('.flipcontent').slideUp('fast');
      }
    });

    $('#menu a.icon').hover(function() {
      var shorttip = $(this).closest('#menu').find('.shorttip');
      shorttip.find('.shorttip-tail').css('left', $(this).position().left + 6);
      if(shorttip.is(':visible')) {
        shorttip.hide();
      } else {
        shorttip.find('.shorttip-text').text($(this).data('shorttip'));
        shorttip.show();
      }
    });
  };

  $(document).ready(function() {
    if(!document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure", "1.1")) {
      $('.too-old').fadeIn('slow');
    } else {
      finance.draw();
      $('#chart').hide().fadeIn('slow');
      $('.loader').show().fadeOut('slow');
      finance.registerListeners();
    }
  });

}(jQuery));
