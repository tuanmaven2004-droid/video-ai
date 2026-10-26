/* Own reusable graphics. GSAP is passed by caller; paused, seek-safe, no autoplay.
   Bind child timeline into the owning HyperFrames timeline at the cue start.
   Uses original designs; no copied reference assets. */
(function(root){
 root.REMotion={mount:function(gsap,element,kind,duration){
  if(!['hook','space','stat','amenity','closing'].includes(kind))throw Error('Unknown motion role');
  if(duration<1.2)throw Error('Insufficient reading time');
  const title=element.querySelector('[data-main]'),sub=element.querySelector('[data-sub]');
  const tl=gsap.timeline({paused:true});
  tl.set(element,{opacity:1},0);
  if(kind==='hook')tl.fromTo(title,{y:28,scale:.92,opacity:0},{y:0,scale:1,opacity:1,duration:.32,ease:'back.out(1.05)'},0);
  if(kind==='space')tl.fromTo(title,{x:-30,opacity:0},{x:0,opacity:1,duration:.24,ease:'power2.out'},0);
  if(kind==='stat')tl.fromTo(title,{scale:1.12,opacity:0},{scale:1,opacity:1,duration:.30,ease:'power2.out'},0);
  if(kind==='amenity')tl.fromTo(title,{y:18,opacity:0},{y:0,opacity:1,duration:.28,ease:'power2.out'},0);
  if(kind==='closing')tl.fromTo(title,{opacity:0},{opacity:1,duration:.32},0);
  if(sub)tl.fromTo(sub,{opacity:0,y:8},{opacity:1,y:0,duration:.22},.12);
  tl.to(element,{opacity:0,duration:.16},duration-.16);return tl;
 }};
})(typeof window==='undefined'?globalThis:window);
