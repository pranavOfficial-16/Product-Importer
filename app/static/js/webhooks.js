async function loadWebhooks() {
  let res = await fetch("/webhooks/");
  let data = await res.json();

  let tbody = document.querySelector("#webhook-table tbody");
  tbody.innerHTML = "";

  data.forEach((w) => {
    tbody.innerHTML += `
            <tr>
                <td>${w.url}</td>
                <td>${w.event}</td>
                <td>${w.enabled}</td>
                <td>
                    <button onclick="toggleWebhook(${w.id})">Toggle</button>
                    <button onclick="deleteWebhook(${w.id})">Delete</button>
                    <button onclick="testWebhook(${w.id})">Test</button>
                </td>
            </tr>
        `;
  });
}

async function createWebhook() {
  let body = {
    url: document.getElementById("url").value,
    event: document.getElementById("event").value,
  };
  await fetch("/webhooks/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  loadWebhooks();
}

async function toggleWebhook(id) {
  await fetch(`/webhooks/${id}/toggle`, { method: "PUT" });
  loadWebhooks();
}

async function deleteWebhook(id) {
  await fetch(`/webhooks/${id}`, { method: "DELETE" });
  loadWebhooks();
}

async function testWebhook(id) {
  await fetch(`/webhooks/${id}/test`, { method: "POST" });
  alert("Test webhook sent!");
}

loadWebhooks();
