document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }
    const res = await apiFetch("/api/requests/my");
    const requests = await res.json();
    const tbody = document.querySelector("#requestsTable tbody");
    const fields = await (await apiFetch("/api/fields")).json();
    const fieldMap = {};
    fields.forEach(f => fieldMap[f.id] = f.name);
    requests.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${fieldMap[r.field_id] || r.field_id}</td>
            <td>${r.check_in} — ${r.check_out}</td>
            <td>${r.comment || ""}</td>
            <td>${r.status}</td>
            <td>${r.admin_comment || ""}</td>
        `;
        tbody.appendChild(tr);
    });
});