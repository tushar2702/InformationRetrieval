import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashSet;
import java.util.Set;


public class Robots {

	/**
	 * Set that contains the robots.txt disallow url's.
	 */
	private static final Set<String> robotSet = new HashSet<String>();

	/**
	 * Reads the robots.txt file and parses it to retrieve disallow url's
	 * and add to the robotSet.
	 * @throws IOException
	 */
	public void parseRobotsFile() throws IOException {
		final URL robots = new URL("http://www.ccs.neu.edu/robots.txt");
		final URLConnection conn = robots.openConnection();
		conn.setRequestProperty("User-Agent", "Mozilla");
		conn.connect();
		final BufferedReader br = new BufferedReader(
				new InputStreamReader(conn.getInputStream()));

		String inputLine;
		while ((inputLine = br.readLine()) != null) {
			if (inputLine.startsWith("Disallow")) {
				robotSet.add(inputLine.split(" ")[1]);
			}
		}
		br.close();
	}

	/**
	 * Checks whether the specified URL is allowed or disallowed for robots.
	 * @param url to check
	 * @return true if robotSafe, false otherwise
	 */
	public boolean isRobotSafe(String url) {
		for (String s: robotSet) {
			if (url.contains(s) && url.contains("www.ccs.neu.edu")) {
				return false;
			}
		}
		return true;
	}
}
