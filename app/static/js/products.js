let editingSku = null;

// Load all products
async function loadProducts() {
  let search = document.getElementById("search-box").value;

  let res = await fetch(`/products/?search=${search}`);
  let data = await res.json();

  let tbody = document.querySelector("#product-table tbody");
  tbody.innerHTML = "";

  data.products.forEach((p) => {
    tbody.innerHTML += `
            <tr>
                <td>${p.sku}</td>
                <td>${p.name}</td>
                <td>${p.description}</td>
                <td>${p.price}</td>
                <td>${p.active}</td>
                <td class="actions">
                    <button onclick="editProduct('${p.sku}', '${p.name}', '${p.description}', ${p.price})">Edit</button>
                    <button onclick="deleteProduct('${p.sku}')">Delete</button>
                </td>
            </tr>
        `;
  });
}

function showCreateForm() {
  editingSku = null;
  document.getElementById("form-title").innerText = "Create Product";
  document.getElementById("form-container").style.display = "block";

  document.getElementById("sku").value = "";
  document.getElementById("name").value = "";
  document.getElementById("description").value = "";
  document.getElementById("price").value = "";
}

function editProduct(sku, name, desc, price) {
  editingSku = sku;

  document.getElementById("form-title").innerText = "Update Product";
  document.getElementById("form-container").style.display = "block";

  document.getElementById("sku").value = sku;
  document.getElementById("name").value = name;
  document.getElementById("description").value = desc;
  document.getElementById("price").value = price;
}

function hideForm() {
  document.getElementById("form-container").style.display = "none";
}

// Create or Update product
async function submitForm() {
  let sku = document.getElementById("sku").value;
  let name = document.getElementById("name").value;
  let description = document.getElementById("description").value;
  let price = document.getElementById("price").value;

  if (!sku || !name || !price) {
    alert("Fill SKU, Name & Price");
    return;
  }

  let payload = { name, description, price: Number(price) };

  if (editingSku) {
    // UPDATE
    await fetch(`/products/${editingSku}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    alert("Product updated!");
  } else {
    // CREATE
    payload["sku"] = sku;
    await fetch("/products/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    alert("Product created!");
  }

  hideForm();
  loadProducts();
}

// DELETE
async function deleteProduct(sku) {
  if (!confirm("Delete this product?")) return;

  await fetch(`/products/${sku}`, { method: "DELETE" });

  alert("Deleted");
  loadProducts();
}

// Auto-load on page open
loadProducts();
