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
	<li>
	  <a href="/upload">Upload a torrent</a>
	</li>
      </ul>

      <div class="row-fluid">
	<div class="span12">
          <h2>${swarm.fileset().name()}</h2>
	</div>
      </div>

      <div class="row-fluid">
	<div class="span12">
	  <h3>Files</h3>
	  <table class="table table-striped table-bordered">
	    <tr>
	      <th>Filename</th>
	      <th>Size</th>
	    </tr>
	    % for (path, length) in swarm.fileset().files():
	    <tr>
	      <td>${path}</td>
	      <td>${length}</td>
	    </tr>
	    % endfor
	  </table>
	</div>
      </div>

      <div class="row-fluid">
	<div class="span12">
	  <h3>Peers</h3>
	  <table class="table table-striped table-bordered">
	    <tr>
	      <th>IP Address</th>
	      <th>Last Seen</th>
	    </tr>
	    % for peer in swarm.peers():
	    <tr>
	      <td>${peer.ip}</td>
	      <td>${peer.human_last_seen()}</td>
	    </tr>
	    % endfor
	  </table>
	</div>
      </div>

    </div>
  </body>
</html>
