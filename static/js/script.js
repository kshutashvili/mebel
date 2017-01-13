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

 
});