
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
                alert('Item already in cart');
            }
            else if (response.message === 'please select a size'){
                alert('please select a size')
            }
            else {
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
            alert("quantity-updated")
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