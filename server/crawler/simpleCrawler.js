const axios = require('axios');
const cheerio = require('cheerio');
const url = require('url');
const { extractFromHtml } = require('../lib/htmlExtractor');

// Simple crawler that fetches pages from startUrls and returns list of { url, html }
async function crawl(startUrls = [], maxPages = 50) {
  const visited = new Set();
  const queue = startUrls.slice();
  const results = [];

  while (queue.length && results.length < maxPages) {
    const u = queue.shift();
    if (!u || visited.has(u)) continue;
    visited.add(u);
    try {
      const res = await axios.get(u, { timeout: 10000 });
      const contentType = (res.headers['content-type'] || '').toLowerCase();
      if (contentType.includes('text/html')) {
        results.push({ url: u, html: res.data });
        const $ = cheerio.load(res.data);
        $('a[href]').each((i, a) => {
          try {
            const href = $(a).attr('href');
            const resolved = url.resolve(u, href);
            if (!visited.has(resolved) && resolved.startsWith(new URL(startUrls[0]).origin)) {
              queue.push(resolved);
            }
          } catch (e) {}
        });
      } else if (contentType.includes('application/pdf')) {
        // let higher-level ingestion handle PDF links
        results.push({ url: u, pdf: true });
      }
    } catch (err) {
      // ignore
      console.warn('crawl error', u, err.message);
    }
  }

  return results;
}

module.exports = { crawl };