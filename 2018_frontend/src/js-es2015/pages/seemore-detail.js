//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
export {
    SEEMORE_DETAIL as SEEMORE_DETAIL,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class SEEMORE_DETAIL extends Main {
    constructor(NAME = 'see more detail', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.init();
        this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch(hash);
        //this.anim();
    }
    init(){
        super.init();
        $('.select-opt2').slick({
            dots: false,
            infinite: false,
            speed: 700,
            slidesToShow: 4,
            slidesToScroll: 1,
            responsive: [{
                    breakpoint: 1000,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                        infinite: false,

                    }
                }, {
                    breakpoint: 567,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 3,
                        infinite: false,

                    }
                }



            ]
        });

    }
    watchScroll() {

    }
   
    bind() {

        // console.log('binding....');
        // const context = this;
        // $('.select-area > a').click(function(){
        //     let area = $(this).data('id');
        //     // context.datafetch(id);
        //     if(area==""){area="六都"}
        //         let cityies = GLOBAL.geo[area].cities;

        //         context.updateViewUi(area)
        //         context.updateView(cityies)
        //         context.updateViewUiCounty(0)
        // })
    }

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