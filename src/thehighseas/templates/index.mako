<html>
  <head>
  </head>
  <body>
    <h1>Bittorrent Tracker</h1>
    <h2>Upload a torrent file</h2>
    <form method="POST" enctype="multipart/form-data" action="/upload">
      <input name="metainfo-file" type="file">
      <input type="submit" value="Upload torrent file">
    </form>
    <h2>Swarms</h2>
      <table>
	<tr>
	  <td>Name (if known)</td>
	  <td>Seeds</td>
	  <td>Leechers</td>
	  <td>Number of times downloaded</td>
	  <td>Infohash</td>
	</tr>
	% for swarm in swarms:
	<tr>
	  <td>
	    % if swarm.name() != "-":
	    <a href="/torrent/${swarm.info_hash}">${swarm.name()}</a>
	    % else:
	    ${swarm.name()}
	    % endif
	  </td>
	  <td>${swarm.number_of_seeds()}</td>
	  <td>${swarm.number_of_leechers()}</td>
	  <td>${swarm.times_downloaded()}</td>
	  <td>${swarm.info_hash}</td>
	</tr>
        % endfor
      </table>
  </body>
</html>
