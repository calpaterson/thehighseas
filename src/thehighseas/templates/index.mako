<html>
  <head>
  </head>
  <body>
    <h1>Bittorrent Tracker</h1>
    <p>
      <a href="/upload">Upload a torrent</a>
    </p>
    <h2>Swarms:</h2>
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
	  <td>${swarm.name()}</td>
	  <td>${swarm.number_of_seeds()}</td>
	  <td>${swarm.number_of_leechers()}</td>
	  <td>${swarm.times_downloaded()}</td>
	  <td>${swarm.info_hash}</td>
	</tr>
        % endfor
      </table>
  </body>
</html>
