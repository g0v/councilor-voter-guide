
export { imageEditor }

function imageEditor(...augs) {
    const [MAXZ, MINZ, MAXR, MINR] = augs;
    const moveInterval = 5;
    let [zoomv, rotv] = [50, 50];
    let [cx , cy] = [0,0]

    function bind() {
        console.log('bind imageEditor...')

        function chk_containsImg() {

            return true;
        }
        $('.zoom input[type=range]').change(function() {
            if (!chk_containsImg()) return

            zoomv = Number($(this).val());
            console.log('value ...' + zoomv)
            //update pic            
            let zoom = (MAXZ - MINZ) / 100 * zoomv
            updateView({ zoom: zoom })
        });

        $('.ui .btn-j.btn-move').click(function(){
            if (!chk_containsImg()) return
            let id = $(this).data('id');
            switch(id){
                case "up":
                    cy-=moveInterval;
                break;
                case "down":
                    cy+=moveInterval;
                break;
                case "left":
                    cx-=moveInterval;
                break;
                case "right":
                    cx+=moveInterval;
                break;
            }

            TweenMax.to($(".pop-share .upload"), .3, { x: cx, y: cy })
            // update the posiion attributes
            target.setAttribute('data-x', cx);
            target.setAttribute('data-y', cy);
        })
        $('.ui .btn-j.btn-zoom').click(function() {
            if (!chk_containsImg()) return
            let id = $(this).data('id')

            if (id == "out") {
                console.log('value ...' + zoomv)
                if (zoomv > 0) {
                    zoomv -= 5
                } else {
                    zoomv = 0
                }

            } else {
                console.log('value ...' + zoomv)
                if (zoomv < 100) {

                    zoomv += 5
                } else {
                    zoomv = 100
                }

            }
            $('.zoom input[type=range]').val(zoomv);
            let zoom = (MAXZ - MINZ) / 100 * zoomv
            updateView({ zoom: zoom })
        })



        $('.rotate input[type=range]').change(function() {
            if (!chk_containsImg()) return
            rotv = Number($(this).val());
            console.log('value ...' + rotv)
            //update pic            
            let rot = (MAXR - MINR) / 100 * (rotv - 50)

            updateView({ rotate: rot })
        });

        $('.rotate > .btn').click(function() {
            if (!chk_containsImg()) return
            let id = $(this).data('id')
            if (id == "out") {
                if (rotv > 0) {
                    rotv -= 5
                } else {
                    rotv = 0
                }

            } else {
                if (rotv < 100) {
                    rotv += 5
                } else {
                    rotv = 100
                }

            }
            $('.rotate input[type=range]').val(rotv);
            let rot = (MAXR - MINR) / 100 * (rotv - 50)
            updateView({ rotate: rot })
        })

        /////DRAG
        interact('.draggable')
            .draggable({
                // enable inertial throwing
                inertia: true,
                // keep the element within the area of it's parent

                // enable autoScroll
                autoScroll: true,

                // call this function on every dragmove event
                onmove: dragMoveListener,
                // call this function on every dragend event
                onend: function(event) {
                    var textEl = event.target.querySelector('p');

                    textEl && (textEl.textContent =
                        'moved a distance of ' +
                        (Math.sqrt(event.dx * event.dx +
                            event.dy * event.dy) | 0) + 'px');
                }
            });

        function dragMoveListener(event) {
            var target = event.target,
                // keep the dragged position in the data-x/data-y attributes
                x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
                y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

            // translate the element
            /*target.style.webkitTransform =
                target.style.transform =
                'translate(' + x + 'px, ' + y + 'px)';*/
            TweenMax.to($(".pop-share .upload"), .3, { x: x, y: y })
            // update the posiion attributes
            target.setAttribute('data-x', x);
            target.setAttribute('data-y', y);
            [cx,cy] = [x,y]

            $(".pop-share .hint").fadeOut();
        }

        function updateView(op) {
            let zoom = op.zoom,
                rot = op.rotate;
            //console.log("zoom"+ op.zoom)
            if (zoom) {
                TweenMax.to($(".pop-share .upload"), .3, { scaleX: zoom, scaleY: zoom })
            }
            if (rot) {
                TweenMax.to($(".pop-share .upload"), .3, { rotation: rot })
            }

        }
        window.dragMoveListener = dragMoveListener;

    }
    this.init = function() {
        bind();
    }
    this.init();
}


