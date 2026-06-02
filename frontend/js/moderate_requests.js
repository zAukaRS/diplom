let fieldId = null;
document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }
    // Получаем текущего пользователя, чтобы узнать field_id
    const userRes = await apiFetch("/api/current_user");
    const currentUser = await userRes.json();
    fieldId = currentUser.field_id; // для админа поля это есть, для глобального админа нужно выбрать поле (упростим: покажем все или выбор)
    if (!fieldId) {
        // глобальный админ – предложим выбрать поле из списка
        // добавим выбор
        const container = document.querySelector(".main-content");
        const selectDiv = document.createElement("div");
        selectDiv.innerHTML = `Выберите месторождение: <select id="fieldSelect"></select> <button id="loadBtn">Загрузить</button>`;
        container.prepend(selectDiv);
        const fieldsRes = await apiFetch("/api/fields");
        const fields = await fieldsRes.json();
        const select = document.getElementById("fieldSelect");
        fields.forEach(f => {
            const opt = document.createElement("option");
            opt.value = f.id;
            opt.textContent = f.name;
            select.appendChild(opt);
        });
        document.getElementById("loadBtn").addEventListener("click", () => {
            fieldId = select.value;
            loadRequests();
        });
    } else {
        document.getElementById("fieldName").textContent = currentUser.field_name || "ваше";
        loadRequests();
    }
});
async function loadRequests() {
    if (!fieldId) return;
    const res = await apiFetch(`/api/requests/field/${fieldId}`);
    const requests = await res.json();
    const tbody = document.querySelector("#requestsTable tbody");
    tbody.innerHTML = "";
    for (const r of requests) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${r.username}</td>
            <td>${r.check_in} — ${r.check_out}</td>
            <td>${r.comment || ""}</td>
            <td>${r.status}</td>
            <td>
                <select class="status-select" data-id="${r.id}">
                    <option value="pending" ${r.status === "pending" ? "selected" : ""}>На рассмотрении</option>
                    <option value="approved" ${r.status === "approved" ? "selected" : ""}>Одобрено</option>
                    <option value="rejected" ${r.status === "rejected" ? "selected" : ""}>Отклонено</option>
                </select>
                <input type="text" class="admin-comment" placeholder="Комментарий" value="${r.admin_comment || ""}">
                <button class="save-btn" data-id="${r.id}">Сохранить</button>
            </td>
        `;
        tbody.appendChild(tr);
    }
    // обработчики
    document.querySelectorAll(".save-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const id = btn.dataset.id;
            const row = btn.closest("tr");
            const status = row.querySelector(".status-select").value;
            const adminComment = row.querySelector(".admin-comment").value;
            await apiFetch(`/api/requests/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status, admin_comment: adminComment })
            });
            loadRequests(); // перезагрузить
        });
    });
}