document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const messageEl = document.getElementById("message");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        messageEl.textContent = "";
        messageEl.className = "error";

        const username = form.username.value.trim();
        const password = form.password.value;
        const confirm = form.confirm_password.value;

        if (!username || !password) {
            messageEl.textContent = "Заполните все поля";
            return;
        }
        if (password !== confirm) {
            messageEl.textContent = "Пароли не совпадают";
            return;
        }
        if (password.length < 4) {
            messageEl.textContent = "Пароль должен быть не менее 4 символов";
            return;
        }

        try {
            const res = await fetch("/api/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();

            if (!res.ok) {
                messageEl.textContent = data.detail || "Ошибка регистрации";
                return;
            }

            // Успех
            messageEl.className = "success";
            messageEl.textContent = data.message || "Регистрация успешна! Сейчас перенаправим на вход...";
            setTimeout(() => {
                window.location.href = "/login";
            }, 2000);

        } catch (err) {
            console.error(err);
            messageEl.textContent = "Ошибка соединения с сервером";
        }
    });
});