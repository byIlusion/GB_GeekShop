window.onload = function () {

    let form_row_selector = '.formset_row';

    orderSummaryUpdate();

    function orderSummaryUpdate() {
        let total_quantity = 0;
        let total_cost = 0;
        $(form_row_selector).each(function (i, el) {
            let quantity = 0;
            let cost = 0;
            if (!$('input[name="orderitems-' + i + '-DELETE"]').prop('checked')
                && $('select[name="orderitems-' + i + '-product"]').val()) {
                quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
                cost = parseFloat($('.orderitems-' + i + '-price').text().replace(/,/g, '.')) * quantity;
                total_quantity += quantity;
                total_cost += cost;
            }
        });
        $('.order_total_quantity').text(total_quantity);
        $('.order_total_cost').text(printPrice(total_cost));
    }

    function deleteOrderItem(e) {
        $(e).find('[type="number"]').val(0);
        orderSummaryUpdate();
    }

    function addedOrderItem(e) {
        let formset_row_count = $('.formset_row').length;
        let = select = $(e).find('select');
        let num = parseInt($(select).attr('name').split('-')[1]);
        console.log(num);
        $(e).find('input, select').each(function (i, el) {
            let attr = 'orderitems-' + (formset_row_count - 1) + '-' + $(el).attr('name').split('-')[2];
            $(el).attr('name', attr).attr('id', 'id_' + attr);
        });
        $(e).find('select').val('');
        $(e).find('.orderitems-' + num + '-price').removeClass('orderitems-' + num + '-price').addClass('orderitems-' + (formset_row_count - 1) + '-price').text(printPrice(0));
    }

    function printPrice(price) {
        return parseFloat(price).toFixed(2).replace('.', ',');
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitem',
        removed: deleteOrderItem,
        added: addedOrderItem,
    });


    $(document).on('change', 'input[type="number"]', function () {
        orderSummaryUpdate();
    });


    $(document).on('change', 'select', function () {
        let product_id = $(this).val();
        let num = parseInt($(this).attr('name').split('-')[1]);
        console.log(product_id);
        $.ajax({
            url: '/products/info/' + product_id + '/',
            success: function (data) {
                if (data) {
                    $('input[type="number"]').attr('max', data.quantity).val(1);
                    $('.orderitems-' + num + '-price').text(printPrice(data.price));
                }
            },
            complete: function () {
                orderSummaryUpdate();
            },
        });
    });
}
