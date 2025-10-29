$(document).ready(function () {
    $('.increment-btn').click(function (e) {
        e.preventDefault();
        var qty = $(this).closest('.input-group').find('.qty-input');
        var value = parseInt(qty.val());
        value = isNaN(value) ? 1 : value;
        if (value < 10) { // optional max limit
            qty.val(value + 1);
        }
    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();
        var qty = $(this).closest('.input-group').find('.qty-input');
        var value = parseInt(qty.val());

        value = isNaN(value) ? 1 : value;
        if (value > 1) {
            qty.val(value - 1);
        }
    });
    $('.addToCartBtn').click(function (e){
        e.preventDefault();
        var product_id = $('.prod_id').val();
        var product_qty = $('.qty_input').val();
        var token=$('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method:"POST",
            url:"/add-to-cart",
            data:{
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken:token
            },
            dataType:"dataType",
            success:function(response){

            }

        })
    });

});