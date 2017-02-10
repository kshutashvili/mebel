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

	$('.owl-carousel').owlCarousel({
		items:3,
	    margin:10,
	    nav:true, 
	    responsive:{
	        0:{
	            items:1
	        },
	        600:{
	            items:2
	        },
	        1000:{
	            items:3
	        }
	    }
	})

	 $(".search_button").click(function (){
  		$(".dis_inp").css("display", "inline-block");
		 $(".dis_inp").css("display", "inline-block");
  		$(".constructor").css("display", "none");
  	});


});