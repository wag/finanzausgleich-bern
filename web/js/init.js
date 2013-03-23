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

  $(document).ready(function() {
    finance.setup();
    finance.draw();
  });

}(jQuery));
