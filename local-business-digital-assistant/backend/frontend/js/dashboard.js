async function loadDashboard(){
 try{
  const d=await (await fetch('/api/dashboard')).json();
  document.getElementById('revenue').textContent='R$ '+Number(d.total_revenue).toLocaleString();
  document.getElementById('orders').textContent=Number(d.total_orders).toLocaleString();
  document.getElementById('customers').textContent=Number(d.total_customers).toLocaleString();
  document.getElementById('average-order').textContent='R$ '+Number(d.average_order_value).toLocaleString();
  loadSalesChart(); loadCategoryChart(); loadInsights();
 }catch(e){console.error(e)}
}
async function loadSalesChart(){
 const d=await (await fetch('/api/sales/monthly')).json();
 new Chart(document.getElementById('salesChart'),{type:'line',data:{labels:d.map(x=>x.month),datasets:[{label:'Sales',data:d.map(x=>x.sales),borderWidth:2,tension:.25}]},options:{responsive:true}});
}
async function loadCategoryChart(){
 const d=await (await fetch('/api/categories')).json();
 new Chart(document.getElementById('categoryChart'),{type:'bar',data:{labels:d.map(x=>x.category),datasets:[{label:'Revenue',data:d.map(x=>x.sales),borderWidth:1}]},options:{indexAxis:'y',responsive:true}});
}
async function loadInsights(){
 const d=await (await fetch('/api/insights')).json();
 document.getElementById('insights').innerHTML=d.insights.map(x=>`<div class="rec info">${x}</div>`).join('');
}
loadDashboard();
