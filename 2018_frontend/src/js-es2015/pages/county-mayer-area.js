//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
export {
    COUNTY_MAYER_AREA as COUNTY_MAYER_AREA,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class COUNTY_MAYER_AREA extends Main {
    constructor(NAME = 'county-mayer-area', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.init();
        this.watchScroll();
         let hash = this.chkIgContainsHash();
        this.datafetch(hash);
        
    }
    chkIgContainsHash() {
        let link = location.href;
        let hash = $.param.fragment(link)//.split('#')[1];
       
        if (hash) {
            console.log("hash " + hash)
        }
        return decodeURIComponent(hash)
    }
    init() {
        let context = this;
        super.init();


    }
    datafetch(area){
        const context = this;
        console.log('data fetching....');
        if(area==""){area="六都"}
        let cityies = GLOBAL.geo[area].cities;
        
        context.updateViewUi(area)
        context.updateView(cityies)
    }
    updateViewUi(area){

        $('.area-selector select').val(area);

        $('.select-area > a').each(function(){
            let id = $(this).data('id');
            if(id == area){
                $(this).addClass('act');
            }else{
                $(this).removeClass('act');
            }
        })
        GLOBAL.area = area;
    }
    updateView(cityies) {

        const context = this;



         $('.select-county-blk').html('')
        for(let i in cityies ){
            $('.select-county-blk').append(`
                <div class="col-xs-6 col-sm-3"><a class="info" href="/candidates/mayors/${cityies[i].cne}/#${GLOBAL.area}">
              <p>${cityies[i].cne}</p>
              <p class="eng">${cityies[i].eng}</p></a></div>
              `)
        }
        

        
        context.anim()
    }
   
    anim() {
        console.log('update View...')
        let count =0
        let rnd = Math.random() * 30
        let rndint = Math.ceil(rnd);
        let colorclass = 'bg-light-group-color' 
        //console.log(rndint)
        $('.select-county-blk > div ').each(function(){
            let n = (count + rndint)%30 + 1
            //console.log('n....'+n)
            $(this).find('.info').addClass(colorclass + n)
            TweenMax.fromTo($(this) ,.7 ,{opacity:0,y:20},{delay:.5 + count*.05,opacity:1,y:0,ease:Back.easeOut})
            count++
        })
    }
    watchScroll() {

    }
    bind() {
        const context = this;
        $('.area-selector select').change(function(){
            let area = $(this).val();
            
            $('.select-area > a').each(function(){
                let id = $(this).data('id');
                if(id==area)
                $(this).trigger('click');
            })

            // location.href = `./#${id}`
            // context.datafetch(id);
        })
        $('.select-area > a').click(function(){
            let id = $(this).data('id');
            context.datafetch(id)
        })
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