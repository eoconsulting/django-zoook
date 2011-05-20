/*!
 * Zoook JavaScript Library
 * https://launchpad.net/zoook
 *
 * Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
 * GNU General Public License
 */

function setLocation(key, value){
    window.location.href = '?'+key+'='+value;
}

function addCart(sku){
    window.location.href = '/checkout/cart/'+sku;
}
