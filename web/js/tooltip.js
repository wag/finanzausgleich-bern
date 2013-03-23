// Based on https://github.com/tpreusse/open-budget/blob/master/scripts/tooltip.js
finance.tooltip = function(target) {
    var tip = $('<div id="tooltip"></div>').html('<div></div>').hide().appendTo($('body'));
    var tipInner = tip.find('div');

    $(document).mousemove(function(e){
        var width = e.pageX + tip.width() > $(window).width() ? - tip.width() - 15 : 15;
        tip.css({
            'top': e.pageY,
            'left': e.pageX + width
        });
    });

    target.bind('mouseover', function(){
        tipInner.html( $(this).data('tooltip') );
        tip.show();
    });
    target.bind('mouseout', function(){
        tip.hide();
    });
};
