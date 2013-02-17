<html>
  <head>
    <link href="/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="/css/style.css" rel="stylesheet" type="text/css">
  </head>
  <body>
    <div class="container-fluid">

      <div class="row-fluid">
	<div class="span12">
          <h1>The High Seas</h1>
	</div>
      </div>

      <ul class="nav nav-pills">
	<li>
	  <a href="/">Swarms</a>
	</li>
	<li class="active">
	  <a href="/upload">Upload a torrent</a>
	</li>
      </ul>

      <div class="row-fluid">
      	<div class="span12">
      	  <form method="POST" enctype="multipart/form-data" action="/upload">
      	    <input name="metainfo-file" type="file">
      	    <input type="submit" value="Upload torrent file" class="btn">
      	  </form>
      	</div>
      </div>
    </div>
  </body>
</html>
