//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
import { FB_ASSET } from "../fb_assets.js";
export {
    BILL_COUNTY as BILL_COUNTY,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class BILL_COUNTY extends Main {
    constructor(NAME = 'councilmen county', ifFB = true, ifYT = false, ifScrollHandle = true) {
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
    /**
     * 檢查有沒有給#區域
     * @return HASH
     */
    chkIgContainsHash() {
        let link = location.href;
        let hash = $.param.fragment(link)//.split('#')[1];
       
        if (hash) {
            console.log("hash " + hash)
        }
        return decodeURIComponent(hash)
    }
    /**
     * 抓特定年份重新整理資料到  GLOBAL.geo
     * @param  {[type]} area [description]
     * @param  {[type]} year [description]
     * @return {[type]}      [description]
     */
    datafetch(area , year){
        const context = this;
        getD(area, year)
        function getD(area = '六都'  , year=2018){
            //if(year_global) year = year_global;
             $.get( jsonUrl_global , (pResponse) => {
                if (pResponse) {
                    GLOBAL.constituencies = pResponse;
                    updateData('高山原住民');
                    updateData('平地原住民');
                    console.log('area...'+area);
                    console.log('GLOBAL.county...'+GLOBAL.county)
                    if(area==""){
                        area=findAreaBycounty(county_global);
                    }
                    let cityies = GLOBAL.geo[area].cities;
                    context.updateViewUi(area);
                    context.updateView(cityies , 'city');
                    
                    let ct = context.updateViewUiCounty(county_global);
                    context.updateViewCounty(ct);
                    
                } else {
                    alert('出現錯誤，請稍後再試！');
                }
            }, 'json');
        }
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
    // datafetchCounty(){

    // }
    updateViewUi(area ){
            
            $('.select-area > a').each(function(){
                let id = $(this).data('id');
                if(id == area){
                    $(this).addClass('act');
                }else{
                    $(this).removeClass('act');
                }
            })
            GLOBAL.area=area
            
       
    }
    updateViewUiCounty(county = 0){
        let tmp = county 
        if(county == 0){
            county=$('.select-county a:first').data('id');
        }
        GLOBAL.county=county
        $('.select-county a').each(function(){

                let id = $(this).data('id');
                
                if(id == county){
                    if(tmp !=0)
                    $(this).addClass('act');
                }else{
                    $(this).removeClass('act');
                }

                

        })

        return county;
        
    }

    /**
     * 更新區域option們
     * @param  {[type]} cityies [description]
     * @param  {[type]} typ     要更新的內容為城市或是選區
     * @return {[type]}         NULL
     */
    updateView(cityies,typ) {
        const context = this;

       
        if($('.select-county  a').length >=10){
            $('.select-county').slick('unslick');
        }
        $('.select-county').html('')


        for(let i in cityies ){
            $('.select-county').append(`
             <a href="${prefixUrl_global}#${GLOBAL.area}" data-id="${cityies[i].cne}">${cityies[i].cne}</a>
              `)
        }
        context.bindcounty();
        if($('.select-county  a').length>=10)
        $('.select-county').slick({
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
    /**
     * RENDER 每區的方塊資訊
     * @param  {[type]} cityies [description]
     * @return {[type]}         [description]
     */
    updateViewCounty(county) {
        return
        const context = this;
        let cityies;
        if( GLOBAL.area.indexOf('原住民')<0 ){
            let items = GLOBAL.constituencies;
            cityies = $.grep(items, function(item) {
                return item.county.indexOf(county) >=0;
            });

        }else{
            let items = GLOBAL.constituencies;
            let area = (GLOBAL.area=="高山原住民") ? '山地原住民' :GLOBAL.area
            cityies = $.grep(items, function(item) {
                return (item.county.indexOf(county) >=0 && item.district.indexOf(area) >=0) ;
            });
        }
        $('.select-county-blk').html('');
        //let hash = context.chkIgContainsHash();
        for(let i in cityies ){

                $('.select-county-blk').append(`
                  <div class="col-xs-6 col-sm-3">
                  <a class="info councilmen-area" href="${prefixUrl_global}${cityies[i].county}/${cityies[i].constituency}/#${GLOBAL.area}">
                  <p></p>
                  <p class="eng">${cityies[i].constituency}</p>
                  <div class="area-info">${cityies[i].district}</div>
                  </a>
                  
                  </div>
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
    bindcounty(){
        const context = this;
        $('.select-county > a').off('click').click(function(){
            
            let id = $(this).data('id');
           
            console.log("id..."+id);

            let ct =  context.updateViewUiCounty(id)
            
            context.updateViewCounty(ct)

        })


    }
    bind() {
        const context = this;
        $('.select-area a').click(function(){
            let area = $(this).data('id');
            if(area==""){area="六都"}
            let cityies = GLOBAL.geo[area].cities;
            
            context.updateViewUi(area);
            context.updateView(cityies , 'city');
            let ct = context.updateViewUiCounty(0);
            context.updateViewCounty(ct);
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