(function($) {

    $.zUpdatePrice = function(element, options) {

 		// Default options of plugin
        var defaults = {
            timeInterval: '10000',
            delayUpdater: '5000',
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

			// Activem l'interval d'actualització de preus
//			setInterval( function() {

			if(!element.timeInterval) { element.timeInterval = plugin.settings.timeInterval }
			if(!element.idPriceAttr) { element.idPriceAttr = plugin.settings.idPriceAttr }
			if(!element.textAlert) { element.textAlert = plugin.settings.textAlert }
			if(!element.url) { element.textAlert = plugin.settings.url }
			if(!element.delayUpdater) { element.delayUpdater = plugin.settings.delayUpdater }

			// Recorro tot el contingut cercant els price-box per obtenir la id del div i extreure el ID del producte
			var ids_sended;
			var ids_product = [];
			var id_extract;
			
			if( !ids_sended )
			{
				$('.price-box').each( function()
					{
						id_extract = $(this).prop('id');
						ids_product.push( id_extract.replace(element.idPriceAttr ,'') );
					}
				);
				ids_sended =  ids_product.join(',');
			}

			// Coloquem el loader cada cop que demani dades als preus del contingut
			$('body').ajaxSend(function() {
				if( $('#update-price-info').length == 0 ) {
					$(this).prepend('<div id="update-price-info">'+ element.textAlert +'</div>');
				}
				$('#update-price-info').fadeIn(250).delay(element.delayUpdater).fadeOut(250);
			});

			$.getJSON(element.url, {"ides": ids_sended}, function(data) 
			{ 
					$.each(data, function(product, prices) {
						var pricesEl = $('#'+element.idPriceAttr+ product+' .regular-price .price')
						if(pricesEl[0].innerHTML.trim() != prices.regularPrice) {
							pricesEl.animate({opacity:0.5},250, function() { $(this).animate({opacity:1},250) })
								    .addClass('special-price')
								    .parent().append('<p class="price">' + prices.regularPrice + '</p>');
						}
					});
				} 
			 )
			 .success( function() {  } )
			 .error( function() {  } );
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