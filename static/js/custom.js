function showLargeImage(imageSrc) {
    $('#main-image').attr('src', imageSrc);
    $('#show-main-image-modal').attr('href', imageSrc);
}

function addProductComment(productId) {
    var comment = $('#commentText').val();
    $.get('/products/add-product-comment', {
        product_comment: comment,
        product_id: productId
    }).then(res => {
        console.log(res)
    }).catch(error => {
        console.error("Error:", error);
    });
}

function fillPage(page) {
    $('#page').val(page);
    $('#paginate-form').submit();
}

function paginate_by(page) {
    $('#paginate_by').value(page);
    $('#paginate_form').submit();
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('blog_comments_area').scrollIntoView({behavior: 'smooth'})
}


function changeOrderDetailCount(detailId, state) {
    $.get('/account/change-order-count', {
        detail_id: detailId,
        state: state
    }).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    })
}

function delOrderDetail(detailId) {
    $.get('/account/remove-order-detail', {
        detail_id: detailId
    }).then(res => {
        if (res.status === 'remove_success') {
            $('#order-detail-content').html(res.body)
            Swal.fire({
                title: "Notice",
                text: res.text,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: res.confirm_button_text,
            })
        }
    })
}

function addProductToOrder(productId) {
    const productCount = $('#product_count').val()
    $.get('/order/add-to-order/', {
        product_id: productId,
        count: productCount
    }).then(res => {
        Swal.fire({
            title: "Notice",
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: res.confirm_button_text,
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = res.redirect_url;
            }
        });
    });
}

function listAddToCart(productId, count) {
    $.get('/order/add-to-order/', {
        product_id: productId,
        count: count
    }).then(res => {
        Swal.fire({
            title: "Notice",
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: res.confirm_button_text,
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = res.redirect_url;
            }
        });
    });
}

// document.getElementById('payment-form').addEventListener('submit', function (event) {
//     event.preventDefault();
//     let selectedOption = document.querySelector('input[name="selector"]:checked');
//     let orderId = document.getElementById('order-id').value;  // خواندن مقدار id
//     if (selectedOption) {
//         if (selectedOption.value === 'door_to_door') {
//             this.action = `/account/successful-purchase/${orderId}`;
//         } else if (selectedOption.value === 'zarinpal') {
//             this.action = `/account/successful-purchase/${orderId}`;
//         }
//         this.submit();
//     }
// });