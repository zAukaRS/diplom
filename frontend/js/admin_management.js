document.addEventListener("DOMContentLoaded", () => {

    // Загрузка админов при старте
    loadAdmins();

    // Создание нового администратора
    document.getElementById("createAdminBtn").addEventListener("click", async () => {
        const username = document.getElementById("newAdminUsername").value.trim();
        const password = document.getElementById("newAdminPassword").value.trim();
        const messageEl = document.getElementById("adminMessage");

        messageEl.textContent = "";
        messageEl.style.color = "red";

        if (!username || !password) {
            messageEl.textContent = "Заполните все поля!";
            return;
        }

        try {
            const res = await fetch("/api/create_admin", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();

            if (res.ok) {
                messageEl.style.color = "green";
                messageEl.textContent = "Админ создан!";
                document.getElementById("newAdminUsername").value = "";
                document.getElementById("newAdminPassword").value = "";
                loadAdmins();
            } else {
                messageEl.textContent = data.error || "Ошибка создания";
            }

        } catch (err) {
            messageEl.textContent = "Ошибка сервера";
            console.error(err);
        }
    });
});

async function loadAdmins() {
    try {
        const res = await fetch("/api/get_admins");
        const admins = await res.json();

        const tbody = document.getElementById("adminTableBody");
        tbody.innerHTML = "";

        admins.forEach(admin => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>
                    <input value="${admin.username}" disabled class="edit-input username">
                </td>
                <td>
                    <input type="password" placeholder="******" disabled class="edit-input password">
                </td>
                <td>
                    ${admin.field || ""}
                </td>
                <td>
                    <button class="edit-btn" onclick="toggleEdit(this, ${admin.id})">Изменить</button>
                    <button class="delete-btn" onclick="deleteAdmin(${admin.id})">Удалить</button>
                </td>
            `;

            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error("Ошибка загрузки админов:", err);
    }
}


async function deleteAdmin(id) {
    if (!confirm("Удалить этого администратора?")) return;

    try {
        const res = await fetch(`/api/delete_admin/${id}`, {
            method: "DELETE"
        });

        if (res.ok) {
            loadAdmins();
        } else {
            alert("Ошибка при удалении!");
        }

    } catch (err) {
        alert("Ошибка сервера!");
    }
}

function toggleEdit(button, id) {
    const row = button.closest("tr");
    const inputs = row.querySelectorAll("input");

    const isEditMode = button.textContent === "Изменить";

    inputs.forEach(input => {
        input.disabled = !isEditMode;
        input.style.background = isEditMode ? "#fff" : "#f5f5f5";
    });

    button.textContent = isEditMode ? "Сохранить" : "Изменить";

    if (!isEditMode) {
        saveAdmin(row, id);
    }
}

async function saveAdmin(row, id) {
    const username = row.querySelector(".username").value.trim();
    const password = row.querySelector(".password").value.trim();

    try {
        const res = await fetch(`/api/update_admin_inline/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Ошибка обновления");
        }

    } catch (err) {
        alert("Ошибка сервера!");
    }
}