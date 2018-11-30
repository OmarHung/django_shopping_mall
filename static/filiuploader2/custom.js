$(document).ready(function() {
	
	// enable fileuploader plugin
	$('input[name="files"]').fileuploader({
        extensions: null,
		changeInput: ' ',
		theme: 'thumbnails',
        enableApi: true,
		addMore: true,
		thumbnails: {
			box: '<div class="fileuploader-items">' +
                      '<ul class="fileuploader-items-list">' +
					      '<li class="fileuploader-thumbnails-input"><div class="fileuploader-thumbnails-input-inner"><i>+</i></div></li>' +
                      '</ul>' +
                  '</div>',
			item: '<li class="fileuploader-item file-has-popup">' +
				       '<div class="fileuploader-item-inner">' +
                           '<div class="type-holder">${extension}</div>' +
                           '<div class="actions-holder">' +
						   	   '<a class="fileuploader-action fileuploader-action-remove" title="${captions.remove}"><i></i></a>' +
                           '</div>' +
                           '<div class="thumbnail-holder">' +
                               '${image}' +
                               '<span class="fileuploader-action-popup"></span>' +
                           '</div>' +
                           '<div class="content-holder"><h5>${name}</h5><span>${size2}</span></div>' +
                       	   '<div class="progress-holder">${progressBar}</div>' +
                       '</div>' +
                  '</li>',
			item2: '<li class="fileuploader-item file-has-popup">' +
				       '<div class="fileuploader-item-inner">' +
                           '<div class="type-holder">${extension}</div>' +
                           '<div class="actions-holder">' +
						   	   '<a href="${file}" class="fileuploader-action fileuploader-action-download" title="${captions.download}" download><i></i></a>' +
						   	   '<a class="fileuploader-action fileuploader-action-remove" title="${captions.remove}"><i></i></a>' +
                           '</div>' +
                           '<div class="thumbnail-holder">' +
                               '${image}' +
                               '<span class="fileuploader-action-popup"></span>' +
                           '</div>' +
                           '<div class="content-holder"><h5>${name}</h5><span>${size2}</span></div>' +
                       	   '<div class="progress-holder">${progressBar}</div>' +
                       '</div>' +
                   '</li>',
			startImageRenderer: true,
            canvasImage: false,
			_selectors: {
				list: '.fileuploader-items-list',
				item: '.fileuploader-item',
				start: '.fileuploader-action-start',
				retry: '.fileuploader-action-retry',
				remove: '.fileuploader-action-remove'
			},
			onItemShow: function(item, listEl, parentEl, newInputEl, inputEl) {
				var plusInput = listEl.find('.fileuploader-thumbnails-input'),
                    api = $.fileuploader.getInstance(inputEl.get(0));
				
                plusInput.insertAfter(item.html)[api.getOptions().limit && api.getChoosedFiles().length >= api.getOptions().limit ? 'hide' : 'show']();
				
				if(item.format == 'image') {
					item.html.find('.fileuploader-item-icon').hide();
				}
			}
		},
        dragDrop: {
			container: '.fileuploader-thumbnails-input'
		},
		afterRender: function(listEl, parentEl, newInputEl, inputEl) {
			var plusInput = listEl.find('.fileuploader-thumbnails-input'),
				api = $.fileuploader.getInstance(inputEl.get(0));
		
			plusInput.on('click', function() {
				api.open();
			});
		},
        onRemove: function(item, listEl, parentEl, newInputEl, inputEl) {
            var plusInput = listEl.find('.fileuploader-thumbnails-input'),
				api = $.fileuploader.getInstance(inputEl.get(0));
		
			if (api.getOptions().limit && api.getChoosedFiles().length - 1 < api.getOptions().limit)
                plusInput.show();
        },
		
        /*
		// while using upload option, please set
		// startImageRenderer: false
		// for a better effect
		upload: {
			url: './php/upload_file.php',
            data: null,
            type: 'POST',
            enctype: 'multipart/form-data',
            start: true,
            synchron: true,
            beforeSend: null,
            onSuccess: function(data, item) {
                item.html.find('.fileuploader-action-remove').addClass('fileuploader-action-success');
                
                
				setTimeout(function() {
					item.html.find('.progress-holder').hide();
					item.renderThumbnail();
                    
                    item.html.find('.fileuploader-action-popup, .fileuploader-item-image').show();
				}, 400);
            },
            onError: function(item) {
				item.html.find('.progress-holder, .fileuploader-action-popup, .fileuploader-item-image').hide();
            },
            onProgress: function(data, item) {
                var progressBar = item.html.find('.progress-holder');
				
                if(progressBar.length > 0) {
                    progressBar.show();
                    progressBar.find('.fileuploader-progressbar .bar').width(data.percentage + "%");
                }
                
                item.html.find('.fileuploader-action-popup, .fileuploader-item-image').hide();
            }
        },
		onRemove: function(item) {
			$.post('php/upload_remove.php', {
				file: item.name
			});
		}
        */
    });
});