$(document).ready(function () {

	$('.bxslider').bxSlider({
		minSlides: 1,
		maxSlides: 1,
		auto: true,
		moveSlides: 1,
		pause: 3000
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

	$('#myTabs a').click(function (e) {
		e.preventDefault()
		$(this).tab('show')
	});


});