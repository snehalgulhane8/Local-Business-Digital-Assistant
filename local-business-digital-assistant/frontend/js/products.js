async function loadProducts(){
 const data=await (await fetch('/api/products/top')).json();
 let html='<table><thead><tr><th>Product ID</th><th>Category</th><th>Revenue</th><th>Quantity</th></tr></thead><tbody>';
 data.forEach(x=>html+=`<tr><td>${x.product_id}</td><td>${x.category}</td><td>R$ ${Number(x.revenue).toFixed(2)}</td><td>${x.quantity}</td></tr>`);
 html+='</tbody></table>';
 document.getElementById('product-list').innerHTML=html;
}
loadProducts();
