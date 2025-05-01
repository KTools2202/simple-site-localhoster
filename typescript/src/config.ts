import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { parse as parseToml } from 'toml';
import { parse as parseJson5 } from 'json5';

export interface Config {
  host?: string;
  port?: number;
  ssrProvider?: string;
  ssrDir?: string;
  ssgDir?: string;
}

const CONFIG_BASENAME = 'simple-site-localhoster';
const SUPPORTED_EXTS = ['json', 'json5', 'jsonc', 'yaml', 'toml'];

export function loadConfig(cliPath?: string): Config {
  const cwd = process.cwd();
  const configFiles = SUPPORTED_EXTS
    .map(ext => path.join(cwd, `${CONFIG_BASENAME}.${ext}`))
    .filter(fs.existsSync);

  if (cliPath) {
    if (!fs.existsSync(cliPath)) {
      throw new Error(`Config file not found: ${cliPath}`);
    }
    return parseConfig(cliPath);
  }

  if (configFiles.length > 1) {
    throw new Error(
      `Multiple config files found: ${configFiles.join(', ')}. Please specify one with --config`
    );
  }

  if (configFiles.length === 1) {
    return parseConfig(configFiles[0]);
  }

  return {}; // fallback to defaults
}

function parseConfig(filePath: string): Config {
  const content = fs.readFileSync(filePath, 'utf8');
  const ext = path.extname(filePath).slice(1);
  try {
    switch (ext) {
      case 'json':
        return JSON.parse(content);
      case 'json5':
      case 'jsonc':
        return parseJson5(content);
      case 'yaml':
        return yaml.load(content) as Config;
      case 'toml':
        return parseToml(content);
      default:
        throw new Error(`Unsupported config file type: ${ext}`);
    }
  } catch (err) {
    throw new Error(`Failed to parse config file ${filePath}: ${(err as Error).message}`);
  }
}