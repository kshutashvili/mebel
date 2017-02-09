$(document).ready(function(){
  $('.bxslider').bxSlider({
	  minSlides: 1,
	  maxSlides: 1,
	  auto: true,
	  moveSlides: 1,
	  pause: 3000
	});

  $('#myTabs a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
	});

	 $('.bxslider_two').bxSlider({
	  pagerCustom: '#bx-pager', 
	  minSlides: 1,
	  maxSlides: 1,
	  moveSlides: 1
	});
});