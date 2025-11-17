const API_URL = "https://n7e3mxyw28.execute-api.ap-south-1.amazonaws.com/prod";
let token = "";

// --- LOGIN ---
async function handleLogin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
      token = data.token;
      document.getElementById("loginStatus").innerText = "✅ Login successful!";
      console.log("Token after login:", token);
      refreshFileList();
    } else {
      document.getElementById("loginStatus").innerText = `❌ ${data.error}`;
    }
  } catch (err) {
    document.getElementById("loginStatus").innerText = "❌ Login failed";
    console.error(err);
  }
}

// --- UPLOAD ---
async function handleUpload() {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) return alert("Select a file to upload");

  const file = fileInput.files[0];
  const reader = new FileReader();

  reader.onload = async function(e) {
    const base64Content = e.target.result.split(',')[1];

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ filename: file.name, fileContent: base64Content })
      });

      const data = await res.json();
      document.getElementById("uploadStatus").innerText = data.message || data.error;
      refreshFileList();
    } catch(err) {
      document.getElementById("uploadStatus").innerText = "❌ Upload failed";
      console.error(err);
    }
  };

  reader.readAsDataURL(file);
}

// --- LIST FILES ---
async function refreshFileList() {
  const listEl = document.getElementById("fileList");
  listEl.innerHTML = "Loading...";

  try {
    const res = await fetch(`${API_URL}/files`, {
      method: "GET",
      headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to fetch files");

    listEl.innerHTML = "";
    data.files.forEach(file => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span class="filename">${file.file_name}</span>
        <button class="btn download" onclick="downloadFile('${file.file_name}')">Download</button>
        <button class="btn delete" onclick="deleteFile('${file.file_id}')">Delete</button>
        <button class="btn share" onclick="handleShare('${file.file_id}', this)">Share</button>
        <div class="share-link"></div>
      `;
      listEl.appendChild(li);
    });
  } catch(err) {
    listEl.innerHTML = "❌ Failed to load files";
    console.error(err);
  }
}

// --- DELETE FILE ---
async function deleteFile(file_id) {
  try {
    const res = await fetch(`${API_URL}/delete`, {
      method: "DELETE",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ file_id })
    });
    const data = await res.json();
    alert(data.message || data.error);
    refreshFileList();
  } catch(err) {
    alert("❌ Delete failed");
    console.error(err);
  }
}

// --- DOWNLOAD FILE ---
async function downloadFile(filename) {
  try {
    const res = await fetch(`${API_URL}/download?filename=${encodeURIComponent(filename)}`, {
      method: "GET",
      headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Download failed");

    const blob = b64toBlob(data.fileContent);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch(err) {
    alert("❌ Download error: " + err.message);
    console.error(err);
  }
}

// Helper: convert base64 to Blob
function b64toBlob(base64) {
  const byteCharacters = atob(base64);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray]);
}

// --- SHARE FILE ---
async function handleShare(file_id, btn) {
  const shareLinkDiv = btn.closest("li").querySelector(".share-link");
  shareLinkDiv.innerText = "Sharing...";

  try {
    const res = await fetch(`${API_URL}/share`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ file_id })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Share failed");

    shareLinkDiv.innerHTML = `📎 <a href="${data.shareable_link}" target="_blank">${data.shareable_link}</a>`;
  } catch(err) {
    shareLinkDiv.innerText = "❌ Share failed";
    console.error(err);
  }
}
