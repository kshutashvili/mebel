$(document).ready(function () {

	searchForm();

	var $header = $("#header");

	if ($(window).width() >= 1024) {
		$header.addClass("header-fixed");
	}

	$(window).resize(function () {
		if ($(window).width() >= 1024) {
			$header.addClass("header-fixed");
		} else {
			$header.removeClass("header-fixed");
		}
	});

	function searchForm() {
		var $form = $("#searchForm");
		var $btn = $form.find("button");
		var $input = $form.find("#id_q");
		console.log("$form: ", $form);
		console.log("$btn: ", $btn);

		$btn.off("click");
		$btn.on("click", function (e) {
			e.preventDefault();
			$form.find(".constructor").hide();
			$input.show();
			$(this).off("click");
		});
	};


	$('.bxslider').bxSlider({
		minSlides: 1,
		maxSlides: 1,
		auto: true,
		moveSlides: 1,
		pause: 3000
	});

	$('.bxslider_two').bxSlider({
		pagerCustom: '#bx-pager',
		minSlides: 1,
		maxSlides: 1,
		moveSlides: 1
	});

	var $sliderBlocks = $(".tovar, .catalog");


	$sliderBlocks.each(function () {
		var $slider = $(this).find(".slider");
		var $left = $(this).find("a.left");
		var $right = $(this).find("a.right");
		$slider.bxSlider({
			pager: false,
			nextSelector: $right,
			prevSelector: $left,
			slideWidth: 295,
			minSlides: 2,
			maxSlides: 3,
			moveSlides: 1
		});
	});

	$('.owl-carousel').owlCarousel({
		items: 3,
		margin: 10,
		nav: true,
		responsive: {
			0: {
				items: 1
			},
			600: {
				items: 2
			},
			1000: {
				items: 3
			}
		}
	});

	$('#myTabs a').click(function (e) {
		e.preventDefault()
		$(this).tab('show')
	});


});