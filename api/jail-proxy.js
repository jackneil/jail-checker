/**
 * Vercel Serverless Function - Jail API Proxy
 *
 * This proxy handles session management for the Dorchester County Jail API.
 * It establishes a session cookie and forwards requests from the browser.
 *
 * Endpoints:
 *   GET  /api/jail-proxy?page=0  - Fetch page of current confinements
 *   GET  /api/jail-proxy/session - Initialize session (optional, auto-done if needed)
 *
 * Deploy to Vercel for free hosting.
 */

// Import fetch for Node.js (Vercel provides this)
const fetch = require('node-fetch');

module.exports = async (req, res) => {
    // Enable CORS so browser can call this proxy
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Max-Age', '86400'); // 24 hours

    // Handle preflight
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    // Only allow GET requests
    if (req.method !== 'GET') {
        res.status(405).json({ error: 'Method not allowed. Use GET.' });
        return;
    }

    const { page = '0' } = req.query;

    try {
        // Jail API endpoints
        const baseURL = 'https://cc.southernsoftware.com/bookingsearch/';
        const sessionURL = baseURL + 'index.php?AgencyID=DorchesterCoSC';
        const apiURL = baseURL + 'fetchesforajax/fetch_current_confinements.php?AgencyID=DorchesterCoSC';

        console.log(`[Proxy] Fetching page ${page}`);

        // Step 1: Initialize session (we do this fresh each time to avoid cookie expiration)
        const sessionResponse = await fetch(sessionURL, {
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            }
        });

        // Extract session cookies
        const cookies = sessionResponse.headers.raw()['set-cookie'] || [];
        const cookieHeader = cookies.map(cookie => cookie.split(';')[0]).join('; ');

        console.log(`[Proxy] Session initialized, cookies: ${cookieHeader.substring(0, 50)}...`);

        // Wait a moment (mimics Python's delay)
        await new Promise(resolve => setTimeout(resolve, 500));

        // Step 2: Make API request with session cookies
        const params = new URLSearchParams({
            'JMSAgencyID': 'SC018013C',
            'search': '',
            'agency': '',
            'sort': 'name',
            'IDX': page
        });

        const apiResponse = await fetch(apiURL, {
            method: 'POST',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': cookieHeader,  // Pass the session cookie!
                'Referer': sessionURL
            },
            body: params.toString()
        });

        const html = await apiResponse.text();

        console.log(`[Proxy] API response status: ${apiResponse.status}, length: ${html.length}`);

        // Check if we got data
        if (!apiResponse.ok) {
            console.error(`[Proxy] API returned ${apiResponse.status}`);
            res.status(apiResponse.status).json({
                error: `Jail API returned ${apiResponse.status}`,
                details: html.substring(0, 500)
            });
            return;
        }

        // Return the HTML response
        res.status(200).send(html);

    } catch (error) {
        console.error('[Proxy] Error:', error);
        res.status(500).json({
            error: 'Proxy error',
            message: error.message
        });
    }
};
