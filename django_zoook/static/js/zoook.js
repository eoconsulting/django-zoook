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

    $("#nav .topmenu").hover(function(){
            $('a:first',this).css('color','#703f45');
            },function(){
            $('a:first',this).css('color','#e2001a');
            });
    }

function setLocation(key, value){
    window.location.href = '?'+key+'='+value;
}
