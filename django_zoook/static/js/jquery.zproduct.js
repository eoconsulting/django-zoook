jQuery(document).ready(function($)
{
	// DESCRIPTION TABS
	$(".tab-content").hide();
	$(".tabs li:first").addClass("active").show();
	$(".tab-content:first").show();

	// Change tabs and content on click. href of A tabs is ID in tab content
	$(".tabs li").click(function(event)
       {
		  event.preventDefault();
		$(".tabs li").removeClass("active");
		$(this).addClass("active");
		$(".tab-content").fadeOut(10);

		var activeTab = $(this).find("a").attr("href");
		$(activeTab).fadeIn();

		return false;
	});

$(".tabs a").click(function (event) {
  event.preventDefault();
});
	
	// IMAGES PRODUCT
	// Zoom thumbnails where pointer is hover
	$(".other-img li").hover(function() {
		$(this).css({'z-index' : '10'});
		$(this).find('img').addClass("hover").stop()
			.animate({
				marginTop: '-75px', 
				marginLeft: '-75px', 
				top: '50%', 
				left: '50%', 
				width: '150px', 
			}, 200);
		
		} , function() {
		$(this).css({'z-index' : '0'});
		$(this).find('img').removeClass("hover").stop()
			.animate({
				marginTop: '0', 
				marginLeft: '0',
				top: '0', 
				left: '0', 
				width: '58px', 
			}, 400);
	});
 
	// Swap principal image on click in thumbnails
	$(".other-img a").click(function() {
		var mainImage = $(this).attr("href"); //Find Image Name
		$(".product-img img").attr({ src: mainImage });
		$("a.product-img").attr({ href: mainImage });
		return false;		
	});
	
	// ZOOM FOR PRODUCT
	// Product principal image zoom hover animation
	$(".product-img").hover(function() {
		$('.zoom-icon', this).css({'z-index' : '10'}).css({'display' : 'block'});
		$('.zoom-icon', this).animate({
				opacity: '.3', 
			}, 200);
		
		} , function() {
		$('.zoom-icon', this).animate({
				opacity: '0.0', 
			}, 200);
		$('.zoom-icon', this).css({'z-index' : '0'});
	});

}); 