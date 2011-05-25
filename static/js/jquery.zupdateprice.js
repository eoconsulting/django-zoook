(function($) {
 
    $.zUpdatePrice = function(element, options) {

 		// Default options of plugin
        var defaults = {
			url: '../json/test.php',
            timeInterval: '10000',
			idPriceAttr: 'product-price-',
			textAlert: 'Updating prices ...'
        }
		
		// Vars for avoid confusions
        var plugin = this;
 
        plugin.settings = {}
 
        var $element = $(element),
             element = element;
 
        plugin.init = function() {
// ---------------------------------------------------------- PLUGIN ACTION --------------------------------------------------
            plugin.settings = $.extend({}, defaults, options)
			var ides_envio;
			// Activem l'interval d'actualització de preus
			setInterval( function() {

			if(!element.timeInterval) { element.timeInterval = plugin.settings.timeInterval }
			if(!element.idPriceAttr) { element.idPriceAttr = plugin.settings.idPriceAttr }
			if(!element.textAlert) { element.textAlert = plugin.settings.textAlert }
			if(!element.url) { element.textAlert = plugin.settings.url }
			
			// Recorro tot el contingut cercant els price-box per obtenir la id del div i extreure el ID del producte
			var ides_producto = [];
			var ide_extract;
			
			if( !ides_envio )
			{
			$('#content .price-box').each( function()
				{
					ide_extract = $(this).prop('id');
					ides_producto.push( ide_extract.replace(element.idPriceAttr ,'') );
				}
			);
				// Coloquem el loader cada cop que demani dades als preus del contingut
				$('body').ajaxSend(function() {
				  $(this).prepend('<div id="update-price-info">'+ element.textAlert +'</div>');
				  $('#update-price-info').fadeIn(250);
				});
				ides_envio =  ides_producto.join(',');
			}
					
				 $.getJSON(element.url, {"ides": ides_envio}, function(data) 
					{ 
						// Recorro el JSON retornat per test.php amb les IDS=product i els PREUS=prices
						// Faig un petit efecte d'opacitat per resaltar els preus
						$.each(data, function(product, prices){
							$('#'+ element.idPriceAttr + product +' .price').animate({opacity:0.5},250, function() { $(this).animate({opacity:1},250) })
							.html( prices.regularPrice ); 
						});
					} 
				 )
				 .success( function() { $('#update-price-info').fadeOut(250).remove(); } )
				 .error( function() { $('#update-price-info').fadeOut(250).remove(); } ); 
			
			}, element.timeInterval); // end setInterval

        }
        plugin.init();
 
    }
	
// ---------------------------------------------------------- DONT MODIFY --------------------------------------------------
    $.fn.zUpdatePrice = function(options) {
 
        return this.each(function() {
            if (undefined == $(this).data('zUpdatePrice')) {
                var plugin = new $.zUpdatePrice(this, options);
                $(this).data('zUpdatePrice', plugin);
            }
        });
 
    }
 
})(jQuery);