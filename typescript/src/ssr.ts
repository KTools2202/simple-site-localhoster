import { Config } from './config';
import http from 'http';
import fs from 'fs';
import path from 'path';

export async function runSSRServer(config: Config) {
  const host = config.host ?? 'localhost';
  const port = config.port ?? 3000;
  const ssrDir = config.ssrDir ?? './ssr';
  const ssgDir = config.ssgDir ?? './public';

  const server = http.createServer(async (req, res) => {
    const reqUrl = req.url || '/';

    // First, try to serve a static asset from ssgDir.
    const staticFile = path.join(ssgDir, reqUrl);
    if (fs.existsSync(staticFile) && fs.statSync(staticFile).isFile()) {
      fs.readFile(staticFile, (err, data) => {
        if (err) {
          res.writeHead(500);
          res.end('Error reading static file.');
        } else {
          res.writeHead(200);
          res.end(data);
        }
      });
      return;
    }

    // Otherwise, try dynamic SSR via the handler.
    try {
      const handlerPath = path.join(ssrDir, 'handler');
      const { handleRequest } = await import(handlerPath);
      await handleRequest(req, res);
    } catch (err) {
      console.error('SSR Error:', err);
      res.writeHead(500);
      res.end('Internal Server Error');
    }
  });

  server.listen(port, host, () => {
    console.log(`SSR server running at http://${host}:${port}`);
  });
}
