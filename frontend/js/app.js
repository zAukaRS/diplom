document.addEventListener("DOMContentLoaded", function () {

    loadResidents();

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

async function loadResidents() {
    try {
        const response = await fetch("/api/residents");
        const data = await response.json();

        const table = document.getElementById("residents-table");
        table.innerHTML = "";

        data.forEach(item => {
            const row = `
                <tr>
                    <td>${item.field}</td>
                    <td>${item.customer}</td>
                    <td>${item.full_name}</td>
                    <td>${formatDate(item.check_in)}</td>
                    <td>${formatDate(item.check_out)}</td>
                    <td>${item.days}</td>
                </tr>
            `;
            table.innerHTML += row;
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
