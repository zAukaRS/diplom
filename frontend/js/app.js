
document.addEventListener("DOMContentLoaded", function () {
    loadFields();

    // Показать / скрыть форму
    document.getElementById("addResidentBtn").addEventListener("click", function () {
        const form = document.getElementById("addResidentForm");
        form.style.display = form.style.display === "none" ? "block" : "none";
    });

    // Сохранение записи
    document.getElementById("saveResidentBtn").addEventListener("click", async function () {
        const checkIn = document.getElementById("checkInInput").value;
        const checkOut = document.getElementById("checkOutInput").value;

        const data = {
            field: document.getElementById("fieldInput").value,
            customer: document.getElementById("customerInput").value,
            full_name: document.getElementById("fullNameInput").value,
            check_in: checkIn,
            check_out: checkOut,
            days: calculateDays(checkIn, checkOut)
        };

        if (!data.field || !data.customer || !data.full_name) {
            alert("Заполните обязательные поля!");
            return;
        }

        try {
            const response = await fetch("/api/add_resident", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const text = await response.text();
            console.log("Ответ сервера:", text);

            if (response.ok) {
                alert("Запись добавлена!");
                loadResidents();
            } else {
                alert("Ошибка сервера: " + text);
            }
        } catch (error) {
            alert("Ошибка: " + error.message);
        }
    });

    
    
});
function downloadReport() {
    const dateFrom = document.getElementById("dateFrom").value;
    const dateTo = document.getElementById("dateTo").value;

    if (!dateFrom || !dateTo) {
        alert("Выберите обе даты!");
        return;
    }

    window.open(`/api/get_report?date_from=${dateFrom}&date_to=${dateTo}`, "_blank");
    }
let dragStart = null; // {residentId, day, value}
let dragMode = null;

let workplaces = [];

async function loadWorkplaces() {
    const res = await fetch("/api/workplaces");
    workplaces = await res.json();
}

async function loadResidents() {
    try {
        const response = await fetch("/api/residents");
        const data = await response.json();
        console.log(data);

        const tbody = document.getElementById("calendarBody");
        tbody.innerHTML = ""; // очищаем тело таблицы

        data.forEach(item => {
            const row = `
                <tr>
                    <td>${item.room_location}</td>
                    <td>${item.room_path}</td>
                    <td>${item.room_number}</td>
                    <td>${item.room_capacity || ""}</td>
                    <td>${item.gender || ""}</td>
                    <td>${item.full_name}</td>
                    <td>${item.position || ""}</td>
                    <td>${item.shift || ""}</td>
                    <td>${item.workplace || ""}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });

    } catch (error) {
        console.error("Ошибка загрузки данных:", error);
    }
}

function formatDate(dateString) {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date.toLocaleDateString("ru-RU");
}

function calculateDays(checkIn, checkOut) {
    if (!checkIn || !checkOut) return 0;

    const start = new Date(checkIn);
    const end = new Date(checkOut);

    const diffTime = end - start;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    return diffDays > 0 ? diffDays : 0;
}


async function loadFields() {
    try {
        const response = await fetch("/api/fields");
        const data = await response.json();

        const select = document.getElementById("fieldFilter");
        // очищаем список перед добавлением
        select.innerHTML = '<option value="">Выберите месторождение</option>';

        data.forEach(field => {
            const option = document.createElement("option");
            option.value = field.id;
            option.textContent = field.name;
            select.appendChild(option);
        });
    } catch (err) {
        console.error("Ошибка загрузки месторождений:", err);
    }
}

function generateCalendar(days){
    const head = document.getElementById("calendarHead");
    let row = "<tr>";
    row += "<th>Расположение</th>";
    row += "<th>Путь</th>";
    row += "<th>№ комнаты</th>";
    row += "<th>К-во мест</th>";
    row += "<th>Пол</th>";
    row += "<th>ФИО</th>";
    row += "<th>Должность</th>";
    row += "<th>Смена</th>";

    // Если нужно, можно добавить дни календаря (1,2,3...)
    for (let i = 1; i <= days; i++) {
        row += `<th>${i}</th>`;
    }

    row += "<th>Места работы</th>";
    row += "</tr>";
    head.innerHTML = row;
}

function daysInMonth(month,year){

    return new Date(year, month, 0).getDate()

}

async function loadCalendar() {
    await loadWorkplaces();
    const field = document.getElementById("fieldFilter").value;
    const year = document.getElementById("yearFilter").value;
    const month = document.getElementById("monthFilter").value;


    const days = daysInMonth(month, year);

    // Формируем заголовок
    generateCalendar(days);

    // Загружаем данные только в tbody
    const response = await fetch(`/api/residents?field=${field}&year=${year}&month=${month}`);
    const residents = await response.json();

    const tbody = document.getElementById("calendarBody");
    tbody.innerHTML = ""; // очищаем только тело

    residents.forEach(r => {
    let row = `<tr>
        <td>${r.room_location || ""}</td>
        <td>${r.room_path || ""}</td>
        <td>${r.room_number || ""}</td>
        <td>${r.room_capacity || ""}</td>
        <td>${r.gender || ""}</td>
        <td>${r.full_name}</td>
        <td>${r.position || ""}</td>
        <td>${r.shift || ""}</td>`;


    for (let i = 1; i <= days; i++) {
        const selectedId = r.days_info?.[i] || "";

        row += `<td>
            <select class="day-select" data-resident="${r.id}" data-day="${i}" title="Выберите рабочее место">
                <option value="">-</option>
                ${workplaces.map(w => `
                    <option value="${w.id}" ${w.id == selectedId ? "selected" : ""}>
                        ${w.name}
                    </option>
                `).join("")}
            </select>
        </td>`;
    }


    row += `</tr>`;

    tbody.innerHTML += row;
    initDragFill();
});
}

const addResidentBtn = document.getElementById("addResidentBtn");
const addResidentForm = document.getElementById("addResidentForm");

addResidentBtn.addEventListener("click", () => {
    if (addResidentForm.style.display === "none") {
        addResidentForm.style.display = "block";
    } else {
        addResidentForm.style.display = "none";
    }
});

const saveResidentBtn = document.getElementById("saveResidentBtn");

saveResidentBtn.addEventListener("click", async () => {
    const data = {
        field: document.getElementById("fieldInput").value,
        customer: document.getElementById("customerInput").value,
        full_name: document.getElementById("fullNameInput").value,
        check_in: document.getElementById("checkInInput").value,
        check_out: document.getElementById("checkOutInput").value,
        days: calculateDays(
            document.getElementById("checkInInput").value,
            document.getElementById("checkOutInput").value
        )
    };

    if (!data.field || !data.customer || !data.full_name || !data.check_in || !data.check_out) {
        alert("Заполните все поля!");
        return;
    }

    // отправка на сервер
    try {
        const response = await fetch("/api/add_resident", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            addResidentForm.style.display = "none";
            loadResidents(); // обновляем таблицу после добавления
        } else {
            alert(result.error || "Ошибка добавления");
        }
    } catch (err) {
        alert("Ошибка: " + err.message);
    }
});




document.addEventListener("change", async (e) => {
    if (e.target.classList.contains("day-select")) {
        const residentId = e.target.dataset.resident;
        if (!residentId) return alert("Не удалось определить жильца");
        const day = e.target.dataset.day;
        const month = document.getElementById("monthFilter").value;
        const year = document.getElementById("yearFilter").value;

        let workplaceId = e.target.value;
        if (!workplaceId) {
            workplaceId = null;  // <- сюда пустое значение
        } else {
            workplaceId = parseInt(workplaceId);
        }

        console.log({residentId, day, month, year, workplaceId}); // <- проверь что отправляется

        try {
            const response = await fetch("/api/update_day", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    resident_id: residentId,
                    day: day,
                    month: month,
                    year: year,
                    workplace_id: workplaceId
                })
            });

            const result = await response.json();
            console.log("Сохранено:", result);

        } catch (err) {
            alert("Ошибка: " + err.message);
        }
    }
});



// Функция сохранения одного дня
async function saveDay(selectEl) {
    const residentId = selectEl.dataset.resident;
    const day = selectEl.dataset.day;
    const month = document.getElementById("monthFilter").value;
    const year = document.getElementById("yearFilter").value;
    const workplaceId = selectEl.value || null;

    try {
        await fetch("/api/update_day", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resident_id: residentId, day, month, year, workplace_id: workplaceId })
        });
    } catch (err) {
        console.error("Ошибка при сохранении дня:", err);
    }
}

function initDragFill() {
    const tbody = document.getElementById("calendarBody");

    tbody.addEventListener("mousedown", (e) => {
        const td = e.target.closest("td");
        if (!td) return;
        if (e.target.tagName === "SELECT") return; // клики по select пропускаем

        const sel = td.querySelector(".day-select");
        if (!sel) return;

        dragStart = {
            residentId: sel.dataset.resident,
            day: parseInt(sel.dataset.day),
            value: sel.value
        };

        // Если значение есть — будем заполнять этим значением, иначе очищать
        dragMode = dragStart.value ? "fill" : "clear";

        // Подсветка начального дня
        sel.classList.add("drag-highlight");

        e.preventDefault();
    });

    tbody.addEventListener("mouseover", (e) => {
        if (!dragStart) return;

        const td = e.target.closest("td");
        if (!td) return;

        const sel = td.querySelector(".day-select");
        if (!sel) return;
        if (sel.dataset.resident !== dragStart.residentId) return;

        const currentDay = parseInt(sel.dataset.day);
        const start = Math.min(dragStart.day, currentDay);
        const end = Math.max(dragStart.day, currentDay);

        // Сбрасываем подсветку всех дней этого жильца
        tbody.querySelectorAll(`.day-select[data-resident='${dragStart.residentId}']`).forEach(s => s.classList.remove("drag-highlight"));

        // Подсвечиваем диапазон
        for (let i = start; i <= end; i++) {
            const cell = tbody.querySelector(`.day-select[data-resident='${dragStart.residentId}'][data-day='${i}']`);
            if (cell) cell.classList.add("drag-highlight");
        }
    });

    document.addEventListener("mouseup", async () => {
        if (!dragStart) return;

        const selList = tbody.querySelectorAll(`.day-select[data-resident='${dragStart.residentId}'].drag-highlight`);

        for (const sel of selList) {
            sel.value = dragMode === "fill" ? dragStart.value : "";
            await saveDay(sel);
        }

        selList.forEach(s => s.classList.remove("drag-highlight"));

        dragStart = null;
        dragMode = null;
    });
}

/*document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("excelFile");
    if (!fileInput.files.length) {
        alert("Выберите файл Excel");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("/api/upload_excel", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            loadResidents();
        } else {
            alert(result.error || "Ошибка загрузки");
        }
    } catch (err) {
        alert("Ошибка: " + err.message);
    }
});*/