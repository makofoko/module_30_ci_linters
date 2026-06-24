document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");
  const logoutBtn = document.getElementById("logoutBtn");

  // Регистрация
  if (registerForm) {
    registerForm.addEventListener("submit", e => {
      e.preventDefault();
      const childName = document.getElementById("childName").value;
      const phone = document.getElementById("phone").value;
      const password = document.getElementById("password").value;

      // Сохраняем аккаунт в localStorage
      localStorage.setItem("account", JSON.stringify({ childName, phone, password }));
      alert("Регистрация успешна!");
      window.location.href = "login.html";
    });
  }

  // Вход
  if (loginForm) {
    loginForm.addEventListener("submit", e => {
      e.preventDefault();
      const phone = document.getElementById("loginPhone").value;
      const password = document.getElementById("loginPassword").value;

      const account = JSON.parse(localStorage.getItem("account"));
      if (account && account.phone === phone && account.password === password) {
        alert("Добро пожаловать, " + account.childName + "!");
        localStorage.setItem("user", account.childName);
        window.location.href = "profile.html";
      } else {
        alert("Неверный номер или пароль!");
      }
    });
  }

  // Выход
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("user");
      alert("Вы вышли из аккаунта.");
      window.location.href = "login.html";
    });
  }
});
