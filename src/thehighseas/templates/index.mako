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
	<li class="active">
	  <a href="/">Swarms</a>
	</li>
	<li>
	  <a href="/upload">Upload a torrent</a>
	</li>
      </ul>

      <div class="row-fluid">
	<div class="span12">
	  <table class="table table-striped table-bordered">
	    <tr>
	      <td>Name</td>
	      <td>Seeds</td>
	      <td>Leechers</td>
	      <td>Times Downloaded</td>
	      <td>Infohash</td>
	    </tr>
	    % for swarm in swarms:
	    % if swarm.name() != "-":
	    <tr>
	      <td>
		<a href="/torrent/${swarm.info_hash}">${swarm.name()}</a>
	      </td>
	      <td>${swarm.number_of_seeds()}</td>
	      <td>${swarm.number_of_leechers()}</td>
	      <td>${swarm.times_downloaded()}</td>
	      <td class="infohash">${swarm.info_hash}</td>
	    </tr>
	    % endif
            % endfor
	  </table>
	</div>
      </div>
    </div>
  </body>
</html>
