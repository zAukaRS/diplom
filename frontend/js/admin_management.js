document.addEventListener("DOMContentLoaded", () => {
    loadAdmins();
    loadFieldsForSelect("newAdminField");

    const fieldSelect = document.getElementById("newAdminField");
    const newFieldBlock = document.getElementById("newFieldBlock");
    if (fieldSelect) {
        // Добавляем опцию "Новое"
        const newOption = document.createElement("option");
        newOption.value = "new";
        newOption.textContent = "+ Новое месторождение...";
        fieldSelect.appendChild(newOption);

        fieldSelect.addEventListener("change", () => {
            newFieldBlock.style.display = fieldSelect.value === "new" ? "block" : "none";
        });
    }

    document.getElementById("createAdminBtn").addEventListener("click", async () => {
        const username = document.getElementById("newAdminUsername").value.trim();
        const password = document.getElementById("newAdminPassword").value.trim();
        let field_id = null;
        const selectedVal = fieldSelect.value;
        const messageEl = document.getElementById("adminMessage");

        messageEl.textContent = "";
        if (!username || !password) {
            messageEl.textContent = "Заполните логин и пароль!";
            return;
        }

        try {
            if (selectedVal === "new") {
                const newFieldName = document.getElementById("newFieldName").value.trim();
                if (!newFieldName) {
                    messageEl.textContent = "Введите название нового месторождения";
                    return;
                }
                const res = await apiFetch("/api/fields/create", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: newFieldName })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || "Ошибка создания поля");
                field_id = data.id;
            } else if (selectedVal && selectedVal !== "") {
                field_id = parseInt(selectedVal);
            }

            const res = await apiFetch("/api/create_admin", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password, field_id })
            });
            const data = await res.json();
            if (res.ok) {
                messageEl.style.color = "green";
                messageEl.textContent = "Админ создан!";
                document.getElementById("newAdminUsername").value = "";
                document.getElementById("newAdminPassword").value = "";
                document.getElementById("newFieldName").value = "";
                fieldSelect.value = "";
                newFieldBlock.style.display = "none";
                loadAdmins();
            } else {
                messageEl.textContent = data.error || "Ошибка создания";
            }
        } catch (err) {
            messageEl.textContent = err.message || "Ошибка сервера";
        }
    });
});

async function loadFieldsForSelect(selectId) {
    try {
        const res = await apiFetch("/api/fields");
        const fields = await res.json();
        const select = document.getElementById(selectId);
        if (!select) return;
        // Сохраняем текущее выбранное значение (если есть)
        const oldValue = select.value;
        select.innerHTML = '<option value="">-- Без месторождения --</option>';
        fields.forEach(f => {
            const opt = document.createElement("option");
            opt.value = f.id;
            opt.textContent = f.name;
            select.appendChild(opt);
        });
        // Восстанавливаем опцию "Новое"
        const newOpt = document.createElement("option");
        newOpt.value = "new";
        newOpt.textContent = "+ Новое месторождение...";
        select.appendChild(newOpt);
        if (oldValue && oldValue !== "new") select.value = oldValue;
    } catch (err) {
        console.error("Ошибка загрузки полей:", err);
    }
}

async function loadAdmins() {
    try {
        const res = await apiFetch("/api/get_admins");
        const admins = await res.json();
        const tbody = document.getElementById("adminTableBody");
        tbody.innerHTML = "";
        for (const admin of admins) {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><input value="${admin.username}" disabled class="edit-input username"></td>
                <td><input type="password" placeholder="******" disabled class="edit-input password"></td>
                <td class="field-cell">${admin.field || ""}</td>
                <td>
                    <button class="edit-btn" onclick="toggleEdit(this, ${admin.id})">Изменить</button>
                    <button class="delete-btn" onclick="deleteAdmin(${admin.id})">Удалить</button>
                </td>
            `;
            tbody.appendChild(tr);
        }
    } catch (err) {
        console.error("Ошибка загрузки админов:", err);
    }
}

async function deleteAdmin(id) {
    if (!confirm("Удалить этого администратора?")) return;
    try {
        const res = await apiFetch(`/api/delete_admin/${id}`, { method: "DELETE" });
        if (res.ok) loadAdmins();
        else alert("Ошибка при удалении!");
    } catch (err) {
        alert("Ошибка сервера!");
    }
}

async function toggleEdit(button, id) {
    const row = button.closest("tr");
    const inputs = row.querySelectorAll("input");
    const isEditMode = button.textContent === "Изменить";
    const fieldCell = row.querySelector(".field-cell");

    if (isEditMode) {
        // Вход в режим редактирования
        inputs.forEach(input => {
            input.disabled = false;
            input.style.background = "#fff";
        });
        // Превращаем поле месторождения в select
        const currentFieldName = fieldCell.textContent.trim();
        const select = document.createElement("select");
        select.className = "edit-select field-select";
        // Загружаем список полей
        try {
            const res = await apiFetch("/api/fields");
            const fields = await res.json();
            select.innerHTML = '<option value="">-- Без месторождения --</option>';
            fields.forEach(f => {
                const opt = document.createElement("option");
                opt.value = f.id;
                opt.textContent = f.name;
                if (currentFieldName === f.name) opt.selected = true;
                select.appendChild(opt);
            });
            // Добавляем опцию "Новое месторождение"
            const newOpt = document.createElement("option");
            newOpt.value = "new";
            newOpt.textContent = "+ Новое...";
            select.appendChild(newOpt);
            select.addEventListener("change", async () => {
                if (select.value === "new") {
                    const newName = prompt("Введите название нового месторождения:");
                    if (newName) {
                        const createRes = await apiFetch("/api/fields/create", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ name: newName })
                        });
                        const newField = await createRes.json();
                        if (createRes.ok) {
                            // Добавляем новое поле в select
                            const opt = document.createElement("option");
                            opt.value = newField.id;
                            opt.textContent = newField.name;
                            select.insertBefore(opt, select.lastChild);
                            select.value = newField.id;
                        } else {
                            alert("Ошибка создания поля");
                        }
                    }
                }
            });
        } catch (err) {
            console.error(err);
        }
        fieldCell.innerHTML = "";
        fieldCell.appendChild(select);
        button.textContent = "Сохранить";
    } else {
        // Сохранение
        const username = row.querySelector(".username").value.trim();
        const password = row.querySelector(".password").value.trim();
        let field_id = null;
        const fieldSelect = row.querySelector(".field-select");
        if (fieldSelect) {
            let val = fieldSelect.value;
            if (val && val !== "") field_id = parseInt(val);
        }
        try {
            const res = await apiFetch(`/api/update_admin_inline/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password, field_id })
            });
            if (!res.ok) {
                const data = await res.json();
                alert(data.error || "Ошибка обновления");
            }
        } catch (err) {
            alert("Ошибка сервера!");
        }
        // Перезагружаем список админов (проще, чем обновлять строку вручную)
        loadAdmins();
    }
}