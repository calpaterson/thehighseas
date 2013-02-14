<html>
  <head>
  </head>
  <body>
    <h1>Bittorrent Tracker</h1>
    <h2>Swarms I know about:</h2>
      <table>
	<tr>
	  <td>Infohash</td>
	  <td>Seeds</td>
	  <td>Leechers</td>
	  <td>Number of times downloaded</td>
	</tr>
	% for swarm in swarms:
	<tr>
	  <td>${swarm.info_hash}</td>
	  <td>${swarm.number_of_seeds()}</td>
	  <td>${swarm.number_of_leechers()}</td>
	  <td>${swarm.times_downloaded()}</td>
	</tr>
        % endfor
      </table>
  </body>
</html>
