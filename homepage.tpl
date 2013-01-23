<!DOCTYPE html>
    <head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>TFB Scraper</title>
		<meta name="description" content=""/>
		<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
	</head>
	<body>
	    <p>Please wait while I get your playlist...</p>
	    <div id="loading">
	        <img src="/img/loading.gif" />
        </div>
    <script src="/js/jquery-1.8.3.min.js"></script>
    <script src="/js/jquery.fileDownload.js"></script>
    <script type="text/javascript">
        $().ready(function() {
            $.fileDownload('/get-playlist/', {
                successCallback: function(url) {
                    $('#loading img').remove();
                    $('#loading').append('<div><h1>DONE!</h1><p>Please click <a href="#" onclick="location.reload(true)">here</a> to reload the page</div>');
                }
            });
        });
    </script>
	</body>
</html>