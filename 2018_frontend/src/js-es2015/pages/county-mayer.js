//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
export {
    COUNTY_MAYER as COUNTY_MAYER,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class COUNTY_MAYER extends Main {
    constructor(NAME = 'county-mayer', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.init();
        this.watchScroll();
        let hash = this.chkIgContainsHash();
        this.datafetch(hash);
        this.anim();
    }
    chkIgContainsHash() {
        let link = location.href;
        let hash = $.param.fragment(link)//.split('#')[1];
       
        if (hash) {
            console.log("hash " + hash)
            GLOBAL.area = hash
        }
        return decodeURIComponent(hash)
    }
    init() {
        let context = this;
        super.init();


    }


    datafetch(area){
        const context = this;
        console.log('data fetching....' + area);
        if(area=="" || !checkArea(area)){ 
            area=findAreaBycounty(county_global);
        }
        let cityies = GLOBAL.geo[area].cities;

        context.updateViewUi(area)
        context.updateView(cityies)
        context.updateViewUiCounty(county_global)


        function findAreaBycounty(county){
            let area;
            for (let i in GLOBAL.geo) {
                let cities = GLOBAL.geo[i].cities;
                console.log('iterate ...area:' + i)
                for (let j in cities) {
                    let ct = GLOBAL.geo[i].cities[j].cne;
                    if (county == ct) {
                        console.log('city match ...area:' + county);
                        area = i;
                        break;
                    }
                }

                if (typeof area != 'undefined')
                    break;
            }
            return area;
        }

        function checkArea(a){
            let areas = ['六都','北部','中部','南部','東部','離島', '原住民'];

            for(let i in areas){
                if(a.indexOf(areas[i]) >=0){
                    return true;
                }
            }
            return false;

        }

    }
    updateViewUi(area){
        $('.select-area > a').each(function(){
            let id = $(this).data('id');
            if(id == area){
                $(this).addClass('act');
            }else{
                $(this).removeClass('act');
            }
        })
        GLOBAL.area = area

    }
    updateViewUiCounty(val){
        let tmp = val
        if(val==0){
            val=$('.select-county a:first').data('id');
        }
        $('.select-county  a').each(function(){
            let id = $(this).data('id');
            if(id == val){
                if(tmp !=0 )
                $(this).addClass('act');
            }else{
                $(this).removeClass('act');
            }
        })
    }
    updateView(cityies) {
        const context = this;

        $('.select-county').html('')
        for(let i in cityies ){
            $('.select-county').append(`
             <a href="${prefixUrl_global}${cityies[i].cne}/#${GLOBAL.area}" data-id="${cityies[i].cne}">${cityies[i].cne}</a>
              `)
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
            let n = (count + rndint)%30 + 1
            $(this).addClass(colorclass + n);
            TweenMax.fromTo($(this) ,.7 ,{opacity:0,y:20},{delay:.5 + count*.05,opacity:1,y:0,ease:Back.easeOut})
            count++
            


        })

        
        context.detailbind()
    }
    watchScroll() {

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
    bind() {
        console.log('binding....');
        const context = this;
        // $('.select-area > a').click(function(){
        //     let area = $(this).data('id');
            
        //     // context.datafetch(id);
        //     // if (area == "") {
        //     //     area = "六都"
        //     // }
        //     // let cityies = GLOBAL.geo[area].cities;

        //     // context.updateViewUi(area)
        //     // context.updateView(cityies)
        //     // context.updateViewUiCounty(0)
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