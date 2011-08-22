    window.onload = function()
    {
        // create the FCK Editor and replace the specific text area with it        
		var eid = ['id_content', 'id_description_en', 'id_summary', 'id_quote'];
		for(i=0;i<eid.length;i++){
			if($(eid[i])){  
				$$('label[for=' + eid[i] + ']')[0].setStyles({
					"display":"block", 
					"clear":"both", 
					"width":"100%", 
					"height":"18px"
				});

				var contentElement = new Element('div', {id: 'contentElement'});
				contentElement.setStyles({
					"display":"block", 
					"clear":"both", 
					"width":"100%", 
					"height":"3px"
				});
				contentElement.inject(eid[i], "before");

				var CKeditor = new CKEDITOR.replace(eid[i], { 
					customConfig : '', 
					language : 'en', 
					filebrowserBrowseUrl: '/static/js/filemanager/index.html',
					filebrowserImageBrowseUrl : '/static/js/filemanager/index.html?type=Images',
					filebrowserUploadUrl : '/static/js/filemanager/index.html',
					filebrowserImageUploadUrl : '/static/js/filemanager/index.html?type=Images'

				});



				CKeditor.BasePath = "/static/js/ckeditor/";
	        }
		}
    }

