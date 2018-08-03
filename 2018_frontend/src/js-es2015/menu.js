
import { GLOBAL } from './config.js';

function MENU() {
    let curr = 0,
        last = 0,
        sanim,
        interval, state,
        bgState = 'off';
    function route(hash) {
        var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
        let top;
        let navh = $('nav').height() + 20
        top = $("#"+hash).offset().top;
        //TweenMax.set(window, {scrollTo:{y:top}});
        $body.animate({
            scrollTop: top - navh 
        }, 700);
        updateState(hash)
    }

    function getHash() {
        var hash = document.location.hash
        //     id = hash.match(re); // for some reason this matches both the full string and the number
        // id = id.pop();
        return hash;
    }

    function scrollBy(typ = "share") {
        if (typ != "body") {
            $('html , body').css("overflow-y", "hidden")
        } else {
            $('html , body').css("overflow-y", "auto")
        }
    }

    function showPop(typ = "game") {
        console.log("showPop:" + typ)
        if(typ=='game')
        $(".btn-qa-kv").trigger("click");
        else{
            let id = typ.replace( "result", "");
            console.log("result:" + id)
            $('#result'+id+'_pop' ).trigger('click');
            GLOBAL.ga.GT('/bot-web', '.pv.' +typ , '' );
        }
    }

    function bind() {
        $('.navbar-search').hover(function(){

            TweenMax.to($(this).find('input') ,.5, {'width':100})
            let toggle = $('.navbar-menu').attr('data-toggle');
            
            if(toggle!='collapse'){
                const bg = $('.navbar .bg-cover')
                $('#navbar').animate({height: 0}, 300);
                $('.navbar-menu').attr('data-toggle' , 'collapse');
                TweenMax.to($(".navbar-toggle .icon-bar.top") , .3, {y:0, x:0,rotation:0 , transformOrigin:"50% 50%"} )
                TweenMax.to($(".navbar-toggle .icon-bar.mid") , .3, {opacity:1,rotation:0 , transformOrigin:"50% 50%"} )
                TweenMax.to($(".navbar-toggle .icon-bar.bottom") , .3, {y:0,x:0,rotation:0 , transformOrigin:"50% 50%"} )
                 $('#navbar ul li ').each(function(){
                    TweenMax.to($(this) ,.3 , {opacity:0 , y:20})
                
                })
                if($(window).scrollTop()<60)
                {
                    TweenMax.to(bg , .5, {delay:.2,opacity:0,ease:Expo.easeOut}) ;
                }
            }
        } , function(){
            TweenMax.to($(this).find('input') ,.5, {'width':1})
        })
        $('.navbar-menu').click(function(){
            let toggle = $(this).attr('data-toggle');
            collapseNav(toggle)
        })
        function collapseNav(toggle){
            const bg = $('.navbar .bg-cover')
             const autoHeight = parseInt($('#navbar').css('height', 'auto').height());
            if(toggle == "collapse"){
                $('#navbar').css('height' ,0);
                $('.navbar-menu').attr('data-toggle' , 'expand');
                // TweenMax.to($('#navbar') , .5,{height:'auto'})
                $('#navbar').animate({height: autoHeight}, 300);
                TweenMax.to(bg , .5, {opacity:1,ease:Expo.easeOut}) ;   
                TweenMax.to($(".navbar-toggle .icon-bar.top") , .2, {y:6, x:0,rotation:45 , transformOrigin:"50% 50%"} )
                TweenMax.to($(".navbar-toggle .icon-bar.mid") , .2, {opacity:0,rotation:45 , transformOrigin:"50% 50%"} )
                TweenMax.to($(".navbar-toggle .icon-bar.bottom") , .2, {y:-6,x:0,rotation:-45 , transformOrigin:"50% 50%"} )
                let count =0;
                $('#navbar ul li ').each(function(){
                    TweenMax.fromTo($(this) ,.5 , {opacity:0 , y:20} , {opacity:1 , y:0 , delay:.05 * count , ease:Back.easeOut})
                    count ++
                })
            }else{
                
                $('#navbar').animate({height: 0}, 300);
                $('.navbar-menu').attr('data-toggle' , 'collapse');
                TweenMax.to($(".navbar-toggle .icon-bar.top") , .3, {y:0, x:0,rotation:0 , transformOrigin:"50% 50%"} )
                TweenMax.to($(".navbar-toggle .icon-bar.mid") , .3, {opacity:1,rotation:0 , transformOrigin:"50% 50%"} )
                TweenMax.to($(".navbar-toggle .icon-bar.bottom") , .3, {y:0,x:0,rotation:0 , transformOrigin:"50% 50%"} )
                
                 $('#navbar ul li ').each(function(){
                    TweenMax.to($(this) ,.3 , {opacity:0 , y:20})
                
                })
                if($(window).scrollTop()<60)
                {
                    TweenMax.to(bg , .5, {delay:.2,opacity:0,ease:Expo.easeOut}) ;
                }
            }
                
        }
        

        $("a.hash").each(function() {
            console.log("hash")
            $(this).click(function(e) {
                e.preventDefault();
                var ga = $(this).data("ga");
                var link = $(this).attr('href');
                let hash = $.param.fragment(link).split('/')[1];
                console.log("hash " + hash);
                if ($('#' + hash).parents('html').length > 0) {
                    let toggle = $('.navbar-toggle')
                    if (toggle.attr('aria-expanded') == 'true')
                        toggle.trigger('click');


                    GLOBAL.ga.GT(( $(this).parent().hasClass('banner') )? '/nav-banner' :'/nav', '.btn.' +ga, "" );
                    switch (ga) {
                        case "game":
                            
                            
                            if(GLOBAL.started != 1 )
                            showPop(hash);
                            break;
                        case "promo":
                            route(ga);
                            break;
                        case "blogger":
                            route(ga);
                            break;
                        case "trial":
                            sendTrackParam('JYfp037zYK7Q', "btn A", "", "", "", "", "", "", "", "", "", "", "");
                            route(ga);
                            break;
                      
                    }
                } else {
                    GLOBAL.ga.GT(( $(this).parent().hasClass('banner') )? '/nav-banner' :'/nav', '.btn.' +ga, "" );
                    if( $(this).parent().hasClass('banner') ){
                        if(ga=='trial'){
                            sendTrackParam('JYfp037zYK7Q', "", "btn B", "", "", "", "", "", "", "", "", "", "");
                            findoutRedeemNow();
                        }
                        
                        else
                        findoutPetCombination();
                    }
                    setTimeout(function(){location.href = link;} , 300)
                    
                }

                return false;
            })

        })
        $("nav ul li ").each(function(){
            $(this).hover(function(){
                
                TweenMax.to($(this).find('.line') , .5 ,{opacity:1 , scaleX:1 , transformOrigin:"0% 0%",ease:Cubic.easeOut})
            } , function(){
                if(!$(this).hasClass('act'))
                TweenMax.to($(this).find('.line') , .5 , {opacity:0 , scaleX:0 , transformOrigin:"0% 0%",ease:Cubic.easeIn})

            })
        })
        // $('.dropdown').on('show.bs.dropdown', function() {
        //     $(this).find('.dropdown-menu').first().slideDown(500);
        //     $(this).find('.dropdown-toggle .plus').html('-')
        // });

        // // Add slideUp animation to Bootstrap dropdown when collapsing.
        // $('.dropdown').on('hide.bs.dropdown', function() {
        //     $(this).find('.dropdown-menu').first().hide();
        //     $(this).find('.dropdown-toggle .plus').html('+')
        // });

        // $('#navbar .btn-close img').click(function(){
        //     $('.navbar-toggle').trigger("click")
        // })

    }
    this.getupdateState = function(id) {
        updateState(id);
    }

    function updateState(id) {

        curr = id;
        $('nav #navbar > ul > li ').each(function() {
            let ga = $(this).data('ga');
            if (curr == ga) {
                $(this).addClass('act');
                //TweenMax.to($(this).find('.line') , .5 ,{opacity:0 , scaleX:0, transformOrigin:"0% 0%",ease:Cubic.easeOut})
            } else {
                $(this).removeClass('act')
                TweenMax.to($(this).find('.line') , .5 ,{opacity:0, scaleX:0 , transformOrigin:"0% 0%",ease:Cubic.easeOut})

            }
        })
    }

    function chgState(obj, id, typ) {
        clearTimeout(interval)
        if (typ == "act") {
            if (id != 'fb') {

            }

        } else {



            //sanim.setPolyOpen(curr)
        }
    }

    function bind_html_link() {
        $('nav li ').not('.hash').each(function() {
            // $(this).hover(function() {
            //     let id = $(this).data('id');
            //     if (id != curr)
            //         chgState($(this), id, 'act')
            // }, function() {
            //     let id = $(this).data('id');
            //     if (id != curr)
            //         chgState($(this), id, 'dis')
            // })
             $(this).find('.tracklink').hover(function(){
                    TweenMax.to($(this).find('i') , .2 ,{x:5})
             } , function(){
                    TweenMax.to($(this).find('i') , .2 ,{x:0})
             })
            $(this).find('.tracklink').click(function(e) {

                let target = $(this).attr('target');
                let href = $(this).attr('href');
                let act = $(this).data('act');

                let ga = $(this).data('ga');
                //GLOBAL.ga.GT('/nav', '.click' , ga );
                
                GLOBAL.ga.GT('/nav', '.btn.' +ga, "" );
                if(ga == 'tobuy'){
                    console.log('tobuy ...... media');
                    //cy_action_conver('5558404','sccvbrgm','53','2');
                }
                clk(target, href, act, ga, e);

                return false;
            })
        })

        $(".wrapper .tracklink").click(function(e) {
                let target = $(this).attr('target');
                let href = $(this).attr('href');
                let act = $(this).data('act');
                let ga = $(this).data('ga');
                //GLOBAL.ga.GT('/nav', '.click' , ga );
                let page = $('#page').val();
                GLOBAL.ga.GT('/'+page, '.btn.' +ga, "" );

                if(ga == 'tobuy1' ||ga == 'tobuy2' ||ga == 'tobuy3'){
                    console.log('tobuy ......media');
                    switch(ga){
                        case 'tobuy1':
                            //活力保養組
                            momBuyEnergy();
                        break;
                        case 'tobuy2':
                            //水乳霜組
                            momBuyWaterMilk();
                        break;
                        // case 'tobuy3':
                        //     cy_action_conver('5558404','zlfzrecu','53','2');
                        // break;
                    }
                }
                clk(target, href, act, ga, e);
                return false;
        })

        

        $('.navbar-header').find('.tracklink').click(function(e) {

            let target = $(this).attr('target');
            let href = $(this).attr('href');
            let act = $(this).data('act');
            let ga = $(this).data('ga');
            GLOBAL.ga.GT('/nav', '.btn.'+ga ,  );
            clk(target, href, act, ga, e);
            return false;
        })

        function clk(target, href, act, ga, e) {
            e.preventDefault();
            //GLOBAL.ga.GT('/menu', '.btn.' + ga);
            if (act == "disable") {
                alert("敬請期待!")
            } else if (target === '_blank') {
                if(ga=="tvc"){
                    //window.open(href, target  , "width=600,height=400");
                    $('.pop-tvc').fadeIn('fast');
                    TweenMax.to($('.banner') , .5 , {x:140,ease:Cubic.easeOut})
                    
                }else
                window.open(href, target);
            } else {
                setTimeout(function() { window.open(href, '_self'); }, 300)
            }
        }
    }

    function chkIgContainsHash() {
        let link = location.href;
        let hash = $.param.fragment(link)//.split('#')[1];
        console.log("hash " + hash)
        if (hash) {
                try{
                     if ($('#' + hash).parents('html').length > 0) {
                    if (hash == "game" || hash.indexOf("result")>=0 ) {
                        showPop(hash)
                        return
                    }
                    setTimeout(function() { route(hash); }, 1000);
                    } else {
                    //location.href = link;
                    }
                }catch(err){}

               
            // } catch (err) {}

        }
    }
    function loop(){
       let top = GLOBAL.top;

        if(top>0){
            if (bgState != 'on') {
                TweenMax.killTweensOf($('.navbar >.container >.bg'))
                TweenMax.to($('.navbar >.container >.bg'), 1, { opacity: 1 ,ease:Expo.easeOut})
            }
            bgState = 'on'
        }else{
            if(bgState != 'off'){
                TweenMax.killTweensOf($('.navbar >.container >.bg'))
                TweenMax.to($('.navbar >.container >.bg') ,1, {opacity:0,ease:Expo.easeOut})
            }
            
            bgState = 'off'
        }
        setTimeout( loop, 20)
    }
    this.init = function() {
        setTimeout(chkIgContainsHash , 100)
        //updateState(curr);
        bind_html_link();
        bind();
        loop()

    };
    this.init();
}

export { MENU as MENU }