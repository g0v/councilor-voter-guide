'use strict'
const gulp = require('gulp');
const watch = require('gulp-watch');
const uglify = require('gulp-uglify');
const rename = require('gulp-rename');
const connect = require('gulp-connect')
const browserSync = require('browser-sync');
const less = require('gulp-less');
const compress = require('gulp-clean-css');
const tingpng = require('gulp-tinypng');
const pug = require('gulp-pug');
const gulpPlumber = require('gulp-plumber');
const livereload = require('gulp-livereload');
const version = require('gulp-version-number');
const path = require('path');
const fs       = require('fs');
const rollup = require('rollup').rollup;
const rollBabel = require('rollup-plugin-babel');
const commonjs = require('rollup-plugin-commonjs');
const nodeResolve = require('rollup-plugin-node-resolve');
const merge = require('merge-stream');
const sourcemaps = require('gulp-sourcemaps');
const g_if = require('gulp-if');
const spritesmith = require('gulp.spritesmith');
const buffer = require('vinyl-buffer');

const rimraf = require('rimraf');//DELET FOLDER
const chalk = require('chalk');//TERMINAL STRING
const runSequence = require('run-sequence');
const cache = require('gulp-cache');
const gulpCopy = require('gulp-copy');
///////////////////////////
//  參數傳遞
//////////////////////////
const argv = require('yargs').argv;
const PROJ = argv.proj;
const ifsourcemap = argv.ifsourcemap; 
const iftinyPNG = argv.iftinyPNG; //是否壓縮圖片
const ifdebug = argv.ifdebug;
///////////////////////////
//  定義執行環境
//////////////////////////
const folders = [  PROJ + '/src/' ];
const distfolders = [ PROJ + '/dist/'];

function logDevelopment() {
  const str = `
  ########  ######## ##     ##
  ##     ## ##       ##     ##
  ##     ## ##       ##     ##
  ##     ## ######   ##     ##
  ##     ## ##        ##   ##
  ##     ## ##         ## ##
  ########  ########    ###
  `;
  console.log(chalk.black.bgYellow(str));
}
function logProduction() {
  const str = `
  ########  ########   #######
  ##     ## ##     ## ##     ##
  ##     ## ##     ## ##     ##
  ########  ########  ##     ##
  ##        ##   ##   ##     ##
  ##        ##    ##  ##     ##
  ##        ##     ##  #######   `;
  console.log(chalk.bgCyan.white.bold(str));
}
///////////////////////////
//  定義任務
//////////////////////////
gulp.task('images', function() {
    const key = ['M-yeAktpEJ2UQhw29HEd6SB3sCaStZWX', 'ZoJZETIJn3qrq3dUdz2VIlNLA8GjgQ-Z'];
    
    const paths = [''];
    const tasks = folders.map(function(folder){
        let ind = folders.indexOf(folder);
        for (var i = 0; i < paths.length; i++) {
           return gulp.src(folder + 'img/dest/' + paths[i] + '*.{png,jpg,jpeg}')
                .pipe(tingpng(key[0]))
                .pipe(gulp.dest(distfolders[ind] + 'img/dest/' + paths[i]))
        }

    })
    return merge(tasks);

});

// gulp.task('watch-folder', function() {     
//     const tasks = distfolders.map(function(folder) {
//         let source = folder+'img';
//         let ind = distfolders.indexOf(folder);
//         let destination = folders[ind] + 'img';

//         return gulp.src(source + '/**/*', { base: source })
//             .pipe(watch(source, { base: source }))
//             .pipe(gulp.dest(destination));
//     })
//     return merge(tasks);
// });

//////////////
// SPRITE處理 //
//////////////
gulp.task('sprite',function(){
    console.log('sprite');
    const spriteData = gulp.src( folders[0]+ 'img/sprites/*.png')
        .pipe(spritesmith({
            imgName: '../img/dest/sprite.png',
            cssName: '_sprite.css',
            padding: 4,
            imgOpts: { quality: 100 },
            cssTemplate: folders[0]+'css/handlebars/basic.handlebars',
        }));
    const imgStream = spriteData.img
        .pipe(buffer())
        .pipe(gulp.dest(folders[0]+'dest/'));

    const cssStream = spriteData.css
        .pipe(gulp.dest(folders[0]+'css/org/'));
    return merge(imgStream, cssStream);
});
/*WATCH*/
gulp.task('watch', function() {
    livereload.listen();
    folders.map(function(folder){
        watch([folder + '*.pug',folder + 'pug/*.pug'], function() { gulp.start(['templates-watch' ]) })
        watch(folder + 'less/*.less', function() { gulp.start(['minify-css']) })
        watch(folder + 'less/component/*.less', function() { gulp.start(['minify-css']) })
        watch([folder + 'js-es2015/*.js' , folder + 'js-es2015/*/*.js'], function() { gulp.start(['bundle-js']) })
        watch(folder + 'js/*.js', function() { gulp.start('minify-js') })
    })
    //
});


/*LESS*/
gulp.task('less' , [], function() {
    //console.log('less');
     var tasks = folders.map(function(folder){
         let ind = folders.indexOf(folder);
         return  gulp.src(folder + 'less/**.less')
        //.pipe( g_if ( ifsourcemap==1 ,sourcemaps.init())  )
        .pipe(gulpPlumber(function (error) {
                console.log(error.message);
                this.emit('end');
        }))
        .pipe(less())
        .pipe(gulp.dest(folder + 'css/org'))
        
     })
     return merge(tasks);
    
});
/*壓縮 CSS*/
gulp.task('minify-css', ['less'], function() {
    var tasks = folders.map(function(folder){
         let ind = folders.indexOf(folder);
       return  gulp.src(folder + 'css/org/*.css')
            //.pipe(cssBase64())
            .pipe(compress({compatibility: 'ie8'}))
            .pipe(rename(function(path) {
                path.basename += ".min";
                path.extname = ".css";
            }))
            .pipe(gulp.dest(distfolders[ind] + 'css'))
            .pipe(browserSync.stream())
            .pipe(livereload())
            ;
    })
     return merge(tasks);
});


/*
ROLLUP JS
 */
gulp.task('bundle-js', function() {
    for(let n in folders){
        let folder = folders[n]
        rollup({
        entry: folder+'js-es2015/app.js',
        external: ['CSSPlugin' , 'EasePack' , 'TweenMax'],
        paths: {
          // CSSPlugin: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/latest/plugins/CSSPlugin.min.js',
          // EasePack: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/latest/easing/EasePack.min.js',
          // TweenMax: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/latest/TweenMax.min.js'
        },
        globals: {
          //TweenMax: 'TweenMax'
        },
        plugins: [ 
            //es2015無法編譯模塊
            nodeResolve({
                jsnext: true,  // Default: false
                main: true,  // Default: true
                browser: true,
            }),
            rollBabel({
              exclude: 'node_modules/**' // 只编译我们的源代码
            }), 
            commonjs({
              include: [
              'node_modules/**',
             
              ]
            })

        ]
    }).then(function (bundle) {
        var result = bundle.generate({
            format: 'iife'
        });
        fs.writeFileSync( 'bundle.js', result.code );
        bundle.write({
            format: 'iife',
            dest: folder+'js/bundle.js'
        });
    });    
    }
});
/*
MINIFY JS
 */
gulp.task('minify-js', [], function() {
     var tasks = folders.map(function(folder){
         let ind = folders.indexOf(folder);
        return gulp.src(folder + 'js/*.js')
        .pipe( g_if ( ifsourcemap==1 ,sourcemaps.init())  )
        .pipe(gulpPlumber())
        .pipe(uglify())
        .pipe(rename(function(path) {
            path.basename += ".min";
            path.extname = ".js";
        }))
        .pipe( g_if ( ifsourcemap==1 ,sourcemaps.write())  )
        //.pipe( g_if ( ifdebug==0 , stripDebug({debugger: true, console: true, alert: false})) )
        .pipe(gulp.dest(distfolders[ind] + 'js'))
        .pipe(livereload())
    })
     return merge(tasks);
});
/*
 JADE!
 */
gulp.task('templates', function() {
     var config = {
             'value': '%MDS%',
             'append': {
                 'key': 'ver_j',
                 'to': ['css', 'js'],
             },
    }   
    var tasks = folders.map(function(folder){
        let ind = folders.indexOf(folder);
    return gulp.src(folder + '*.pug')
        .pipe(gulpPlumber())
        .pipe(pug({ pretty: true}))
        //.pipe(g_if(ifsourcemap==1 ,version(config) ) )
        .pipe(gulp.dest(distfolders[ind]))
     })
    
     return merge(tasks);
});
/*
templates任務執行結束後 執行callback
(確保PUG已完成才reload)
 */
gulp.task('templates-watch', ['templates'], function (done) {
    var tasks = folders.map(function(folder){
    let ind = folders.indexOf(folder);
    return gulp.src(distfolders[ind] + '*.html')
            .pipe(livereload())
     })
     return merge(tasks);
});

/*
create Server
 */
gulp.task('connect-sync', function() {    
    connect.server({

        livereload: true,
    }, function() {
        browserSync({
            proxy: '127.0.0.1',            
            injectChanges: true,
            livereload:true,
        });
    });
});
gulp.task('logInfo',function(){
    let fun = (ifsourcemap==1) ? logDevelopment:logProduction;
    fun();
});
gulp.task('rimraf', (cb) => {
  console.log('rimraf');
  rimraf('./dist', cb);
});

gulp.task('copy', function() {

    const assets = [ 'img/common' ,'img/dest' , 'lib' , 'lib/css', 'lib/three' ];
    assets.forEach( function(asset){
            const tasks = folders.map(function(folder) {
                let source = folder + asset;
                let ind = folders.indexOf(folder);
                let destination = distfolders[ind] + asset;

                let pathes=(asset=='img' || asset=='lib/three')? [source + '/**/*']:[source + '/*']

                return gulp.src( pathes , { base: source })
                    //.pipe(gulpCopy(destination, { prefix:(folder.indexOf('/m/')>=0)?3:2 }))
                    .pipe(gulp.dest(destination));
            })
            return merge(tasks);
    } )

    
});
gulp.task('clear', () =>
    cache.clearAll()
);

/*初始任務清單*/ 
/*

 */
var tasklist = [ 'logInfo','watch', 'connect-sync', 'bundle-js','templates','less','minify-css'];
gulp.task('build' , tasklist);

if(ifsourcemap==1) 
  gulp.task('default',  () => runSequence( /*'rimraf'*/'clear','copy','build')) 
else {
  if(iftinyPNG==1){
    gulp.task('default',  () => runSequence('clear','copy', 'build' , 'images')) 
  }else{
    gulp.task('default',  () => runSequence(/*'rimraf',*/'clear', 'build'))   
  }
  
}
  


