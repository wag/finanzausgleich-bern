var utils = {};

(function($){
    // Inspired by https://github.com/tpreusse/open-budget/blob/master/scripts/tooltip.js
    utils.tooltip = function(target) {
        var container = $('#chart'),
            tip = $('<div style="display:none" class="tooltip"></div>').appendTo(container);

        container.on('mousemove', function(e) {
            // Use pure javascript to improve performance
            e.preventDefault();
            if(tip[0].style.display !== 'none') {
                var width = e.pageX + tip[0].offsetWidth > window.innerWidth ?
                    -10 - tip[0].offsetWidth : 20;
                var height = e.pageY + tip[0].offsetHeight + 20 > window.innerHeight ?
                    70 + tip[0].offsetHeight : 40;
                tip[0].style.left = e.pageX + width + 'px';
                tip[0].style.top = e.pageY - height + 'px';
            }
        });

        target.hover(function() {
            tip.html($(this).data('tooltip'));
            tip.show();
        }, function() {
            tip.hide();
        });
    };
}(jQuery));