//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
import { ARROWS } from "../arrows.js";
export {
    WISH as WISH,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class WISH extends Main {
    constructor(NAME = 'wish', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        
        this.init();
        this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );
        new ARROWS($('.pagemanager'));
    }
    init() {
        let context = this;
        super.init();
        this.anim()

    }
    /**
     * 檢查有沒有給#區域
     * @return HASH
     */
    
    /**
     * 抓特定年份重新整理資料到  GLOBAL.geo
     * @param  {[type]} area [description]
     * @param  {[type]} year [description]
     * @return {[type]}      [description]
     */
    
    // datafetchCounty(){

    // }
   
    
   
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
            $(this).find('.bg').addClass(colorclass + n);
            TweenMax.fromTo($(this) ,.7 ,{opacity:0,y:20},{delay:.5 + count*.05,opacity:1,y:0,ease:Back.easeOut})
            count++
            


        })
        
    }
    
    watchScroll() {

    }
    
    bind() {
        const context = this;
        let currFilter;
          console.log('binding...........')  
        $('.filters > .f-item').each(function(){

            if($(this).hasClass('act')){
                let id = $(this).data('id');
                console.log('filters act id ...' + id);
                currFilter = id;
            }

            $(this).click(function(){
                let id = $(this).data('id');
                 $('.filters > .f-item').removeClass('act');
                if(id != currFilter){
                    currFilter = id;
                     $(this).addClass('act');
                }
            })
        })
        // $('.select-county-blk > div ').hover(function(){
            
        //     TweenMax.to($(this).find('.hover-info') , .3 , {opacity:1})
        // } , function(){
        //      TweenMax.to($(this).find('.hover-info') , .3 , {opacity:0})
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

function enableSlick(dom){
    if(dom.find('a').length>=10)
        dom.slick({
            dots: false,
            infinite: false,
            speed: 700,
            slidesToShow: 10,
            slidesToScroll: 1,
            responsive: [{
                    breakpoint: 1000,
                    settings: {
                        slidesToShow: 6,
                        slidesToScroll: 1,
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

function WatchMove() {
    const data = {}
    var force = 0 
    
    function loop(){
        let bodyW = Number(getBrowserWidth())
        let vw = Number($('.head-j').width());
        let deltaX = (GLOBAL.mousex - bodyW/2 ); 
        if(deltaX>0){
            $('.hover-area .tri').css('left','75%')
            $('.hover-area').css('left' , deltaX + vw/2 -90)    
        }else{
            $('.hover-area .tri').css('left','20px')
            $('.hover-area').css('left' , deltaX + vw/2)
        }
        
        requestAnimationFrame(loop)
    }
    function init() {
        $('body').mousemove(function(event) {
            var clientCoords = "( " + event.clientX + ", " + event.clientY + " )";
            GLOBAL.mousex = event.clientX;
        });
        loop();
    }
    init();
}