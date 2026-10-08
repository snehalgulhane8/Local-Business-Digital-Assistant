async function loadCustomers(){
 const data=await (await fetch('/api/customers/top')).json();
 let html='<table><thead><tr><th>Customer ID</th><th>Total Spent</th><th>Orders</th></tr></thead><tbody>';
 data.forEach(x=>html+=`<tr><td>${x.customer_id}</td><td>R$ ${Number(x.total_spent).toFixed(2)}</td><td>${x.orders}</td></tr>`);
 html+='</tbody></table>';
 document.getElementById('customer-list').innerHTML=html;
}
loadCustomers();
