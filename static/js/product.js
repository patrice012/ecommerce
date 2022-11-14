// PRODUCT DETAIL SKEW ANIMATION

const curentProductImage = document.querySelector(
  ".product_detail_image"
);


if(curentProductImage) {
  curentProductImage.addEventListener("mouseover", skewImage);
}

function skewImage(e) {
  if ((e.type = "mouseover")) {
    curentProductImage.classList.add("active");
  } else {
    curentProductImage.classList.remove("active");
  }
}


//  change current image to one image in gallery
const productGallery = document.querySelectorAll(
  ".product_detail_image_gallery"
);

Array.from(productGallery).forEach(images => images.addEventListener('click', changeProductImage))


function changeProductImage(e) {
  const currentSrc = curentProductImage.src;
  curentProductImage.src = e.target.src;
  curentProductImage.classList.add("active_img");
  e.target.src = currentSrc
  e.target.classList.add("active_img");
  
  setInterval(()=> {
    curentProductImage.classList.remove("active_img");
    e.target.classList.remove("active_img");
  },
  1000)
}

//  delete product action

let delProduct = document.querySelector('.remove_prod');
if (delProduct) {
  delProduct.addEventListener('click', confirm_delete)
}

function confirm_delete(e) {
  if ( !confirm('This product would be deleted. Confirm?')) {
    e.preventDefault()
    console.log('event')
  }
}



