import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Envelope CSS
old_flap = """/* Envelope flap (top triangle) */
.env-flap{
  position:absolute;top:0;left:0;right:0;
  height:0;
  border-left:calc(min(360px,86vw)/2) solid transparent;
  border-right:calc(min(360px,86vw)/2) solid transparent;
  border-top:calc(min(250px,60vw)*0.44) solid var(--env-flap);
  z-index:5;
  transform-origin:top center;
  transform-style:preserve-3d;
  filter:drop-shadow(0 3px 6px rgba(180,60,100,0.15));
  transition:transform 1.4s cubic-bezier(0.4,0,0.2,1);
}
.env-flap::after{
  content:'';
  position:absolute;
  top:calc(-1 * min(250px,60vw)*0.44);
  left:calc(-1 * min(360px,86vw)/2);
  width:min(360px,86vw);
  height:calc(min(250px,60vw)*0.44);
  background:linear-gradient(180deg,rgba(255,255,255,0.2) 0%,rgba(240,160,180,0.1) 100%);
  clip-path:polygon(50% 100%,0% 0%,100% 0%);
  pointer-events:none;
}
.env-flap.open{transform:rotateX(-180deg);}

/* Bottom triangles (decorative crease lines) */
.env-bottom{
  position:absolute;bottom:0;left:0;right:0;
  height:0;
  border-left:calc(min(360px,86vw)/2) solid transparent;
  border-right:calc(min(360px,86vw)/2) solid transparent;
  border-bottom:calc(min(250px,60vw)*0.38) solid rgba(240,170,195,0.4);
  z-index:1;
}
.env-left{
  position:absolute;top:0;left:0;bottom:0;
  width:0;
  border-top:calc(min(250px,60vw)/2) solid transparent;
  border-bottom:calc(min(250px,60vw)/2) solid transparent;
  border-left:calc(min(360px,86vw)*0.3) solid rgba(245,180,200,0.25);
  z-index:1;
}
.env-right{
  position:absolute;top:0;right:0;bottom:0;
  width:0;
  border-top:calc(min(250px,60vw)/2) solid transparent;
  border-bottom:calc(min(250px,60vw)/2) solid transparent;
  border-right:calc(min(360px,86vw)*0.3) solid rgba(245,180,200,0.25);
  z-index:1;
}"""

new_flap = """/* Envelope flap (top triangle) */
.env-flap{
  position:absolute;top:0;left:0;width:100%;height:58%;
  background:var(--env-flap);
  clip-path:polygon(0 0, 100% 0, 50% 100%);
  z-index:6;
  transform-origin:top center;
  transition:transform 1.4s cubic-bezier(0.4,0,0.2,1);
  filter:drop-shadow(0 4px 6px rgba(180,60,100,0.25));
}
.env-flap::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(255,255,255,0.3) 0%,rgba(240,160,180,0.1) 100%);
  pointer-events:none;
}
.env-flap.open{transform:rotateX(-180deg);}

/* Bottom triangles (decorative crease lines) */
.env-bottom{
  position:absolute;bottom:0;left:0;width:100%;height:55%;
  background:linear-gradient(0deg,rgba(240,170,195,0.5),rgba(245,180,200,0.2));
  clip-path:polygon(0 100%, 100% 100%, 50% 0%);
  z-index:4;
}
.env-left{
  position:absolute;top:0;left:0;width:55%;height:100%;
  background:linear-gradient(90deg,rgba(245,180,200,0.4),rgba(250,190,210,0.1));
  clip-path:polygon(0 0, 0 100%, 100% 50%);
  z-index:3;
}
.env-right{
  position:absolute;top:0;right:0;width:55%;height:100%;
  background:linear-gradient(-90deg,rgba(245,180,200,0.4),rgba(250,190,210,0.1));
  clip-path:polygon(100% 0, 100% 100%, 0 50%);
  z-index:3;
}"""

content = content.replace(old_flap, new_flap)

# 2. Add Modal CSS before </head>
modal_css = """
/* ═══════════════════════════════════════════
   MEDIA MODAL
═══════════════════════════════════════════ */
.media-modal {
  display: none; position: fixed; z-index: 10000; inset: 0; background: rgba(0,0,0,0.85);
  align-items: center; justify-content: center; backdrop-filter: blur(8px);
  opacity: 0; transition: opacity 0.4s ease;
}
.media-modal.active { display: flex; opacity: 1; }
.media-modal-content {
  position: relative; max-width: 95vw; max-height: 90vh; background: var(--card-bg);
  padding: 1rem; border-radius: 16px; border: 1.5px solid var(--glass-b);
  box-shadow: 0 15px 50px rgba(0,0,0,0.6); overflow: hidden;
  display: flex; flex-direction: column; align-items: center; transform: scale(0.9);
  transition: transform 0.4s cubic-bezier(0.34,1.56,0.64,1);
}
.media-modal.active .media-modal-content { transform: scale(1); }
.close-modal {
  position: absolute; top: 12px; right: 18px; font-size: 2.5rem; color: #fff; cursor: pointer;
  text-shadow: 0 0 10px rgba(0,0,0,0.6); z-index: 10; transition: color 0.3s ease;
}
.close-modal:hover { color: var(--p4); }
.media-container {
  display: flex; gap: 1rem; overflow-x: auto; max-width: 100%; max-height: 80vh; padding-bottom: 10px;
  scroll-snap-type: x mandatory;
}
.media-container::-webkit-scrollbar { height: 8px; }
.media-container::-webkit-scrollbar-track { background: rgba(255,255,255,0.1); border-radius: 4px; }
.media-container::-webkit-scrollbar-thumb { background: var(--p3); border-radius: 4px; }
.media-item { flex-shrink: 0; text-align: center; scroll-snap-align: center; position: relative; }
.media-item img, .media-item video {
  max-width: 100%; max-height: 75vh; border-radius: 8px; object-fit: contain; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
"""
content = content.replace('</head>', modal_css + '\n</head>')

# 3. Update Memory Grid HTMl
old_grid = """<div class="memories-grid">
      <div class="memory-card reveal rd1"><div class="memory-icon">📸</div><div class="memory-label">Our Memories</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd2"><div class="memory-icon">🌙</div><div class="memory-label">Late Night Talks</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd3"><div class="memory-icon">🌸</div><div class="memory-label">Sweet Moments</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd1"><div class="memory-icon">✨</div><div class="memory-label">Magic Between Us</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd2"><div class="memory-icon">🎵</div><div class="memory-label">Songs &amp; Smiles</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd3"><div class="memory-icon">💌</div><div class="memory-label">Every Little Thing</div><div class="memory-soon">Coming Soon…</div></div>
    </div>"""

new_grid = """<div class="memories-grid">
      <div class="memory-card reveal rd1" onclick="openModal('memories')"><div class="memory-icon">📸</div><div class="memory-label">Our Memories</div><div class="memory-soon">Click to view 🩷</div></div>
      <div class="memory-card reveal rd2" onclick="openModal('late_night')"><div class="memory-icon">🌙</div><div class="memory-label">Late Night Talks</div><div class="memory-soon">Click to view 🩷</div></div>
      <div class="memory-card reveal rd3" onclick="openModal('funny')"><div class="memory-icon">😂</div><div class="memory-label">Our Funny Moments</div><div class="memory-soon">Click to view 🩷</div></div>
      <div class="memory-card reveal rd1"><div class="memory-icon">✨</div><div class="memory-label">Magic Between Us</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd2"><div class="memory-icon">🎵</div><div class="memory-label">Songs &amp; Smiles</div><div class="memory-soon">Coming Soon…</div></div>
      <div class="memory-card reveal rd3"><div class="memory-icon">💌</div><div class="memory-label">Every Little Thing</div><div class="memory-soon">Coming Soon…</div></div>
    </div>"""
content = content.replace(old_grid, new_grid)

# 4. Add Modal HTML before scripts
modal_html = """
<!-- ════════════════════════════════════
     MEDIA MODAL
════════════════════════════════════ -->
<div id="media-modal" class="media-modal">
  <div class="media-modal-content">
    <span class="close-modal" onclick="closeModal()">&times;</span>
    <div id="modal-body"></div>
  </div>
</div>
"""
content = content.replace('<!-- ══════════════ SCRIPT ══════════════ -->', modal_html + '\n<!-- ══════════════ SCRIPT ══════════════ -->')


# 5. Update MSG and Typing logic
old_msg = """const MSG = "I may not know all your dreams yet, but I promise this — I will support you in every step you take. Every decision you make, I will stand beside you. Until the day I die, I will be with you, supporting you until you achieve everything your heart desires.";
let typingDone = false;

function startTyping(){
  if(typingDone) return; typingDone = true;
  const el = document.getElementById('typing-text');
  el.innerHTML = '<span class="cursor"></span>';
  let i = 0;
  const iv = setInterval(()=>{
    if(i < MSG.length){
      el.innerHTML = MSG.slice(0,++i) + '<span class="cursor"></span>';
    } else {
      clearInterval(iv);
      setTimeout(()=>{ const c=document.querySelector('.cursor'); if(c) c.style.display='none'; },2000);
      // Switch to Best Part when love message done
      if(musicUnlocked) switchTrack('p2', 22, 2200);
      setHBPhase('medium');
    }
  }, 47);
}"""

new_msg = """const MSG = `Happy Anniversary My Baby<br><br>My Dearest Ephiii,<br><br>Happy Anniversary!! 🎉 I really wanna start things first by thanking you my princess, if you didn't make the first move I wouldn't be where I am today with you, if they didn't provoke you and dared you that day we wouldn't be existing 😫 ughhh how grateful I am for those incidents. Looking back on our time together, I am constantly amazed by how much we've grown–both as individuals and as a team, life is just better with you by my side and I am blessed for it everyday. And you did your absolute part in it whether by rage-baiting me, loving me, bullying me mnamn...... I'm really blessed for you to have you as my girlfriend, I particularly would appreciate it gn if you were like letting me on your things like you do dero also I love & lil hate how you silence me during an argument (savage way btw), I feel I'm at my safe place when I'm with you, sometimes feel loved & seen.<br><br>I love your personalities all of em even tho I haven't yet seen the weird ones & ughhh your whole presence makes me feel high like I am floating above all, I love every bit of youuu.<br>Like you said it yourself I will definitely choose you in every life time I can think of.<br><br>You're My partner in crime<br>My missing ribs<br>My home<br>My wifeyyy<br>My everything<br><br>This website can't even express a quarter of feelings I have for you mi vida you deserve every single ounce of the world and this website is the least I can do for you babyyy. I may not know all your dreams yet, but I promise this — I will support you in every step you take. Every decision you make, I will stand beside you. Until the day I die, I will be with you, supporting you until you achieve everything your heart desires.<br><br>In this world the rest can wait it's just You and I. You're the most amazing person in da world babes<br><br>I Love you so much my wife! MWAHHHHH 💋💍`;

let typingDone = false;

function startTyping(){
  if(typingDone) return; typingDone = true;
  const el = document.getElementById('typing-text');
  el.innerHTML = '<span class="cursor"></span>';
  let i = 0;
  let text = '';
  let isTag = false;
  
  const iv = setInterval(()=>{
    if(i < MSG.length){
      text += MSG[i];
      if(MSG[i] === '<') isTag = true;
      if(MSG[i] === '>') isTag = false;
      i++;
      if(!isTag){
        el.innerHTML = text + '<span class="cursor"></span>';
      }
    } else {
      clearInterval(iv);
      setTimeout(()=>{ const c=document.querySelector('.cursor'); if(c) c.style.display='none'; },2000);
      // Switch to Best Part when love message done
      if(musicUnlocked) switchTrack('p2', 22, 2200);
      setHBPhase('medium');
    }
  }, 20); // Faster typing for the long essay
}"""

content = content.replace(old_msg, new_msg)

# 6. Add Modal JS and Autoplay JS
new_js = """
/* ─────────────────────────────────────
   MEDIA MODAL
───────────────────────────────────── */
const MEDIA_DATA = {
  'memories': [
    { type: 'video', src: 'pics and vids/first time we met.mp4' },
    { type: 'image', src: 'pics and vids/last time we met.jpg' }
  ],
  'late_night': [
    { type: 'image', src: 'pics and vids/old late night talks.jpg' },
    { type: 'image', src: 'pics and vids/old late night talks2.jpg' }
  ],
  'funny': [
    { type: 'image', src: 'pics and vids/old late night talks.jpg' }
  ]
};

function openModal(id) {
  const modal = document.getElementById('media-modal');
  const body = document.getElementById('modal-body');
  body.innerHTML = '';
  
  if (MEDIA_DATA[id]) {
    const container = document.createElement('div');
    container.className = 'media-container';
    
    MEDIA_DATA[id].forEach(media => {
      const item = document.createElement('div');
      item.className = 'media-item';
      if (media.type === 'video') {
        const vid = document.createElement('video');
        vid.src = media.src;
        vid.controls = true;
        vid.autoplay = true;
        vid.loop = true;
        vid.style.maxHeight = '75vh';
        item.appendChild(vid);
      } else {
        const img = document.createElement('img');
        img.src = media.src;
        item.appendChild(img);
      }
      container.appendChild(item);
    });
    body.appendChild(container);
    modal.classList.add('active');
  }
}

function closeModal() {
  const modal = document.getElementById('media-modal');
  modal.classList.remove('active');
  const videos = modal.querySelectorAll('video');
  videos.forEach(v => v.pause());
}

document.getElementById('media-modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

/* ─────────────────────────────────────
   AUTOPLAY BACKGROUND MUSIC
───────────────────────────────────── */
let autoPlayed = false;
function tryAutoPlay() {
  if (autoPlayed) return;
  // Automatically start Get You if not started
  ['p1','p2','p3'].forEach(id => {
    try { PLAYERS[id].volume = 0; PLAYERS[id].play().then(() => PLAYERS[id].pause()).catch(()=>{}); } catch(_){}
  });
  switchTrack('p1', 20, 1500);
  autoPlayed = true;
  musicUnlocked = true;
}
document.addEventListener('click', tryAutoPlay, {once: true});
document.addEventListener('touchstart', tryAutoPlay, {once: true});
window.addEventListener('load', () => {
  try {
    PLAYERS['p1'].volume = 0;
    PLAYERS['p1'].play().then(() => {
      fadeVol(PLAYERS['p1'], 0, 20, 1500);
      autoPlayed = true;
      musicUnlocked = true;
    }).catch(()=>{});
  } catch(e){}
});
"""

# inject at the bottom of script
content = content.replace('</script>', new_js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

