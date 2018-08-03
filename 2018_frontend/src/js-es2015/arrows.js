
class ARROWS{
    //name 属性
    //YTT_class.name  "YTT_class"
    constructor(dom){
        console.log('Arrows class contrusct...')
        this._dom = dom;
        this._Total = this._dom.find('.pg').length;
        // console.log('total pages ....' + this._Total)
        this._curr = this._dom.find('.pg.act').data('id');
        
        if(typeof this._curr == 'undefined'){
            this._curr = 1;    
        }
        
        

        this.NumPerPage = 10;
        
        
        this.chkPages = this.chkPages.bind(this);
        this.updateUIView = this.updateUIView.bind(this);
        this.updateView = this.updateView.bind(this);
        this.on = this.on.bind(this);
        this.init = this.init.bind(this);
        this.init();
        
    };
    

    init(){
        this.chkPages();
        this.updateUIView()
        this.updateView()
        this.on();


    }
    chkPages(){
        
        this.pgs = Math.ceil(this._curr /this.NumPerPage);
        this.maxPgs = Math.ceil(this._Total /this.NumPerPage);

       
        this.minpg = (this.pgs-1) *  this.NumPerPage;
        this.maxpg = (this.pgs) *  this.NumPerPage;
        
    }
    updateUIView(){ 
        this._dom.find('.pg' + this._curr).addClass('act');
        this._dom.find('.btnNext,.btnPrev').show();
        



        if(this.pgs >= this.maxPgs || this.maxPgs == 0){
            this._dom.find('.btnNext').hide();
        }
        if(this.pgs <=1){
            this._dom.find('.btnPrev').hide();
        }
    }
    updateView(){
        
        this.removePage(this.minpg,this.maxpg);
        this.addPage(this.minpg,this.maxpg)
    }
    hidePage(){}
    addPage(min  , max){
        let count =0;
        for(let i = 1 ; i <= this._Total ; i ++){
            if(i >min && i<= max){
                this._dom.find('.pg' + i).css('opacity', 0).show();
                TweenMax.fromTo( this._dom.find('.pg' + i), .2, {y:5} , {delay :.05 *count,y:0 , opacity:1})
                count ++
            }
            
            
        }
    }
    removePage(min  , max){
        for(let i = 1 ; i <= this._Total ; i ++){
            if(i <= min || i > max)
            this._dom.find('.pg' + i).hide();
            
        }
        
    }
    on(){
        let context = this;
        this._dom.find('.btnNext').click(function   (){
            // console.log('next........')
            context._curr= (context.pgs ) * context.NumPerPage+ 1;
            
           
            trigger()
        })
        this._dom.find('.btnPrev').click(function   (){
            
            context._curr = (context.pgs -2) * context.NumPerPage+ 1;
            // console.log('prev........'+context._curr)
           
            trigger()
        })


        function trigger(){
            context.chkPages();
            context.updateUIView()
            context.updateView()
        }
    }
    ///////////////////////////////
    //类的方法内部如果含有this，它默认指向类的实例。
    //但是，必须非常小心，一旦单独使用该方法，很可能报错。 //
    ///////////////////////////////
    /**
     * [_initplayer description]
     * 私有方法
     * 表示这是一个只限于内部使用的私有方法。
     * 但在类的外部，还是可以调用到这个方法。
     * (私有屬性)
     */
     /*

     */
    
    //https://aerotwist.com/blog/flip-your-animations/
   
}
export { ARROWS as ARROWS}
