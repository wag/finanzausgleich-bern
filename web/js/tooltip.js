// Inspired by https://github.com/tpreusse/open-budget/blob/master/scripts/tooltip.js
finance.tooltip = function(target) {
    var container = $('#chart'),
        tip = $('<div style="display:none" class="tooltip"></div>').appendTo(container);

    container.on('mousemove', function(e) {
        // Use pure javascript to improve performance
        e.preventDefault();
        if(tip[0].style.display != 'none') {
            var width = e.pageX + tip[0].offsetWidth > window.innerWidth ?
                -10 - tip[0].offsetWidth : 20;
            tip[0].style.top =  e.pageY - 30 + 'px';
            tip[0].style.left = e.pageX + width + 'px';
        }
    });

    target.hover(function() {
        tip.html($(this).data('tooltip'));
        tip.show();
    }, function() {
        tip.hide();
    });
};