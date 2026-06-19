document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }

    let currentType = "drafts";
    const tbody = document.querySelector("#requestsTable tbody");
    const tabs = document.querySelectorAll(".tab");

    // Загрузка месторождений для отображения названий
    const fieldsRes = await apiFetch("/api/fields");
    const fields = await fieldsRes.json();
    const fieldMap = {};
    fields.forEach(f => fieldMap[f.id] = f.name);

    async function loadRequests() {
        const res = await apiFetch(`/api/requests/my?req_type=${currentType}`);
        const requests = await res.json();
        tbody.innerHTML = "";
        for (const r of requests) {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${fieldMap[r.field_id] || r.field_id}</td>
                <td>${r.check_in} — ${r.check_out}</td>
                <td>${r.comment || ""}</td>
                <td>${r.status}</td>
                <td>${r.admin_comment || ""}</td>
            `;
            if (r.status === "pending") {
                const actionsCell = document.createElement("td");
                const editBtn = document.createElement("button");
                editBtn.textContent = "Редактировать";
                editBtn.onclick = () => window.location.href = `/request_form?id=${r.id}`;
                const deleteBtn = document.createElement("button");
                deleteBtn.textContent = "Удалить";
                deleteBtn.onclick = async () => {
                    if (confirm("Удалить черновик?")) {
                        const resDel = await apiFetch(`/api/requests/${r.id}`, { method: "DELETE" });
                        if (resDel.ok) loadRequests();
                        else alert("Ошибка удаления");
                    }
                };
                actionsCell.appendChild(editBtn);
                actionsCell.appendChild(deleteBtn);
                tr.appendChild(actionsCell);
            } else {
                tr.appendChild(document.createElement("td")); // пустая ячейка
            }
            tbody.appendChild(tr);
        }
    }

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            currentType = tab.dataset.type;
            loadRequests();
        });
    });

    loadRequests();
});