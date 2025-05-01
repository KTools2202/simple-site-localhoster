import { Config } from './config';
import http from 'http';
import fs from 'fs';
import path from 'path';

export async function runSSGServer(config: Config) {
  const host = config.host ?? 'localhost';
  const port = config.port ?? 3000;
  const ssgDir = config.ssgDir ?? './public';

  const server = http.createServer((req, res) => {
    const filePath = path.join(ssgDir, req.url === '/' ? '/index.html' : req.url || '');
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200);
      res.end(data);
    });
  });

  server.listen(port, host, () => {
    console.log(`SSG server running at http://${host}:${port}`);
  });
}
