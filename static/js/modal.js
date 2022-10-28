

const detailImage = document.querySelectorAll(".product_detail_image");

const modalContent = document.querySelector(".modal_content");

const modalContainer = document.querySelector(".modal_container");

const modalImage = document.querySelector(".modal_image");

// Array.from(detailImage).forEach(image => {
//     image.addEventListener('click', imageModalShow)
// })

Array.from(detailImage).forEach((image) => {
    image.addEventListener("click", (e) => {
        if (e.type == "click") {
            modalContainer.classList.add("active");
            modalImage.src = image.src;
        }
    });
});

// function imageModalShow(e) {
//     if(e.type == "click") {
//         modalContainer.classList.add('active')

//         modalImage.src = image.src;
//         console.log('click')
//     }
// }

const closeModalBtn = document.querySelector(".modal_close");

if (closeModalBtn) {
    closeModalBtn.addEventListener("click", (e) => {
        console.log("remove");
        modalContainer.classList.remove("active");
    });

}