//  DASHBOARD MENU SHOW ON TABLETE AND MODILE

const dashBtn = document.querySelector(".dash__box");
const dashMenu = document.querySelector(".side__navbar");
const dashContent = document.querySelector(".dashboard__content");

if (dashBtn) {
  dashBtn.addEventListener("click", (e) => {
    dashMenu.classList.toggle("active");
    dashBtn.classList.toggle("active");
    // dashContent.classList.toggle("active");
  });
}

// profile image show using modal

const profilePic = document.getElementById("profile_image");
const profileModal = document.querySelector(".modal_container");
const img = document.querySelector(".user__information").firstElementChild;

(img) ? img.addEventListener('click', profile_modal): console.log('not found');

function profile_modal() {
  console.log('click event in')
}

if(profilePic) {
  profilePic.addEventListener('click', () => {
    profileModal.classList.add('active');
    document.querySelector(".modal_image").src = profilePic.src;
  })
}
  document.querySelector(".modal_close").addEventListener('click', () => {
  profileModal.classList.remove("active");
});
