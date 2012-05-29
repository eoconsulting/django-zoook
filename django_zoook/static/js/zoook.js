/*!
 * Zoook JavaScript Library
 * https://launchpad.net/zoook
 *
 * Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
 * GNU General Public License
 */
function mainmenu()
{
    $("#nav .sub").css({display: "none"}); // Correcció per opera
    $("#nav .topmenu").hover(function(){
            $(this).find('.sub').css({visibility: "visible",display: "none"}).fadeIn(250);
            },function(){
            $(this).find('.sub').fadeOut(200);
            });
}

function setLocation(key, value){
	window.location.href = putURLParam(window.location.href, key, value);
}

function getURLParam(url, paramName) {
	var strReturn = null;
	if(url.indexOf('?') > -1) {
		var strQueryString = url.substr(url.indexOf('?')).toLowerCase();
		var aQueryString = strQueryString.split('&');
		for(var iParam = 0; iParam < aQueryString.length; iParam++) {
			if(aQueryString[iParam].indexOf(paramName + '=') > -1) {
				var aParam = aQueryString[iParam].split('=');
				if(aParam[1]!=null && aParam[1]!='') {
					strReturn = aParam[1];
				}
				break;
			}
	    }
	}
	if(strReturn!=null && strReturn.indexOf('#') > -1) {
		return strReturn.substr(0, strReturn.indexOf('#'));
	}
	return strReturn;
}

function hasURLParams(url) {
	return url.indexOf('?')!=-1
	        && url.indexOf('?')!=url.length-1;
}

function putURLParam(url, paramName, paramValue) {
	var newUrl = url;
	var newParamAndValue = paramName + '=' + paramValue;
	if(!hasURLParams(url)) {
		if(newUrl.indexOf('?')!=url.length-1) {
			newUrl += '?';
		}
		newUrl += newParamAndValue;
	} else if(getURLParam(url, paramName)==null) {
		newUrl += '&' + newParamAndValue;
	} else {
		var currentParamAndValue = paramName + '='
		       + getURLParam(url, paramName);
		newUrl = url.replace(currentParamAndValue, newParamAndValue);
	}
	return newUrl;
}
