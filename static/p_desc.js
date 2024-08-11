
$(document).ready(function() {
    $.ajaxSetup({
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
                }
            });

    $('#buy-now').click(function() {
    const itemId = $(this).data('item-id');
    console.log(itemId)
    const catName = $(this).data('category-name');
    console.log(catName)

        $.ajax({
            url: '/order/'+ catName + '/' + itemId,  // URL to your backend view
            method: 'GET',
            success: function(response) {
                // Handle success, like redirecting to order page
                window.location.href = "/order/"+ catName +'/'+ itemId;
            },
            error: function(error) {
                // Handle error
                alert('Something went wrong');
            }
        });
});



    $('#add-to-cart').click(function() {
    const itemId = $(this).data('item-id');

    $.ajax({
        url: '/add-to-cart',  // URL to your backend view
        method: 'POST',
        data: {
            'item_id': itemId,
        },
        success: function(response) {
        if (response.message === "item already in cart"){
            alert('Item already in cart');
        }
        else{
            alert('Item added to cart');
        }

        },
        error: function(error) {
            alert('Something went wrong');
        }
    });
});

$('.add-to-wishlist').click(function() {
    const itemId = $(this).data('item-id');
    console.log(itemId);
    const categoryId = $(this).data('category-id');
    console.log(categoryId);
    $.ajax({
        url: '/'+ categoryId + '/' + itemId,  // URL to your backend view
        method: 'POST',
        data: {
            'item_id': itemId,
            'category_id': categoryId,
        },
        success: function(response) {
            if (response.message === "item already in wishlist"){
                alert('Item already in wishlist');
            } else {
                alert('Item added to wishlist');
                $('.offcanvas-body').html(response);
            }
        },
        error: function(error) {
            alert('Something went wrong');
        }
    });
});


$('.quantity').change(function(){
    const Qty = $(this).find(':selected').data('qty-no');
    const clothId = $(this).find(':selected').data('cloth-id');
    $.ajax({
        url: '/updateQuantity',
        method: 'post',
        data: {
            'qty': Qty,
            'cloth_id': clothId,
        },
        success: function(response) {
            window.location.href = "/cart";
        },
        error: function(response) {
            alert('Something went wrong');
        }
    });
});


});