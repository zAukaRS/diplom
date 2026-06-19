document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }

    const tbody = document.querySelector("#requestsTable tbody");

    // Загрузка списка полей
    const fieldsRes = await apiFetch("/api/fields");
    const fields = await fieldsRes.json();
    const fieldMap = {};
    fields.forEach(f => fieldMap[f.id] = f.name);

    async function loadPendingRequests() {
        const res = await apiFetch("/api/requests/pending");
        const requests = await res.json();
        tbody.innerHTML = "";
        for (const req of requests) {
            const tr = document.createElement("tr");
            tr.dataset.id = req.id;
            tr.innerHTML = `
                <td>${req.id}</td>
                <td>${req.user_id}</td>
                <td>${fieldMap[req.field_id] || req.field_id}</td>
                <td>${req.check_in} — ${req.check_out}</td>
                <td>${req.room_id || ""}</td>
                <td class="editable" data-field="customer">${req.customer || ""}</td>
                <td class="editable" data-field="contract_num">${req.contract_num || ""}</td>
                <td class="editable" data-field="contract_date">${req.contract_date || ""}</td>
                <td class="editable" data-field="eol_fio">${req.eol_fio || ""}</td>
                <td class="editable" data-field="position">${req.position || ""}</td>
                <td class="editable" data-field="comment">${req.comment || ""}</td>
                <td class="actions">
                    <button class="edit-btn">Редактировать</button>
                    <button class="approve-btn">Одобрить</button>
                    <button class="reject-btn">Отклонить</button>
                </td>
            `;
            tbody.appendChild(tr);
        }
        attachEventHandlers();
    }

    function attachEventHandlers() {
        // Редактирование
        document.querySelectorAll(".edit-btn").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const row = btn.closest("tr");
                const id = row.dataset.id;
                const editables = row.querySelectorAll(".editable");
                // Если уже в режиме редактирования – сохраняем
                if (btn.textContent === "Сохранить") {
                    const updateData = {};
                    editables.forEach(cell => {
                        const input = cell.querySelector("input");
                        if (input) {
                            updateData[cell.dataset.field] = input.value;
                        }
                    });
                    try {
                        const res = await apiFetch(`/api/requests/${id}`, {
                            method: "PATCH",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(updateData)
                        });
                        if (res.ok) {
                            loadPendingRequests();
                        } else {
                            alert("Ошибка сохранения");
                        }
                    } catch (err) {
                        alert("Ошибка сервера");
                    }
                } else {
                    // Вход в режим редактирования
                    editables.forEach(cell => {
                        const value = cell.textContent.trim();
                        const input = document.createElement("input");
                        input.value = value;
                        input.style.width = "100%";
                        cell.innerHTML = "";
                        cell.appendChild(input);
                    });
                    btn.textContent = "Сохранить";
                }
            });
        });

        // Одобрение
        document.querySelectorAll(".approve-btn").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const row = btn.closest("tr");
                const id = row.dataset.id;
                if (confirm("Одобрить эту заявку?")) {
                    const res = await apiFetch(`/api/requests/${id}/approve`, { method: "POST" });
                    if (res.ok) {
                        loadPendingRequests();
                    } else {
                        alert("Ошибка одобрения");
                    }
                }
            });
        });

        // Отклонение
        document.querySelectorAll(".reject-btn").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const row = btn.closest("tr");
                const id = row.dataset.id;
                const comment = prompt("Введите комментарий к отклонению (необязательно):");
                if (comment !== null) {
                    const res = await apiFetch(`/api/requests/${id}/reject?admin_comment=${encodeURIComponent(comment)}`, { method: "POST" });
                    if (res.ok) {
                        loadPendingRequests();
                    } else {
                        alert("Ошибка отклонения");
                    }
                }
            });
        });
    }

    loadPendingRequests();
});