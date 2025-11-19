// CSV UPLOAD
document.getElementById("upload-form").onsubmit = async function (e) {
  e.preventDefault();

  let file = document.getElementById("file-input").files[0];
  if (!file) {
    alert("Please select a file");
    return;
  }

  let formData = new FormData();
  formData.append("file", file);

  let response = await fetch("/upload/", {
    method: "POST",
    body: formData,
  });

  let result = await response.json();
  let job_id = result.job_id;

  document.getElementById("status").innerText = "Upload started...";

  // POLL PROGRESS
  let interval = setInterval(async () => {
    let res = await fetch(`/progress/${job_id}`);
    let data = await res.json();

    if (data.status === "not_found") return;

    document.getElementById(
      "progress"
    ).innerText = `Progress: ${data.progress}% — ${data.status}`;

    if (data.progress >= 100 || data.progress == -1) {
      clearInterval(interval);
    }
  }, 1000);
};

// DELETE ALL PRODUCTS
document.getElementById("delete-all-btn").onclick = async function () {
  if (!confirm("Are you sure? This CANNOT be undone!")) return;

  let res = await fetch("/products/delete-all", { method: "DELETE" });
  let data = await res.json();

  let job_id = data.job_id;
  document.getElementById("delete-status").innerText = "Deleting products...";

  let interval = setInterval(async () => {
    let r = await fetch(`/progress/${job_id}`);
    let p = await r.json();

    if (p.status === "not_found") return;

    document.getElementById(
      "delete-status"
    ).innerText = `Delete Progress: ${p.progress}% — ${p.status}`;

    if (p.progress >= 100 || p.progress == -1) {
      clearInterval(interval);
    }
  }, 1000);
};
