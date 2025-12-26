jQuery(function ($) {

    //Slider
    $(document).ready(function () {
        var time = 7; // time in seconds

        var $progressBar,
	      $bar,
	      $elem,
	      isPause,
	      tick,
	      percentTime;

        //Init the carousel
        try{
            $("#HSlider").find('.owl-carousel').owlCarousel({
				slideSpeed: 500,
				paginationSpeed: 500,
				dots: false,
                pagination:false,
                singleItem: true,
                navigation: true,
                navigationText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
                ],
                afterInit: progressBar,
                afterMove: moved,
                startDragging: pauseOnDragging,
                //autoHeight : true,
                transitionStyle: "fade" /*Transitions : fade, fadeUp, backSlide, goDown*/
            });
        }
        catch (err) {
        }
        //Init progressBar where elem is $("#owl-demo")
        function progressBar(elem) {
            $elem = elem;
            //build progress bar elements
            buildProgressBar();
            //start counting
            start();
        }

        //create div#progressBar and div#bar then append to $(".owl-carousel")
        function buildProgressBar() {
            $progressBar = $("<div>", {
                id: "progressBar"
            });
            $bar = $("<div>", {
                id: "bar"
            });
            $progressBar.append($bar).appendTo($elem);
        }

        function start() {
            //reset timer
            percentTime = 0;
            isPause = false;
            //run interval every 0.01 second
            tick = setInterval(interval, 10);
        };

        function interval() {
            if (isPause === false) {
                percentTime += 1 / time;
                $bar.css({
                    width: percentTime + "%"
                });
                //if percentTime is equal or greater than 100
                if (percentTime >= 100) {
                    //slide to next item 
                    $elem.trigger('owl.next')
                }
            }
        }

        //pause while dragging 
        function pauseOnDragging() {
            isPause = true;
        }


        function moved() {
            clearTimeout(tick);
            start();
        }
    });

    //Initiat WOW JS
    try {
        new WOW().init();
    }
    catch (err) {
    }

    $(document).ready(function () {
        //Animated Progress
        $('.progress-bar').bind('inview', function (event, visible, visiblePartX, visiblePartY) {
            if (visible) {
                $(this).css('width', $(this).data('width') + '%');
                $(this).unbind('inview');
            }
        });
    });

});





