
// nav bar
const mobilMenu = document.querySelector('.box');
const mobilNav = document.querySelector(".mobile");


mobilMenu.addEventListener('click', (e) => {
    mobilMenu.classList.toggle('active')
    mobilNav.classList.toggle('active')
})


//  search part
const search = document.querySelector(".search");
const searchBtn = document.querySelector(".search_btn");
const searchInput = document.querySelector(".search_input");


searchBtn.addEventListener('click', () => {
    search.classList.toggle("active");
    searchBtn.classList.toggle("active");
    searchInput.focus()
})

const searchContainer = document.querySelector(".search__container");
const searchContent = document.querySelector(".search__content");

const searchMsgModal = document.querySelector(".msg__modal");
const searchMsgText = document.querySelector(".msg__modal__content");


if (searchContainer) {
    if (searchContainer.childElementCount === 0) {
        searchContainer.hidden = true;
        searchMsgModal.style.display = "block";
        searchMsgText.textContent =
        "Ooops! Nothing was found. Try again we other keyword.";
      setTimeout(() => {
        searchMsgModal.style.display = "none";
      }, 3000);
    }
}



// sticky header

const userState = document.querySelector("[data-user]").dataset.user;

const stickyNav = document.getElementById('nav');
const navLink = document.querySelectorAll('.nav_link');
const lignes = document.querySelectorAll('.lignes')

const profileIcon = document.getElementById("profile__icon");

if (userState === "AnonymousUser") {
    login_url = "/account/login/";
    profileIcon.parentElement.href = login_url;
    profileIcon.src = "/static/img/im-kick-user.svg";
} else {
    profileIcon.src = "/static/img/moncomptemobile.png";
}


window.addEventListener('scroll', () => {

    if ( window.scrollY > stickyNav.offsetHeight + 150 ) {
        stickyNav.classList.add("active");
        Array.from(navLink).forEach(link => {
            link.classList.add('scroll')
        })
        mobilMenu.style.border = "1px solid black";
        
        Array.from(lignes).forEach((ligne) => {
            ligne.style.color = "black";
        });
        userStateFunc();
    }
    else {
        stickyNav.classList.remove("active");
        Array.from(navLink).forEach((link) => {
            link.classList.remove("scroll");
        });

        mobilMenu.style.border = "1px solid white";

        Array.from(lignes).forEach((ligne) => {
            ligne.style.color = "white";
        });

        // profileIcon.src = "/static/img/moncomptemobile.png";
        userStateFunc();
    }
})


// const overView = document.querySelector("#overview");
// console.log(overView)
function userStateFunc() {
    if (userState === "AnonymousUser") {
        profileIcon.src = "/static/img/im-kick-user.svg";
        // overView.classList.remove('active');
        // overView.innerHTML = "Login first";
    } else  {
        // overView.classList.remove("active");
        if (window.scrollY > stickyNav.offsetHeight + 150) {
            profileIcon.src = "/static/img/user.svg";
        } else {
                profileIcon.src = "/static/img/moncomptemobile.png";
        }
    }
}




// header section loading

const headerText = document.querySelectorAll(".header_text");

const bg = document.getElementsByTagName('header');

document.addEventListener('DOMContentLoaded', () => {
    // let load = 0;
    // let int = setInterval(blurring, 10);
    blurring();
})

let load = 0;
let int = setInterval(blurring, 5);

function blurring() {
    load++;
    if (load > 99) {
        clearInterval(int);
    }
    Array.from(headerText).forEach(item => {
        item.style.opacity = scale(load, 0, 100, 0, 1);
    } );
    Array.from(bg).forEach(item => {
        item.style.filter = `blur(${scale(load, 0, 100, 30, 0)}px)`;
    });

//   loadText.innerText = `${load}%`;
//   headerText.style.opacity = scale(load, 0, 100, 1, 0);
//   bg.style.filter = `blur(${scale(load, 0, 100, 30, 0)}px)`;
}




// https://stackoverflow.com/questions/10756313/javascript-jquery-map-a-range-of-numbers-to-another-range-of-numbers
const scale = (num, in_min, in_max, out_min, out_max) => {
  return ((num - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min
}

