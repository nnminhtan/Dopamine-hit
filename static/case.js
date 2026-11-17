const track = document.querySelector('#track'), btn = document.querySelector('#openBtn'), statusEl = document.querySelector('#status');
const palette = [
    ['MP9 | Cobalt Grid', '#4b69ff'], 
    ['Glock-18 | Violet Circuit', '#8847ff'], 
    ['AK-47 | Neon Ember', '#d32ce6'], 
    ['AWP | Crimson Pulse', '#eb4b4b']
];
function card(n, c) { 
    let d = document.createElement('div'); 
    d.className = 'roll-item'; 
    d.style.setProperty('--c', c); 
    d.textContent = n; 
    return d 
}
async function openCase() { 
    btn.disabled = true; 
    statusEl.textContent = 'Opening...'; 
    track.innerHTML = ''; 
    track.style.transition = 'none'; 
    track.style.transform = 'translateX(0)'; 
    let res = await fetch('/api/open', { method: 'POST' }), winner = await res.json(); 
    let all = []; for (let i = 0; i < 52; i++) { 
        let x = palette[Math.floor(Math.random() * palette.length)]; all.push(x) 
    } all[46] = [winner.name, winner.color]; 
    all.forEach(x => track.append(card(x[0], x[1]))); 
    requestAnimationFrame(() => requestAnimationFrame(() => { 
        let w = track.children[0].getBoundingClientRect().width + 6; 
        let target = 46 * w - (document.querySelector('#reel').clientWidth / 2) + (w / 2); track.style.transition = 'transform 6.5s cubic-bezier(.08,.65,.15,1)'; 
        track.style.transform = `translateX(-${target}px)` })); 
        setTimeout(() => { statusEl.textContent = `You opened: ${winner.name} (${winner.rarity})`; 
        btn.disabled = false 
    }, 6600) 
}

btn.addEventListener('click', openCase);

document.querySelector('#casesTab').onclick = () => { cases.hidden = false; inventory.hidden = true };

document.querySelector('#invTab').onclick = async () => { cases.hidden = true; inventory.hidden = false; 
    let data = await (await fetch('/api/inventory')).json(), g = document.querySelector('#inventoryGrid'); 
    g.innerHTML = ''; 
    data.forEach(x => { let d = document.createElement('div'); 
        d.className = 'item'; d.style.setProperty('--c', x.color); 
        d.innerHTML = `<div class="art">◆</div><b>${x.name}</b><small>${x.rarity} · ${x.opened_at}</small>`; 
        g.append(d) }) 
    };