$(document).ready(function () {

    // --- Update cart count dynamically ---
    function updateCartCount() {
        fetch('/get-cart-count/')
            .then(response => response.json())
            .then(data => {
                const cartCountEl = document.getElementById('cart-count');
                if (cartCountEl) {
                    cartCountEl.textContent = data.cart_count;
                }
            })
            .catch(error => console.error('Error fetching cart count:', error));
    }

    // --- Increment quantity ---
    $('.increment-btn').click(function (e) {
        e.preventDefault();
        let qtyInput = $(this).closest('.input-group').find('.qty-input');
        let currentVal = parseInt(qtyInput.val());
        if (!isNaN(currentVal) && currentVal < 10) {
            qtyInput.val(currentVal + 1);
        }
    });

    // --- Decrement quantity ---
    $('.decrement-btn').click(function (e) {
        e.preventDefault();
        let qtyInput = $(this).closest('.input-group').find('.qty-input');
        let currentVal = parseInt(qtyInput.val());
        if (!isNaN(currentVal) && currentVal > 1) {
            qtyInput.val(currentVal - 1);
        }
    });

    // --- Add to Cart ---
    $('.addToCartBtn').click(function (e) {
        e.preventDefault();

        let parentDiv = $(this).closest('.product-data');
        let product_id = parentDiv.find('.prod_id').val();
        let product_qty = parentDiv.find('.qty-input').val();
        let token = $('input[name=csrfmiddlewaretoken]').val();

        if (!product_id) {
            console.error("❌ Product ID not found. Check your HTML structure.");
            return;
        }

        $.ajax({
            method: "POST",
            url: `/add-to-cart/${product_id}/`,
            data: {
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                alert(response.message);
                updateCartCount();  // 🔥 Live update cart count
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseText);
            }
        });
    });

});
