document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }
    await loadFields();
    document.getElementById("requestForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const field_id = document.getElementById("fieldId").value;
        const check_in = document.getElementById("checkIn").value;
        const check_out = document.getElementById("checkOut").value;
        const comment = document.getElementById("comment").value;
        const messageDiv = document.getElementById("message");
        messageDiv.textContent = "";
        if (!field_id || !check_in || !check_out) {
            messageDiv.textContent = "Заполните все поля";
            return;
        }
        try {
            const res = await apiFetch("/api/requests/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ field_id, check_in, check_out, comment })
            });
            const data = await res.json();
            if (res.ok) {
                messageDiv.style.color = "green";
                messageDiv.textContent = "Заявка отправлена!";
                document.getElementById("requestForm").reset();
            } else {
                messageDiv.style.color = "red";
                messageDiv.textContent = data.detail || "Ошибка";
            }
        } catch (err) {
            messageDiv.textContent = "Ошибка сервера";
        }
    });
});
async function loadFields() {
    const res = await apiFetch("/api/fields");
    const fields = await res.json();
    const select = document.getElementById("fieldId");
    fields.forEach(f => {
        const opt = document.createElement("option");
        opt.value = f.id;
        opt.textContent = f.name;
        select.appendChild(opt);
    });
}