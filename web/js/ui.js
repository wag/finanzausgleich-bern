(function($){
    $('#about-content').hide();
    $('#about a:first').click(function(evt){
        $($(evt.currentTarget).attr('href')).slideToggle();
        evt.preventDefault();
    });
}(jQuery));
