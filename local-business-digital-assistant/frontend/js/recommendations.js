async function loadRecommendations(){
 const data=await (await fetch('/api/recommendations')).json();
 document.getElementById('recommendations').innerHTML=data.map(x=>`
 <div class="rec ${x.type}"><h3>${x.title}</h3><p>${x.message}</p></div>`).join('');
}
async function askQuestion(){
 const q=document.getElementById('question').value.trim();
 if(!q)return;
 const r=await fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
 const d=await r.json();
 document.getElementById('answer').innerHTML=`<strong>📊 Business Insight</strong><p>${d.answer}</p>`;
}
loadRecommendations();
