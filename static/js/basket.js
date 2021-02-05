(function ($) {

    $(document).ready(function () {
        $('#basket').on('change', '.item-quantity', (e) => {
            $.ajax({
                url: '/basket/edit/' + e.target.name + '/' + e.target.value + '/',
                success: (data) => {
                    if (data) {
                        $('#basket').html(data.result);
                    }
                }
            });
        });

        // Функция работает, но не используется
        // Для включения:
        // 1. Раскоментить кнопку в шаблоне страницы товаров (закоментить ссылку)
        // 2. Раскоментить JsonResponse() в контроллере (закоментить render())
        $(document).on('click', '.add-to-basket', (e) => {
            $.ajax({
                url: '/basket/add/' + $(e.target).attr('data-product') + '/',
                success: (data) => {
                    console.log(data);
                }
            });
        });
    });

})(jQuery);