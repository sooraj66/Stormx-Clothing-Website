
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

});