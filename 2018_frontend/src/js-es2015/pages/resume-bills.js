//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
import { ARROWS } from "../arrows.js";
export {
    RESUME_BILLS as RESUME_BILLS,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class RESUME_BILLS extends Main {
    constructor(NAME = 'resume-bills', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.init();
        this.watchScroll();
        this.slickTool();
        this.updateView();
        this.anim();
        this.detailbind();
        new ARROWS($('.pagemanager'));
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
    detailbind(){
        let collapsestates = {}
        $('.content-item').each(function(){
            let id = $(this).data('id')
            $(this).find('.content-detail ').css('height' ,0);
            collapsestates[id] = 0
            $(this).find('.btn-detail').click(function(){
                let dom = $(this).parent().parent().parent()
                let ID = dom.data('id');
                let detail = dom.find('.content-detail');
                
                if(collapsestates[id] == 0){
                    autoHeightAnimate(detail , 500);
                    
                    TweenMax.to($(this).find('i') , .3 , {rotation:180})
                    collapsestates[id] = 1;
                }else{
                    detail.animate({ height: '0' }, 500);
                    TweenMax.to($(this).find('i') , .3 , {rotation:0})
                    collapsestates[id] = 0;
                }  
               
                
            })
        })
        function autoHeightAnimate(element, time) {
            var curHeight = element.height(), // Get Default Height
                autoHeight = element.css('height', 'auto').height(); // Get Auto Height
            element.height(curHeight); // Reset to Default Height
            element.stop().animate({ height: autoHeight }, time); // Animate to Auto Height
        }
            
    }
    anim() {
        const context = this;
        console.log('update View...')
        let count =0
        let rnd = Math.random() * 30
        let rndint = Math.ceil(rnd);
        let colorclass = 'bg-dark-group-color' 
        $('.content-list > .content-item ').each(function(){
            let n = (count + rndint)%30 + 1;
             console.log('add color...')
            $(this).addClass(colorclass + n);
            TweenMax.fromTo($(this) ,.7 ,{opacity:0,y:20},{delay:.5 + count*.05,opacity:1,y:0,ease:Back.easeOut})
            count++
            


        })
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