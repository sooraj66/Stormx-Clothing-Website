
$(document).ready(function() {
    $.ajaxSetup({
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
                }
            });

//$('#buy-now').click(function() {
//const itemId = $(this).data('item-id');
//const sizeId = $('#select-size').val();
//console.log(sizeId);
//const catName = $(this).data('category-name');
//    $.ajax({
//        url: '/order/'+ catName + '/' + itemId,  // URL to your backend view
//        method: 'POST',
//        data:{
//          'item_id':itemId,
//          'category_name' : catName,
//          'size_id' : sizeId,
//        },
//        success: function(response) {
//            // Handle success, like redirecting to order page
//            window.location.href = "/order/"+ catName +'/'+ itemId;
//        },
//        error: function(error) {
//            // Handle error
//            alert('Something went wrong');
//        }
//    });
//});



$('#add-to-cart').click(function() {
    const itemId = $(this).data('item-id');
    const sizeId = $('#select-size').val();
    console.log(sizeId);
    $.ajax({
        url: '/add-to-cart',  // URL to your backend view
        method: 'POST',
        data: {
            'item_id': itemId,
            'size_id' : sizeId,
        },
        success: function(response) {
            if (response.message === "item already in cart"){
                $('#wishlist-message').text('Item already in cart');
                $('#wishlist-message').css('color','orange');
            }
            else if (response.message === 'please select a size'){
                $('#wishlist-message').text('please select size');
                $('#wishlist-message').css('color','red');
            }
            else {
                $('#wishlist-message').text('Item added to cart');
                $('#wishlist-message').css('color','green');
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
                $('#wishlist-message').text('Item already in wishlist');
                $('#wishlist-message').css('color','orange');
            } else {
                $('#wishlist-message').text('Item added to wishlist');
                $('#wishlist-message').css('color','green');
                $('.offcanvas-body').html(response.wishlist_html);
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


$('.order-quantity').change(function(){
console.log("hi")
    const Qty = $(this).find(':selected').data('qty-no');
    console.log(Qty)
    const clothId = $(this).find(':selected').data('cloth-id');
    console.log(clothId)
    const hiddenQuantityInput = document.querySelector('input[name="quantity"]');
    hiddenQuantityInput.value = Qty
    console.log(hiddenQuantityInput)
    $.ajax({
        url: '/updateQuantity',
        method: 'post',
        data: {
            'qty': Qty,
            'cloth_id': clothId,
        },
        success: function(response) {
            pass
        },
        error: function(response) {
            alert('Something went wrong');
        }
    });
});




$('.filter-select').change(function(){
console.log("changed")
    const sizeId = $('#size-select').val();
    console.log(sizeId)
    const priceId = $('#price-select').val();
    console.log(priceId)
    const categoryId = $(this).data('category-id');
    $.ajax({
        url: '/category/'+ categoryId,
        method: 'post',
        data: {
            'size_id': sizeId,
            'price':priceId,
            'category_id': categoryId
        },
        success: function(response) {
            $('.itemBody').html(response.clothitems_html);
        },
        error: function(response) {
            alert('Something went wrong');
        }
    });
});

});