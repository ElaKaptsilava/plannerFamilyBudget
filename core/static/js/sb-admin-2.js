(function ($) {
    "use strict"; // Start of use strict

    // Toggle the side navigation
    $("#sidebarToggle, #sidebarToggleTop").on('click', function (e) {
        $("body").toggleClass("sidebar-toggled");
        $(".sidebar").toggleClass("toggled");
        if ($(".sidebar").hasClass("toggled")) {
            $('.sidebar .collapse').collapse('hide');
        }
        ;
    });

    // Close any open menu accordions when window is resized below 768px
    $(window).resize(function () {
        if ($(window).width() < 768) {
            $('.sidebar .collapse').collapse('hide');
        }
        ;

        // Toggle the side navigation when window is resized below 480px
        if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
            $("body").addClass("sidebar-toggled");
            $(".sidebar").addClass("toggled");
            $('.sidebar .collapse').collapse('hide');
        }
        ;
    });

    // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
    $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function (e) {
        if ($(window).width() > 768) {
            var e0 = e.originalEvent,
                delta = e0.wheelDelta || -e0.detail;
            this.scrollTop += (delta < 0 ? 1 : -1) * 30;
            e.preventDefault();
        }
    });

    // Scroll to top button appear
    $(document).on('scroll', function () {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });

    // Smooth scrolling using jQuery easing
    $(document).on('click', 'a.scroll-to-top', function (e) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top)
        }, 1000, 'easeInOutExpo');
        e.preventDefault();
    });

})(jQuery); // End of use strict

function showFields() {
    var type = document.getElementById('id_type').value;
    var expenseDiv = document.getElementById('div_id_category_expense');
    var runningCostDiv = document.getElementById('div_id_category_running_cost');
    var targetDiv = document.getElementById('div_id_target');

    if (type === 'needs') {
        expenseDiv.classList.remove('hidden');
        runningCostDiv.classList.remove('hidden');
        targetDiv.classList.add('hidden');
    } else if (type === 'wants') {
        expenseDiv.classList.add('hidden');
        runningCostDiv.classList.add('hidden');
        targetDiv.classList.remove('hidden');
    } else {
        expenseDiv.classList.add('hidden');
        runningCostDiv.classList.add('hidden');
        targetDiv.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    showFields();  // To set the initial state based on the default selected value
});
