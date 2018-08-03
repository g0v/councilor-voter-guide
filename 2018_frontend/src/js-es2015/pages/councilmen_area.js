//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
export {
    COUNCILMEN_AREA as COUNCILMEN_AREA,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class COUNCILMEN_AREA extends Main {
    constructor(NAME = 'county-mayer-area', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        //this.fb = new FB_ASSET();
        this.init();
        this.watchScroll();
        let hash = this.chkIgContainsHash();
        this.datafetch( hash );
        
    }
    init() {
        let context = this;
        super.init();


    }
    chkIgContainsHash() {
        let link = location.href;
        let hash = $.param.fragment(link)//.split('#')[1];
       
        if (hash) {
            console.log("hash " + hash)
        }
        return decodeURIComponent(hash)
    }
    datafetch(area = '六都'  , year=2018){
        const context = this;
            if(year_global) year = year_global;
            $.get( jsonUrl_global , (pResponse) => {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');
                    if (area==""){area ="六都"}
                    let cityies = GLOBAL.geo[area].cities;
                    context.updateViewUi(area);
                    context.updateView(cityies , 'city');
                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');

        function updateData(category){

            GLOBAL.geo[category] = {cities:[]};
            //找出有山地原住民
            let items = GLOBAL.constituencies;


            
            let cts = $.grep(items, function(item) {
                if(category=='高山原住民')
                return item.district.indexOf('山地原住民') >=0;
                else
                return item.district.indexOf(category) >=0;
            });
            
            //console.log(cts)
            let norepeatcts = _.groupBy(cts, function(ct){ return ct.county; });

            for(let ct in norepeatcts){
                console.log('norepeatcts ...' + ct);
                let eng = findEngCounty( ct )
                GLOBAL.geo[category].cities.push({cne: ct , eng:eng})
            }
        }

        function findEngCounty(countyval){
            let all = GLOBAL.allcities
            let cts = $.grep(all, function(item) {
               
                return item.cne.indexOf(countyval) >=0;
            });
            return cts[0].eng
        }

        
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

       
    }

    /**
     * 更新區域方塊們
     * @param  {[type]} cityies [description]
     * @param  {[type]} typ     要更新的內容為城市或是選區
     * @return {[type]}         NULL
     */
    updateView(cityies,typ) {

        const context = this;



        $('.select-county-blk').html('');

        let hash = context.chkIgContainsHash();

        if(typ=='city'){
            for(let i in cityies ){

                $('.select-county-blk').append(`
                  <div class="col-xs-6 col-sm-3"><a class="info" href="/candidates/councilors/${cityies[i].cne}/#${hash}">
                  <p>${cityies[i].cne}</p>
                  <p class="eng">${cityies[i].eng}</p></a>
                  </div>
                  `)
            }
        }else{
            for(let i in cityies ){

                $('.select-county-blk').append(`
                  <div class="col-xs-6 col-sm-3">
                  <a class="info councilmen-area" href="/candidates/councilors/${cityies[i].cne}/#${hash}">
                  <p></p>
                  <p class="eng">01</p>
                  <div class="area-info">桃源區、那瑪夏區、甲
                    仙區、六龜區、杉林區
                    、內門區、旗山區、美
                    濃區、茂林區 </div>
                  </a>
                  
                  </div>
                  `)
            }
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