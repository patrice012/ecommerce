// add to cart using ajax
const addToCartBtn = document.querySelectorAll(".add_to_cart_btn");

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

csrftoken = getCookie("csrftoken");

Array.from(addToCartBtn).forEach((btn) => {
  btn.addEventListener("submit", (e) => {
    e.preventDefault();
    const id = e.target.dataset.productId;
    const name = e.target.dataset.productName;
    productNumber = document.getElementById("user_product_quantity").value;

    if (productNumber <= 0) {
      productNumber = 1;
    }

    if (is_login_user()) {
      add_product(id, name, productNumber);
      get_cart_items_number();
    } else {
      save_unlogged_data(id, name);
      console.log("not working");
    }
  });
});

// if (is_login_user()) {
//     if(localStorage.length> 0) {
//         data = get_unlogged_datas()
//         for (i of data) {
//             add_product(i, "None", "None")
//         }
//     }
//     console.log('working')
// }

function get_unlogged_datas() {
  data = {};
  for (let i = 0; i < localStorage.length; i++) {
    let key = Number(localStorage.key(i));
    let value = localStorage.getItem(key);
    console.log(typeof key);
    data[key] = value;
    // data[occurences] =
  }
  return data;
}

function save_unlogged_data(id, name) {
  data = get_unlogged_datas();
  localStorage.setItem(id, name);
}

function add_product(id, name, productNumber) {
  const url = "../../../action/add/";

  data = {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ id: id, name: name, productNumber: productNumber }),
  };

  fetch(url, data)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw (error) => console.log(error);
      }
    })
    .then((data) => {
      const prodMsgModal = document.querySelector(".msg__modal");
      const msgTextProd = document.querySelector(".msg__modal__content");

      if (data["message"]) {
        prodMsgModal.style.display = "block";
        msgTextProd.textContent = data["message"];
      }
      setTimeout(() => {
        prodMsgModal.style.display = "none";
      }, 2500);
    });
}

function is_login_user() {
  let user = document.querySelector("[data-user]").dataset.user;
  if (user === "AnonymousUser") {
    return false;
  } else {
    return true;
  }
}

// request cart item number in the database set inetval 1000ms
const userCartNumber = document.querySelector(".cart_item_number");
const cartOverView = document.querySelector(".cart__overview");

const get_cart_items_number = () => {
  let interva = setInterval(cart_items, 500);
  setTimeout(() => {
    clearInterval(interva);
  }, 3000);
};

const cart_items = () => {
  if (is_login_user()) {
    fetch("/action/i/")
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          console.log("error");
        }
      })
      .then((data) => {
        if (data["cart_item_number"]) {
          userCartNumber.innerHTML = data["cart_item_number"];
        } else {
          userCartNumber.innerHTML = "";
        }
      })
      .catch((error) => console.log(error));
  }
};

cart_items();



//  cart overview item then clicking in btn
const cartBtn = document.querySelector(".cart_item_link");
cartBtn.addEventListener("click", () => {
  cartOverView.classList.toggle("active");
});

//  increase or decrease cart item in cart page using AJAX
const increaseBtn = document.querySelectorAll(".increase");
const decreaseBtn = document.querySelectorAll(".decrease");

Array.from(increaseBtn).forEach((btn) =>
  btn.addEventListener("click", cartActionFunction)
);
Array.from(decreaseBtn).forEach((btn) =>
  btn.addEventListener("click", cartActionFunction)
);

function cartActionFunction(e) {
  e.preventDefault();
  let productId = e.target.dataset.productId;
  let productName = e.target.dataset.productName;
  let productQuantity =
    e.target.parentElement.parentElement.previousElementSibling;
  let productPrice = e.target.parentElement.parentElement.nextElementSibling;
  let productDiv = e.target.parentElement.parentElement.parentElement;
  const cartSubTotal = document.getElementById("cart_subtotal");
  const cartTotal = document.getElementById("cart_total");

  if (e.target.name === "increase") {
    cartAction = e.target.name;
  } else if (e.target.name === "decrease") {
    cartAction = e.target.name;
  }

  let send_data = () => {
    const url = "../cart-action/";
    fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        id: productId,
        name: productName,
        action: cartAction,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        const quantity = data["quantity"];
        if (quantity >= 1) {
          productQuantity.textContent = quantity;
          console.log(quantity, "inner quantity");
          productPrice.textContent = `$ ${data["price"]}`;
        } else if (quantity == 0) {
          confirm;
          productDiv.remove();
        }
        cartSubTotal.textContent = `$ ${data["cart_sub_total"]}`;
        cartTotal.textContent = `$ ${data["cart_total"]}`;
      })
      .catch((error) => {
        if (error) {
          console.log(error);
        }
      });
  };

  if (productQuantity.textContent == 1 && e.target.name === "decrease") {
    const action = confirm(`${productName} will be delete in your cart!`);
    if (action) {
      send_data();
      get_cart_items_number();
    }
  } else {
    send_data();
  }
}

// cart overview item for 4 items only
let start = 0;
let step = 4;
let next = step;
const cartItem = document.querySelectorAll(".car__overview__container");
let arrayItem = Array.from(cartItem);
let itemsNumber = arrayItem.length;
const previousBtn = document.getElementById("previous_items");
const nextBtn = document.getElementById("next_items");

previousBtn.addEventListener("click", nextFunction);
nextBtn.addEventListener("click", nextFunction);

resetItemView();
showItem(start, next);
previousBtn.hidden = true;
cartBtnState(itemsNumber);

function cartBtnState(itemsNumber) {
  if (itemsNumber > 0) {
    if (itemsNumber <= step) {
      previousBtn.style.display = "none";
      nextBtn.style.display = "none";
    }
    nextFunction();
  } else {
    document.querySelector(".cart__overview").innerHTML = emptyCart();
  }
}

function nextFunction() {
  unshow = itemsNumber - next;
  // check if the number for item to show is more than the current pagination number
  if (unshow >= next) {
    resetItemView();
    showItem(start, next);
    previousBtn.hidden = true;
    nextBtn.hidden = false;
    start = next;
    next += next;
  }
  // if unshow is less than the element to display
  else if (unshow < next) {
    previousBtn.hidden = true;
    nextBtn.hidden = false;
    resetItemView();
    // if the current next paginator is more than item number => iterate from start to items number because if next is more than item number we will have indexerror
    if (next > itemsNumber) {
      showItem(start, itemsNumber);
    } else {
      // iterate to the next element
      showItem(start, next);
    }

    // if next is mre than item numbers reinitialise all variables else we continue
    if (next >= itemsNumber) {
      start = 0;
      next = step;
      nextBtn.hidden = true;
      previousBtn.hidden = false;
    } else {
      start = next;
      next += next;
    }
    // console.log("end", start, next);
  }
}

function showItem(start, end) {
  // display the current range of items
  for (let i = start; i < end; i++) {
    if (arrayItem[i] !== undefined) {
      arrayItem[i].style.display = "flex";
    }
  }
}

function resetItemView() {
  // hidde all items
  arrayItem.forEach((item) => {
    item.style.display = "none";
  });
}

function emptyCart() {
  console.log("empty cart item");
  url = "/list/";
  htmlDiv = `<div class="emty-cart">
                <span>Ooooops Your cart is empty now.</span>
                <a id="shop-url" href=${url}>Buy something now...</a>
            </div>`;
  return htmlDiv;
}
