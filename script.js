const pluginButtons = document.querySelectorAll(".plugin-pill");
const pluginDetail = document.querySelector("#plugin-detail");

pluginButtons.forEach((button) => {
  button.addEventListener("click", () => {
    pluginButtons.forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    pluginDetail.textContent = button.dataset.detail;
  });
});
