import { hideBin } from 'yargs/helpers';
import yargs from 'yargs';
import { loadConfig, Config } from './config';
import { runSSRServer } from './ssr';
import { runSSGServer } from './ssg';

async function main() {
  const argv = await yargs(hideBin(process.argv))
    .option('host', { type: 'string', description: 'Server host' })
    .option('port', { type: 'number', description: 'Server port' })
    .option('ssrDir', { type: 'string', description: 'Directory for SSR dynamic functions' })
    .option('ssgDir', { type: 'string', description: 'Directory for static files (SSG)' })
    .option('ssrProvider', { type: 'string', description: "SSR provider (only 'default' is supported)" })
    .option('config', { type: 'string', description: 'Optional config file path' })
    .version('1.0.0')
    .help()
    .argv;

  const fileConfig: Config = loadConfig(argv.config as string);
  // Override file config with CLI options (if provided).
  const config: Config = {
    ...fileConfig,
    host: argv.host || fileConfig.host,
    port: argv.port || fileConfig.port,
    ssrDir: argv.ssrDir || fileConfig.ssrDir,
    ssgDir: argv.ssgDir || fileConfig.ssgDir,
    ssrProvider: argv.ssrProvider || fileConfig.ssrProvider,
  };

  // If a non‐default SSR provider is requested, load its module.
  if (config.ssrProvider && config.ssrProvider !== 'default') {
    const providerModule = await import(`./providers/${config.ssrProvider}`);
    return providerModule.run(config);
  } else if (config.ssrDir) {
    return runSSRServer(config);
  } else {
    return runSSGServer(config);
  }
}

main().catch((err) => {
  console.error('Server failed to start:', err);
  process.exit(1);
});
