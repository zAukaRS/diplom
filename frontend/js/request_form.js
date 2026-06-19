document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }

    // Проверка, редактируем ли мы существующий черновик
    const urlParams = new URLSearchParams(window.location.search);
    const editId = urlParams.get("id");
    const isEditMode = !!editId;

    // Загрузка списка месторождений
    const fieldsRes = await apiFetch("/api/fields");
    const fields = await fieldsRes.json();
    const fieldSelect = document.getElementById("fieldId");
    fields.forEach(f => {
        const opt = document.createElement("option");
        opt.value = f.id;
        opt.textContent = f.name;
        fieldSelect.appendChild(opt);
    });

    // Элементы
    const checkIn = document.getElementById("checkIn");
    const checkOut = document.getElementById("checkOut");
    const availableDiv = document.getElementById("availableRooms");
    const roomIdInput = document.getElementById("roomId");

    // Функция загрузки свободных комнат (только для нового создания, не для редактирования)
    async function loadAvailableRooms() {
        const field_id = fieldSelect.value;
        const check_in = checkIn.value;
        const check_out = checkOut.value;
        if (!field_id || !check_in || !check_out) return;

        const url = `/api/requests/available?field_id=${field_id}&check_in=${check_in}&check_out=${check_out}`;
        const res = await apiFetch(url);
        if (!res.ok) return;
        const rooms = await res.json();
        
        availableDiv.innerHTML = "";
        if (rooms.length === 0) {
            availableDiv.innerHTML = "<p>Нет свободных комнат на выбранные даты</p>";
            roomIdInput.value = "";
            return;
        }
        rooms.forEach(room => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "room-item";
            btn.textContent = `${room.room_number} (мест: ${room.capacity})`;
            btn.dataset.id = room.id;
            btn.addEventListener("click", () => {
                document.querySelectorAll(".room-item").forEach(b => b.classList.remove("selected"));
                btn.classList.add("selected");
                roomIdInput.value = room.id;
            });
            availableDiv.appendChild(btn);
        });
    }

    // Если это редактирование, загружаем данные черновика
    if (isEditMode) {
        const reqRes = await apiFetch(`/api/requests/${editId}`);
        const reqData = await reqRes.json();
        // Заполняем форму
        fieldSelect.value = reqData.field_id;
        checkIn.value = reqData.check_in;
        checkOut.value = reqData.check_out;
        document.getElementById("customer").value = reqData.customer;
        document.getElementById("contractDate").value = reqData.contract_date;
        document.getElementById("eolFio").value = reqData.eol_fio;
        document.getElementById("position").value = reqData.position;
        document.getElementById("comment").value = reqData.comment;
        roomIdInput.value = reqData.room_id;
        // Загружаем комнаты, чтобы подсветить выбранную
        await loadAvailableRooms();
        // Выделяем кнопку с выбранной комнатой
        setTimeout(() => {
            const selectedBtn = Array.from(document.querySelectorAll('.room-item')).find(btn => btn.dataset.id == reqData.room_id);
            if (selectedBtn) selectedBtn.classList.add('selected');
        }, 200);
    } else {
        // Для новой заявки – загружаем комнаты при изменении полей
        fieldSelect.addEventListener("change", loadAvailableRooms);
        checkIn.addEventListener("change", loadAvailableRooms);
        checkOut.addEventListener("change", loadAvailableRooms);
    }

    // Отправка формы
    document.getElementById("requestForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const messageDiv = document.getElementById("message");
        messageDiv.textContent = "";

        const data = {
            customer: document.getElementById("customer").value.trim(),
            contract_date: document.getElementById("contractDate").value,
            eol_fio: document.getElementById("eolFio").value.trim(),
            position: document.getElementById("position").value.trim(),
            field_id: parseInt(fieldSelect.value),
            check_in: checkIn.value,
            check_out: checkOut.value,
            room_id: parseInt(roomIdInput.value),
            comment: document.getElementById("comment").value.trim()
        };

        // Валидация
        if (!data.customer || !data.contract_date || !data.eol_fio || !data.field_id || !data.check_in || !data.check_out || !data.room_id) {
            messageDiv.style.color = "red";
            messageDiv.textContent = "Заполните все обязательные поля";
            return;
        }

        try {
            let res;
            if (isEditMode) {
                // Обновление через PATCH
                res = await apiFetch(`/api/requests/${editId}`, {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
            } else {
                // Создание новой заявки
                res = await apiFetch("/api/requests/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
            }
            const result = await res.json();
            if (res.ok) {
                messageDiv.style.color = "green";
                messageDiv.textContent = isEditMode ? "Заявка обновлена!" : "Заявка успешно создана!";
                setTimeout(() => {
                    window.location.href = "/my_requests";
                }, 1500);
            } else {
                messageDiv.style.color = "red";
                messageDiv.textContent = result.detail || "Ошибка при сохранении заявки";
            }
        } catch (err) {
            messageDiv.style.color = "red";
            messageDiv.textContent = "Ошибка сервера";
        }
    });
});