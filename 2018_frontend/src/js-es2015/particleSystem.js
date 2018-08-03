
export {
    particleSystem as particleSystem
}
class particleSystem {
    constructor() {
        //this.init();
        this.state = 'play';

        this.init();
        this.Puase = this.Pause.bind(this)
    }

    init() {
    const context = this;
    this.group = new THREE.Group();
    this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000);
    var group = this.group
    var camera = this.camera
    var container, stats;
    var particlesData = [];
    var  scene, renderer;
    var positions, colors;
    var particles;
    var pointCloud;
    var particlePositions,ParticleAlphas;
    var linesMesh;

    var maxParticleCount = 100;
    var particleCount = 50;
    var r = (window.innerWidth > window.innerHeight)? window.innerWidth *1: window.innerHeight*1;
    var rHalf = r / 2;

    var effectController = {
        showDots: true,
        showLines: false,
        minDistance: 120,
        limitConnections: true,
        maxConnections: 30,
        particleCount: 50
    };
    


    init();
    //TweenMax.to(Rot , 3,{delay:1.5,speed : 0.01 , ease:Sine.easeOut})
    animate();
   
    function initGUI() {

        var gui = new dat.GUI();

        gui.add(effectController, "showDots").onChange(function(value) { pointCloud.visible = value; });
        gui.add(effectController, "showLines").onChange(function(value) { linesMesh.visible = value; });
        gui.add(effectController, "minDistance", 10, 300);
        gui.add(effectController, "limitConnections");
        gui.add(effectController, "maxConnections", 0, 30, 1);
        gui.add(effectController, "particleCount", 0, maxParticleCount, 1).onChange(function(value) {

            particleCount = parseInt(value);
            particles.setDrawRange(0, particleCount);

        });

    }

    function init() {

        initGUI();
        dat.GUI.toggleHide();
        container = document.getElementById('bg-stars');

        //

       // camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000);
        camera.position.z = 0;

        //var controls = new THREE.OrbitControls(camera, container);

        scene = new THREE.Scene();


       
        scene.add(group);

        // var helper = new THREE.BoxHelper(new THREE.Mesh(new THREE.BoxGeometry(r, r, r)));
        // helper.material.color.setHex(0x080808);
        // helper.material.blending = THREE.AdditiveBlending;
        // helper.material.transparent = true;
        // group.add(helper);

        var segments = maxParticleCount * maxParticleCount;

        positions = new Float32Array(segments * 3);
        colors = new Float32Array(segments * 3);
        let sprite= new THREE.TextureLoader().load( "img/dest/0330/star.png" );
        var pMaterial = new THREE.PointsMaterial({
            
            size: 18,
            blending: THREE.AdditiveBlending,
            map:sprite,
            transparent: true,
            sizeAttenuation: true
        });

        particles = new THREE.BufferGeometry();
        particlePositions = new Float32Array(maxParticleCount * 3);
        ParticleAlphas = new Float32Array( maxParticleCount * 1 );
        for (var i = 0; i < maxParticleCount; i++) {

            var x = (Math.random()>.85)?Math.random() * r - r *.5 : Math.random() * r * .5 - r *.4;
            var y = (Math.random()>.75)?Math.random() * r *.2 - r * 0.05:(Math.random() * r *.2 - r * 0.05)*.5;
            var z = Math.random() * r - r *.5;

            particlePositions[i * 3] = x;
            particlePositions[i * 3 + 1] = y;
            particlePositions[i * 3 + 2] = z;

            ParticleAlphas[i]= Math.random();

            // add it to the geometry
            particlesData.push({
                velocity: new THREE.Vector3(-.1+ Math.random() * .2, -.1+ Math.random() * .2, -0.05+ Math.random() * .1),
                numConnections: 0
            });

        }

        particles.setDrawRange(0, particleCount);
        particles.addAttribute('position', new THREE.BufferAttribute(particlePositions, 3).setDynamic(true));
        particles.addAttribute('alpha', new THREE.BufferAttribute(ParticleAlphas, 1).setDynamic(true));
        

        // create the particle system
        pointCloud = new THREE.Points(particles, pMaterial);
        group.add(pointCloud);


        var geometry = new THREE.BufferGeometry();

        geometry.addAttribute('position', new THREE.BufferAttribute(positions, 3).setDynamic(true));
        geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3).setDynamic(true));

        geometry.computeBoundingSphere();

        geometry.setDrawRange(0, 0);
        //8eb1fa
        var material = new THREE.LineBasicMaterial({
        	color: 0Xffffff, 
            vertexColors: THREE.VertexColors,
            blending: THREE.AdditiveBlending,
            transparent: true
        });

        linesMesh = new THREE.LineSegments(geometry, material);
        group.add(linesMesh);

        //

        renderer = new THREE.WebGLRenderer({ antialias: true , alpha:true});
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);

        renderer.gammaInput = true;
        renderer.gammaOutput = true;

        container.appendChild(renderer.domElement);

        //

        // stats = new Stats();
        // container.appendChild(stats.dom);

        window.addEventListener('resize', onWindowResize, false);

    }

    function onWindowResize() {

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(window.innerWidth, window.innerHeight);

    }

   

    function animate() {

        var vertexpos = 0;
        var colorpos = 0;
        var numConnected = 0;

        for (var i = 0; i < particleCount; i++)
            particlesData[i].numConnections = 0;

        for (var i = 0; i < particleCount; i++) {

            // get the particle
            var particleData = particlesData[i];

            particlePositions[i * 3] += particleData.velocity.x;
            particlePositions[i * 3 + 1] += particleData.velocity.y;
            particlePositions[i * 3 + 2] += particleData.velocity.z;


            if (particlePositions[i * 3 + 1] < -rHalf || particlePositions[i * 3 + 1] > rHalf)
                particleData.velocity.y = -particleData.velocity.y;

            if (particlePositions[i * 3] < -rHalf || particlePositions[i * 3] > rHalf)
                particleData.velocity.x = -particleData.velocity.x;

            if (particlePositions[i * 3 + 2] < -rHalf || particlePositions[i * 3 + 2] > rHalf)
                particleData.velocity.z = -particleData.velocity.z;

            if (effectController.limitConnections && particleData.numConnections >= effectController.maxConnections)
                continue;

            // Check collision
            for (var j = i + 1; j < particleCount; j++) {

                var particleDataB = particlesData[j];
                if (effectController.limitConnections && particleDataB.numConnections >= effectController.maxConnections)
                    continue;
                //console.log("line")
                var dx = particlePositions[i * 3] - particlePositions[j * 3];
                var dy = particlePositions[i * 3 + 1] - particlePositions[j * 3 + 1];
                var dz = particlePositions[i * 3 + 2] - particlePositions[j * 3 + 2];
                var dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                if (dist < effectController.minDistance && effectController.showLines) {

                    particleData.numConnections++;
                    particleDataB.numConnections++;

                    var alpha = 1.0 - dist / effectController.minDistance;

                    positions[vertexpos++] = particlePositions[i * 3];
                    positions[vertexpos++] = particlePositions[i * 3 + 1];
                    positions[vertexpos++] = particlePositions[i * 3 + 2];

                    positions[vertexpos++] = particlePositions[j * 3];
                    positions[vertexpos++] = particlePositions[j * 3 + 1];
                    positions[vertexpos++] = particlePositions[j * 3 + 2];

                    colors[colorpos++] = alpha;
                    colors[colorpos++] = alpha;
                    colors[colorpos++] = alpha;

                    colors[colorpos++] = alpha;
                    colors[colorpos++] = alpha;
                    colors[colorpos++] = alpha;

                    numConnected++;
                }
            }
        }


        linesMesh.geometry.setDrawRange(0, numConnected * 2);
        linesMesh.geometry.attributes.position.needsUpdate = true;
        linesMesh.geometry.attributes.color.needsUpdate = true;

        pointCloud.geometry.attributes.position.needsUpdate = true;

        pointCloud.geometry.attributes.alpha.needsUpdate = true;

        requestAnimationFrame(animate);

        //stats.update();
        render();
    }
    //let ospeed = 1;
    
    //this.Rspeed = 1
   
    let speed= .013;
    let ospeed = .013;        
    
    function render() {
        var time = Date.now() * 0.000001;
        // console.log("Rspeed ...." + speed)
        // speed += (0.01 - ospeed) * 0.35;
        
        // group.rotation.y = time * speed;
        if(context.state!="play"){return;}
        
        renderer.render(scene, camera);        

        //ospeed = speed

    }
    
    
}

setAnimScale(from,t=1){
        const group = this.group;
        TweenMax.fromTo(group.scale ,t , {x:from,z:from},{delay:0,x:1,z:1,ease:Expo.easeOut})
    }
setAnimRotate(from,to , t=1 ,d=1){
    const group = this.group;
    if(from){
        TweenMax.fromTo(group.rotation ,t , {y:from},{delay:d,y:to,ease:Expo.easeOut}) 
    }else{
        TweenMax.to(group.rotation ,t ,{delay:d,y:to,ease:Expo.easeOut}) 
    }
}
setCamRotate(from,to , t=1){
    const camera = this.camera;
    if(from){
        TweenMax.fromTo(camera.rotation ,t , {y:from},{delay:0,y:to,ease:Sine.easeInOut}) 
    }else{
        TweenMax.to(camera.rotation ,t ,{delay:0,y:to,ease:Sine.easeInOut}) 
    }
}

setCamZoom(from,to , t=1 , d=1){
        const camera = this.camera;
     if(from){
        TweenMax.fromTo(camera.position ,t , {z:from},{delay:d,z:to,ease:Expo.easeOut}) 
    }else{
        TweenMax.to(camera.position ,t ,{delay:d,z:to,ease:Expo.easeOut}) 
    }
}
Pause(){
    this.state = 'pause'
}

}