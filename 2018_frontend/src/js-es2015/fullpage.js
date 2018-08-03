export {
    FullPagejs as FullPagejs
}
function FullPagejs() {
    let events;
    let touchStartY = 0;
    let touchStartX = 0;
    let touchEndY = 0;
    let touchEndX = 0;
    let secys = [
        $('#kv'),
        $('#MayorAndCouncilor'),
        $('#seemore'),
        $('#bills'),
        $('#votes'),
        $('#wishingwell'),
        $('.footer')
    ];
    function touchhandle (scrollDirection){
                
                let targetUp,
                    targetDown,
                    targetElement;
                let lastScrollTop = $(window).scrollTop();
                let navh = $('nav').height() * 1.5
                

                if (lastScrollTop >= (secys[0].offset().top - navh) && lastScrollTop < (secys[1].offset().top - navh)) {
                    //console.log('SEC1..... ')
                    targetUp = secys[0];
                    targetDown = secys[1];
                } else if (lastScrollTop >= (secys[1].offset().top - navh) && lastScrollTop < (secys[2].offset().top - navh)) {
                    //console.log('SEC2..... ')
                    targetUp = secys[0];
                    targetDown = secys[2];
                } else if (lastScrollTop >= (secys[2].offset().top - navh) && lastScrollTop < (secys[3].offset().top - navh)) {
                    //console.log('SEC3..... ')
                    targetUp = secys[1];
                    targetDown = secys[3];
                } else if (lastScrollTop >= (secys[3].offset().top - navh) && lastScrollTop < (secys[4].offset().top - navh)) {
                    //console.log('SEC4..... ')
                    targetUp = secys[2];
                    targetDown = secys[4];
                } else if (lastScrollTop >= (secys[4].offset().top - navh) && lastScrollTop < (secys[5].offset().top - navh)) {
                    //console.log('SEC5..... ')
                    targetUp = secys[3];
                    targetDown = secys[5];
                } else if (lastScrollTop >= (secys[5].offset().top - navh) && lastScrollTop < (secys[6].offset().top - navh)) {
                    //console.log('SEC6..... ')
                    targetUp = secys[4];
                    targetDown = secys[6];
                }else if (lastScrollTop >= (secys[6].offset().top - navh)) {
                    //console.log('SEC7..... ')
                    targetUp = secys[5];
                    targetDown = secys[7];
                }else{
                         //console.log('SEC ELSE..... ')
                }
                if (scrollDirection === 'down') {
                    targetElement = targetDown;
                } else if (scrollDirection === 'up') {
                    targetElement = targetUp;
                } // end else if

                scrolltoDom(targetElement)
    }
    
    function scrollhandle(scrollDirection){
                let targetUp,
                    targetDown,
                    targetElement;
                let lastScrollTop = $(window).scrollTop();
                let navh = $('nav').height() * 1.5

                if (lastScrollTop >= (secys[0].offset().top - navh) && lastScrollTop < (secys[1].offset().top - navh)) {
                    targetUp = secys[0];
                    targetDown = secys[1];
                } else if (lastScrollTop >= (secys[1].offset().top - navh) && lastScrollTop < (secys[2].offset().top - navh)) {
                    //console.log('SEC2..... ')
                    targetUp = secys[0];
                    targetDown = secys[2];
                } else if (lastScrollTop >= (secys[2].offset().top - navh) && lastScrollTop < (secys[3].offset().top - navh)) {
                    //console.log('SEC3..... ')
                    targetUp = secys[1];
                    targetDown = secys[3];
                } else if (lastScrollTop >= (secys[3].offset().top - navh) && lastScrollTop < (secys[4].offset().top - navh)) {
                    //console.log('SEC4..... ')
                    targetUp = secys[2];
                    targetDown = secys[4];
                } else if (lastScrollTop >= (secys[4].offset().top - navh) && lastScrollTop < (secys[5].offset().top - navh)) {
                    //console.log('SEC5..... ')
                    targetUp = secys[3];
                    targetDown = secys[5];
                } else if (lastScrollTop >= (secys[5].offset().top - navh)) {
                    //console.log('SEC6..... ')
                    targetUp = secys[4];
                    targetDown = secys[6];
                }else{
                         //console.log('SEC ELSE..... ')
                }
                if (scrollDirection === 'down') {
                    targetElement = targetDown;
                } else if (scrollDirection === 'up') {
                    targetElement = targetUp;
                } // end else if

                scrolltoDom(targetElement)
    }
      var prevTime = new Date().getTime();
      var  scrollings= [];
      var isScrolling = false;
    function getAverage(elements, number){
            var sum = 0;

            //taking `number` elements from the end to make the average, if there are not enought, 1
            var lastElements = elements.slice(Math.max(elements.length - number, 1));

            for(var i = 0; i < lastElements.length; i++){
                sum = sum + lastElements[i];
            }

            return Math.ceil(sum/number);
    }
    function MouseWheelHandler(e) {
        var curTime = new Date().getTime();
        let scrollDirection;
        

            e = e || window.event;
        var value = (e.wheelDelta || -e.deltaY || -e.detail) / 2 ;
        var delta = Math.max(-1, Math.min(1, value));
        var horizontalDetection = typeof e.wheelDeltaX !== 'undefined' || typeof e.deltaX !== 'undefined';
        var isScrollingVertically = (Math.abs(e.wheelDeltaX) < Math.abs(e.wheelDelta)) || (Math.abs(e.deltaX ) < Math.abs(e.deltaY) || !horizontalDetection);

        if(scrollings.length > 149){
            scrollings.shift();
        }
        scrollings.push(Math.abs(value));
        // get scroll direction:
        
        e.preventDefault();
        if( isScrolling){
            return false;
        }

        var timeDiff = curTime-prevTime;
                prevTime = curTime;

        if(timeDiff > 200){
            console.log('clean array')
            scrollings = [];
        }
        var averageEnd = getAverage(scrollings, 10);
        var averageMiddle = getAverage(scrollings, 70);
        var isAccelerating = averageEnd >= averageMiddle;
        if (isAccelerating && isScrollingVertically ) {
            //scrolling down?
            if (delta < 0) {
                console.log('scroll down')
                scrollhandle('down');
                
                //scrolling up?
            } else {
                console.log('scroll up')
                scrollhandle('up')
                
            }
            isScrolling = true;
            // removeMouseWheelHandler();
            setTimeout( function(){
                isScrolling = false;
            }, 1500)   
        }else{
             isScrolling = false;
        }
        return false;
       
    }
    function removeMouseWheelHandler(){
            if (document.addEventListener) {
                document.removeEventListener('mousewheel', MouseWheelHandler, false); //IE9, Chrome, Safari, Oper
                document.removeEventListener('wheel', MouseWheelHandler, false); //Firefox
                document.removeEventListener('MozMousePixelScroll', MouseWheelHandler, false); //old Firefox
            } else {
                document.detachEvent('onmousewheel', MouseWheelHandler); //IE 6/7/8
            }
        }
    function addMouseWheelHandler(){
            var prefix = '';
            var _addEventListener;

            if (window.addEventListener){
                _addEventListener = "addEventListener";
            }else{
                _addEventListener = "attachEvent";
                prefix = 'on';
            }

             // detect available wheel event
            var support = 'onwheel' in document.createElement('div') ? 'wheel' : // Modern browsers support "wheel"
                      document.onmousewheel !== undefined ? 'mousewheel' : // Webkit and IE support at least "mousewheel"
                      'DOMMouseScroll'; // let's assume that remaining browsers are older Firefox


            if(support == 'DOMMouseScroll'){
                document[ _addEventListener ](prefix + 'MozMousePixelScroll', MouseWheelHandler, false);
            }

            //handle MozMousePixelScroll in older Firefox
            else{
                document[ _addEventListener ](prefix + support, MouseWheelHandler, false);
            }
        }
    function getEventsPage(e){
            var events = [];

            events.y = (typeof e.pageY !== 'undefined' && (e.pageY || e.pageX) ? e.pageY : e.touches[0].pageY);
            events.x = (typeof e.pageX !== 'undefined' && (e.pageY || e.pageX) ? e.pageX : e.touches[0].pageX);

            //in touch devices with scrollBar:true, e.pageY is detected, but we have to deal with touch events. #1008
            if( typeof e.touches !== 'undefined'){
                events.y = e.touches[0].pageY;
                events.x = e.touches[0].pageX;
            }

            return events;
    }
    function touchMoveHandler(e) {

        var touchEvents = getEventsPage(e);

        touchEndY = touchEvents.y;
        touchEndX = touchEvents.x;
        if (Math.abs(touchStartY - touchEndY) > 10) {
            e.preventDefault();
            if (touchStartY > touchEndY) {
                touchhandle('down');
            } else if (touchEndY > touchStartY) {
                touchhandle('up');
            }
        }


    }
    function touchStartHandler(e){
        var touchEvents = getEventsPage(e);
        touchStartY = touchEvents.y;
        touchStartX = touchEvents.x;
    }
    function addTouchHandler(){
        events= {
            touchmove: 'ontouchmove' in window ? 'touchmove' :  MSPointer.move,
            touchstart: 'ontouchstart' in window ? 'touchstart' :  MSPointer.down
        };
                document.removeEventListener(events.touchstart, touchStartHandler);
                document.removeEventListener(events.touchmove, touchMoveHandler, {passive: false});
                document.addEventListener(events.touchstart, touchStartHandler);
                document.addEventListener(events.touchmove, touchMoveHandler, {passive: false});
            
    }    
    function init() {
        if(device.mobile() || device.tablet()){
            secys = [
                    $('#kv'),
                    $('#findmayor'),
                    $('#findcouncilor'),
                    $('#seemore'),
                    $('#bills'),
                    $('#votes'),
                    $('#wishingwell'),
                    $('.footer')
            ];
            addTouchHandler();
        }else{
            addMouseWheelHandler();    
        }
        
    }
    init();
}

function scrolltoDom(dom) {
    var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
    let top;
    let navh = $('nav').height();
    top = dom.offset().top;
    let t = 700
    //TweenMax.set(window, {scrollTo:{y:top}});
    $body.stop().animate({
        scrollTop: top - navh
    }, t);
}
