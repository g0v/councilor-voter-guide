
import { GLOBAL } from './config.js';

function getUserPhoto(DOM, CB) {

    function bind() {
        var reader = new FileReader();
        var img = new Image();
        img.onload = function() {
            console.log(this.width);
            console.log(this.height);
            
        }
        /*FB USER PHOTO*/
        // $(".sec2 .btn-usefb").click(function() {
        //     //10155575608813664
        //     console.log("fbid " + GLOBAL.fbid);
        //     $('#loadingajax').fadeIn(400);
        //     GLOBAL.ga.GT('/share.step2', '.btn.fbpic');
        //     $.post(`${GLOBAL.api_root}api/?mode=savefbpic`, {
        //             fbid: GLOBAL.fbid,
        //         },
        //         (pResponse) => {
        //             $('#loadingajax').fadeOut(400);
        //             if (pResponse.state === '1') {
        //                 //alert('成功送出');
        //                 $('#preview_img').attr('src', GLOBAL.api_root + 'uploads/' + pResponse.data);
        //                 GLOBAL.uploaded = true;
        //                 $('.hint2').fadeOut('fast');
        //                 $('.hint-drag').fadeIn('fast')
        //                 CB($('#preview_img'))
        //             } else {
        //                 alert('出現錯誤，請稍後再試！');
        //             }
        //         }, 'json');

        // })

        var ori_tpy = '0';
        $('.canvas .hint').click(function(){
            $("#uploader").trigger("click");
        })
        $("#uploader").change(function() {

            var upload_file = this.files[0];

            DOM.html('')
            DOM.append(`            
            <canvas id="preview_img_reset" alt="empty preview"></canvas>
            `);
            
            GLOBAL.uploaded = true;
            EXIF.getData(upload_file, () => {
                if(device.mobile()|| device.tablet() ){
                    console.log("mobile")
                    ori_tpy = upload_file.exifdata.Orientation; 
                    try{
                        $('#preview_img_reset').data('ori' , ori_tpy.toString() )    
                    }catch(err){
                        console.log(err);
                        $('#preview_img_reset').data('ori' , '0' )   
                    }    
                }
                reader.readAsDataURL(upload_file);
                

            })
            reader.onload = function(e) {
                let resetImage = document.getElementById("preview_img_reset");
                let mpImg = new MegaPixImage(upload_file)
                mpImg.render(resetImage, { maxWidth: 480 * 2 , maxHeight: 2500 * 2})
                //let getImgR = ori_tpy;
                //console.log("onload:"+ori_tpy)
                // switch (ori_tpy.toString()) {
                //     case '8':
                //         TweenMax.set(resetImage, { rotation: -90, transformOrigin: '50% 50%' })
                //         break
                //     case '3':
                //         TweenMax.set(resetImage, { rotation: 180, transformOrigin: '50% 50%' })
                //         break
                //     case '6':
                //         TweenMax.set(resetImage, { rotation: 90, transformOrigin: '50% 50%' })
                //         break
                //     default:
                //         break
                // }
                setTimeout(CB , 300)
                //CB();

                
            }
            
            //$('.hint-drag').fadeIn('fast')
        })
    }
    this.init = function() {
        DOM.html('')
        DOM.append(`            
            <canvas id="preview_img_reset" alt="empty preview"></canvas>
            `);
        bind();
    }
    this.init();
}

/*IOS FIX*/

function resetOrientation(srcBase64, srcOrientation, callback) {
    var img = new Image();

    img.onload = function() {
        var width = img.width,
            height = img.height,
            canvas = document.createElement('canvas'),
            ctx = canvas.getContext("2d");

        // set proper canvas dimensions before transform & export
        if (4 < srcOrientation && srcOrientation < 9) {
            canvas.width = height;
            canvas.height = width;
        } else {
            canvas.width = width;
            canvas.height = height;
        }

        // transform context before drawing image
        switch (srcOrientation) {
            case 2:
                ctx.transform(-1, 0, 0, 1, width, 0);
                break;
            case 3:
                ctx.transform(-1, 0, 0, -1, width, height);
                break;
            case 4:
                ctx.transform(1, 0, 0, -1, 0, height);
                break;
            case 5:
                ctx.transform(0, 1, 1, 0, 0, 0);
                break;
            case 6:
                ctx.transform(0, 1, -1, 0, height, 0);
                break;
            case 7:
                ctx.transform(0, -1, -1, 0, height, width);
                break;
            case 8:
                ctx.transform(0, -1, 1, 0, 0, width);
                break;
            default:
                break;
        }

        // draw image
        ctx.drawImage(img, 0, 0);

        // export base64
        callback(canvas.toDataURL());
    };

    img.src = srcBase64;
}

function getOrientationFileEvent(event, callback) {
    var view = new DataView(event.target.result);

    if (view.getUint16(0, false) != 0xFFD8) return callback(-2);

    var length = view.byteLength,
        offset = 2;

    while (offset < length) {
        var marker = view.getUint16(offset, false);
        offset += 2;

        if (marker == 0xFFE1) {
            if (view.getUint32(offset += 2, false) != 0x45786966) {
                return callback(-1);
            }
            var little = view.getUint16(offset += 6, false) == 0x4949;
            offset += view.getUint32(offset + 4, little);
            var tags = view.getUint16(offset, little);
            offset += 2;

            for (var i = 0; i < tags; i++)
                if (view.getUint16(offset + (i * 12), little) == 0x0112)
                    return callback(view.getUint16(offset + (i * 12) + 8, little));
        } else if ((marker & 0xFF00) != 0xFF00) break;
        else offset += view.getUint16(offset, false);
    }
    return callback(-1);
}

function getOrientation(file, callback) {
    var reader = new FileReader();
    reader.onload = function(event) {
        getOrientationFileEvent(event, callback)
    };

    reader.readAsArrayBuffer(file.slice(0, 64 * 1024));
};
export { getUserPhoto }