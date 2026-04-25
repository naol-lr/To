import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the typing MSG
old_msg = r'const MSG = "I may not know all your dreams yet, but I promise this — I will support you in every step you take\. Every decision you make, I will stand beside you\. Until the day I die, I will be with you, supporting you until you achieve everything your heart desires\.";'

new_msg = r'''const MSG = `Happy Anniversary My Baby<br><br>My Dearest Ephiii,<br><br>Happy Anniversary!! 🎉 I really wanna start things first by thanking you my princess, if you didn't make the first move I wouldn't be where I am today with you, if they didn't provoke you and dared you that day we wouldn't be existing 😫 ughhh how grateful I am for those incidents. Looking back on our time together, I am constantly amazed by how much we've grown–both as individuals and as a team, life is just better with you by my side and I am blessed for it everyday. And you did your absolute part in it whether by rage-baiting me, loving me, bullying me mnamn...... I'm really blessed for you to have you as my girlfriend, I particularly would appreciate it gn if you were like letting me on your things like you do dero also I love & lil hate how you silence me during an argument (savage way btw), I feel I'm at my safe place when I'm with you, sometimes feel loved & seen.<br>I love your personalities all of em even tho I haven't yet seen the weird ones & ughhh your whole presence makes me feel high like I am floating above all, I love every bit of youuu.<br>Like you said it yourself I will definitely choose you in every life time I can think of.<br>You're My partner in crime <br>            My missing ribs<br>            My home<br>            My wifeyyy <br>            My everything <br>This website can't even express a quarter of feelings I have for you mi vida you deserve every single ounce of the world and this website is the least I can do for you babyyy. I may not know all your dreams yet, but I promise this — I will support you in every step you take. Every decision you make, I will stand beside you. Until the day I die, I will be with you, supporting you until you achieve everything your heart desires.<br><br>In this world the rest can wait it's just You and I.   You're the most amazing person in da world babes<br> <br>I Love you so much my wife! MWAHHHHH 💋💍`;'''

content = content.replace(old_msg, new_msg)

# 2. Update typing speed and logic to support <br>
typing_func_old = r'''function startTyping\(\)\{
  if\(typingDone\) return; typingDone = true;
  const el = document\.getElementById\('typing-text'\);
  el\.innerHTML = '<span class="cursor"></span>';
  let i = 0;
  const iv = setInterval\(\(\)=>\{
    if\(i < MSG\.length\)\{
      el\.innerHTML = MSG\.slice\(0,\+\+i\) \+ '<span class="cursor"></span>';
    \} else \{
      clearInterval\(iv\);
      setTimeout\(\(\)=>\{ const c=document\.querySelector\('\.cursor'\); if\(c\) c\.style\.display='none'; \},2000\);
      // Switch to Best Part when love message done
      if\(musicUnlocked\) switchTrack\('p2', 22, 2200\);
      setHBPhase\('medium'\);
    \}
  \}, 47\);
\}'''

typing_func_new = r'''function startTyping(){
  if(typingDone) return; typingDone = true;
  const el = document.getElementById('typing-text');
  el.innerHTML = '<span class="cursor"></span>';
  
  // Parse the MSG and display it character by character smoothly and faster
  // while handling HTML tags instantly
  let i = 0;
  let currentHTML = "";
  let isTag = false;
  
  const iv = setInterval(() => {
    if (i < MSG.length) {
      if (MSG[i] === '<') isTag = true;
      currentHTML += MSG[i];
      if (MSG[i] === '>') isTag = false;
      
      if (!isTag) {
        el.innerHTML = currentHTML + '<span class="cursor"></span>';
      }
      i++;
    } else {
      clearInterval(iv);
      setTimeout(()=>{ const c=document.querySelector('.cursor'); if(c) c.style.display='none'; },2000);
      if(musicUnlocked) switchTrack('p2', 30, 800);
      setHBPhase('medium');
    }
  }, 15); // Super fast 15ms delay for long text
}'''

content = re.sub(typing_func_old, typing_func_new, content)


# 3. Add modal HTML just before </body>
modal_html = r'''
<!-- ════════ GALLERY MODAL ════════ -->
<div id="gallery-modal" class="modal">
  <div class="modal-content">
    <span class="close-btn" onclick="closeGallery()">✕</span>
    <div id="gallery-media"></div>
  </div>
</div>
</body>
'''
content = content.replace('</body>', modal_html)

# 4. Add modal CSS
modal_css = r'''
/* ═══════════════════════════════════════════
   MODAL CSS
═══════════════════════════════════════════ */
.modal {
  display: none; position: fixed; z-index: 10000; inset: 0;
  background: rgba(0,0,0,0.85); backdrop-filter: blur(15px);
  align-items: center; justify-content: center;
  opacity: 0; transition: opacity 0.4s ease;
}
.modal.visible { display: flex; opacity: 1; }
.modal-content {
  position: relative; width: 90vw; max-width: 800px; max-height: 90vh;
  background: var(--card-bg); border-radius: 16px; padding: 1.5rem;
  box-shadow: 0 15px 50px rgba(0,0,0,0.6);
  border: 1px solid var(--glass-b);
  display: flex; flex-direction: column; align-items: center;
  overflow-y: auto;
}
.close-btn {
  position: absolute; top: 12px; right: 20px; font-size: 2rem;
  color: var(--text); cursor: pointer; z-index: 10;
  transition: transform 0.3s ease;
}
.close-btn:hover { transform: scale(1.2) rotate(90deg); color: var(--p5); }
#gallery-media {
  width: 100%; display: flex; flex-direction: column; gap: 1rem; align-items: center;
  margin-top: 2rem;
}
#gallery-media img, #gallery-media video {
  max-width: 100%; max-height: 70vh; border-radius: 12px;
  object-fit: contain; box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

</style>
'''
content = content.replace('</style>', modal_css)

# 5. Add onClick events to Memory Cards
card_replacements = [
    (r'<div class="memory-card reveal rd1"><div class="memory-icon">📸</div><div class="memory-label">Our Memories</div><div class="memory-soon">Coming Soon…</div></div>',
     r'<div class="memory-card reveal rd1" onclick="openGallery(\'memories\')" style="cursor:pointer;"><div class="memory-icon">📸</div><div class="memory-label">Our Memories</div><div class="memory-soon" style="color:var(--p5); font-weight:600;">Tap to view</div></div>'),
     
    (r'<div class="memory-card reveal rd2"><div class="memory-icon">🌙</div><div class="memory-label">Late Night Talks</div><div class="memory-soon">Coming Soon…</div></div>',
     r'<div class="memory-card reveal rd2" onclick="openGallery(\'latenight\')" style="cursor:pointer;"><div class="memory-icon">🌙</div><div class="memory-label">Late Night Talks</div><div class="memory-soon" style="color:var(--p5); font-weight:600;">Tap to view</div></div>'),
     
    (r'<div class="memory-card reveal rd3"><div class="memory-icon">🌸</div><div class="memory-label">Sweet Moments</div><div class="memory-soon">Coming Soon…</div></div>',
     r'<div class="memory-card reveal rd3" onclick="openGallery(\'sweet\')" style="cursor:pointer;"><div class="memory-icon">🌸</div><div class="memory-label">Sweet Moments</div><div class="memory-soon" style="color:var(--p5); font-weight:600;">Tap to view</div></div>'),

    (r'<div class="memory-card reveal rd1"><div class="memory-icon">✨</div><div class="memory-label">Magic Between Us</div><div class="memory-soon">Coming Soon…</div></div>',
     r'<div class="memory-card reveal rd1" onclick="openGallery(\'magic\')" style="cursor:pointer;"><div class="memory-icon">✨</div><div class="memory-label">Magic Between Us</div><div class="memory-soon" style="color:var(--p5); font-weight:600;">Tap to view</div></div>'),

    (r'<div class="memory-card reveal rd2"><div class="memory-icon">🎵</div><div class="memory-label">Songs &amp; Smiles</div><div class="memory-soon">Coming Soon…</div></div>',
     r'<div class="memory-card reveal rd2" onclick="openGallery(\'songs\')" style="cursor:pointer;"><div class="memory-icon">🎵</div><div class="memory-label">Songs &amp; Smiles</div><div class="memory-soon" style="color:var(--p5); font-weight:600;">Tap to view</div></div>'),

    (r'<div class="memory-card reveal rd3"><div class="memory-icon">💌</div><div class="memory-label">Every Little Thing</div><div class="memory-soon">Coming Soon…</div></div>',
     r'<div class="memory-card reveal rd3" onclick="openGallery(\'funny\')" style="cursor:pointer;"><div class="memory-icon">💌</div><div class="memory-label">Our Funny Moments</div><div class="memory-soon" style="color:var(--p5); font-weight:600;">Tap to view</div></div>'),
]
for old, new in card_replacements:
    content = content.replace(old, new)


# 6. Add JS functions for Gallery
gallery_js = r'''
const GALLERY_DATA = {
  memories: [
    { type: 'video', src: 'pics and vids/first time we met.mp4' },
    { type: 'image', src: 'pics and vids/last time we met.jpg' }
  ],
  latenight: [
    { type: 'image', src: 'pics and vids/old late night talks.jpg' },
    { type: 'image', src: 'pics and vids/old late night talks2.jpg' }
  ],
  funny: [
    { type: 'image', src: 'pics and vids/old late night talks.jpg' }
  ]
};

function openGallery(id) {
  const modal = document.getElementById('gallery-modal');
  const media = document.getElementById('gallery-media');
  media.innerHTML = '';
  
  const items = GALLERY_DATA[id] || [];
  if(items.length === 0) {
    media.innerHTML = '<p style="font-family:\'Dancing Script\', cursive; font-size:1.5rem; color:var(--text);">More memories loading soon... 🩷</p>';
  }
  
  items.forEach(item => {
    if (item.type === 'video') {
      const vid = document.createElement('video');
      vid.src = item.src;
      vid.controls = true;
      vid.autoplay = true;
      vid.loop = true;
      vid.volume = 0.6;
      vid.onplay = () => { if(currentAudio) fadeVol(currentAudio, currentAudio.volume*100, 15, 500); };
      vid.onpause = () => { if(currentAudio) fadeVol(currentAudio, currentAudio.volume*100, 35, 500); };
      media.appendChild(vid);
    } else {
      const img = document.createElement('img');
      img.src = item.src;
      media.appendChild(img);
    }
  });
  
  modal.style.display = 'flex';
  setTimeout(() => modal.classList.add('visible'), 10);
}

function closeGallery() {
  const modal = document.getElementById('gallery-modal');
  modal.classList.remove('visible');
  
  // Stop any videos playing
  const vids = document.querySelectorAll('#gallery-media video');
  vids.forEach(v => { v.pause(); v.src = ''; });
  
  setTimeout(() => { 
    modal.style.display = 'none'; 
    document.getElementById('gallery-media').innerHTML = ''; 
    if(currentAudio) fadeVol(currentAudio, currentAudio.volume*100, 35, 800);
  }, 400);
}
</script>
'''
content = content.replace('</script>', gallery_js, 1)


# 7. Speed up switchTrack delays overall and remove delays
content = content.replace("switchTrack('p1', 20, 1500);", "switchTrack('p1', 35, 600);")
content = content.replace("switchTrack('p2', 22, 2000);", "switchTrack('p2', 35, 600);")
content = content.replace("switchTrack('p2', 22, 2200);", "switchTrack('p2', 35, 600);")
content = content.replace("switchTrack('p3', 10, 2800); setTimeout(()=>{ fadeVol(PLAYERS['p3'],10,28,7000); },3000);", "switchTrack('p3', 35, 800);")

content = content.replace("fadeVol(currentAudio, v, 0, 1200);", "fadeVol(currentAudio, v, 0, 500);")
content = content.replace("switchTrack('p1',18,2000);", "switchTrack('p1',35,600);")

# Update Envelope CSS to make it more attractive and responsive
env_css_old = r'''.env-back\{
  position:absolute;inset:0;
  background:var\(--env-back\);
  border-radius:8px 8px 10px 10px;
  box-shadow:0 20px 60px rgba\(200,80,120,0\.18\),0 8px 24px rgba\(200,80,120,0\.12\),inset 0 1px 0 rgba\(255,255,255,0\.5\);
  overflow:hidden;
\}'''

env_css_new = r'''.env-back{
  position:absolute;inset:0;
  background:var(--env-back);
  border-radius:12px;
  box-shadow:0 30px 60px rgba(0,0,0,0.25), inset 0 2px 10px rgba(255,255,255,0.4);
  overflow:hidden;
}'''
content = re.sub(env_css_old, env_css_new, content)

flap_css_old = r'''transition:transform 1\.4s cubic-bezier\(0\.4,0,0\.2,1\);'''
flap_css_new = r'''transition:transform 1.2s cubic-bezier(0.34,1.56,0.64,1);'''
content = content.replace(flap_css_old, flap_css_new)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
