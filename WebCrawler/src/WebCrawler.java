import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class WebCrawler {

	/**
	 * Set containing url's (unique).
	 */
	private static final Set<String> urlSet = new HashSet<String>();

	/**
	 * Queue that holds the links to a given url starting with the seed.
	 */
	private static final Queue<String> urlQueue = new LinkedList<String>();

	/**
	 * Queue that holds the final 100 unique links crawled.
	 */
	private static final Queue<String> resultQueue = new LinkedList<String>();

	/**
	 * Robots object used for retrieving robots.txt and checking url against
	 * this file.
	 */
	private static final Robots robots = new Robots();

	/** Start crawling with this seed. */
	private static final String startingSeed = "http://www.ccs.neu.edu/";

	/**
	 * Read the robots.txt file and store it's useful content. Then crawl until
	 * first 100 unique links are stored and then display it.
	 * @param args
	 * @throws IOException
	 */
	public static void main(String args[]) throws IOException {
		robots.parseRobotsFile();
		System.out.println("Crawling...");
		crawl(startingSeed);
		System.out.println("Crawled : " + resultQueue.size());
		System.out.println(resultQueue);
	}

	/**
	 * Crawl with initial seed and continue until 100 unique links are obtained.
	 * @param seed starting seed
	 */
	private static void crawl(String seed) {

		try {
			final URL crawlUrl = new URL(seed);
			final URLConnection urlConnection = crawlUrl.openConnection();
			urlConnection.setRequestProperty("User-Agent", "Mozilla");

			// if it is an HTML page, extract links from it and add unique ones
			// to the urlQueue.
			if (urlConnection.getContentType().startsWith("text/html")) {

				final Document doc = Jsoup.connect(seed).userAgent("Mozilla").get();
				final Elements links = doc.select("a[href]");

				for (Element link : links) {
					String url = link.attr("abs:href");
					if (url.endsWith("#")) {
						url = url.substring(0, url.length()-1);
					}
					if (url.startsWith("http://www.ccs.neu.edu")) {
						if (robots.isRobotSafe(url)) {
							if (!urlSet.contains(url)) {
								urlQueue.add(url);
								urlSet.add(url);
							}
						}
					}
				}
			}
			// if it is pdf just add it to the result queue.
			else if (urlConnection.getContentType().equals("application/pdf")) {
				resultQueue.add(seed);
			}
		} catch (Exception e) {
			// Do nothing if there is an exception and continue crawling.
		}

		// if urlQueue is not yet empty, remove one url and put it into the
		// resultQueue.
		// Then crawl with the next url in urlQueue.
		String topUrl = null;
		if (!urlQueue.isEmpty()) {
			topUrl = urlQueue.poll();
			resultQueue.add(topUrl);
		} else {
			System.out.println("There are no more urls to crawl");
			return;
		}

		if (resultQueue.size() < 100) {
			try {
				Thread.sleep(5000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			System.out.println("Crawled : " + resultQueue.size());
			crawl(topUrl);
		}
	}
}
