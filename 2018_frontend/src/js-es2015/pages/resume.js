//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
export {
    RESUME as RESUME,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class RESUME extends Main {
    constructor(NAME = 'resume', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.init();
        this.watchScroll();
        this.slickTool();
        this.updateView();
    }
    init() {
        let context = this;
        super.init();


    }
    updateView() {
        let typ = $('.wrapper-header').data('type');
        $('.nav-resume-all  a').each(function(){
          let atyp = $(this).data('type');
          if(atyp == typ){
              $(this).addClass('act')
          }
        })


        $('nav.navbar , nav.navbar .bg-cover').addClass('bg-' + typ)

    }
    slickTool() {
        $('.nav-resume-all').on('init', function() {
            console.log('carousel3 has init....')
            $('.nav-resume-all .slick-prev').html(`<i class="fa fa-arrow-right"></i>`)
            $('.nav-resume-all .slick-next').html(`<i class="fa fa-arrow-right"></i>`)
        });
        $('.nav-resume-all').slick({

            dots: false,
            infinite: false,
            speed: 700,
            slidesToShow: 5,
            slidesToScroll: 1,
            responsive: [{
                    breakpoint: 767,
                    settings: {
                        slidesToShow: 4,
                        slidesToScroll: 4,
                        infinite: false,

                    }
                }, {
                    breakpoint: 567,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        infinite: false,

                    }
                }



            ]
        });
    }
    anim() {

    }
    watchScroll() {

    }
    bind() {}

}



function route(hash) {



    var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
    const speed = 5;
    let top;
    top = $("#" + hash).offset().top;

    let t = Math.abs(GLOBAL.top - top) / speed

    //TweenMax.set(window, {scrollTo:{y:top}});
    $body.animate({
        scrollTop: top - 120
    }, t);


}