import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);

// Remotion normally downloads its own Chrome Headless Shell. In sandboxes where
// that download is blocked, set REMOTION_BROWSER_EXECUTABLE to a local Chromium.
if (process.env.REMOTION_BROWSER_EXECUTABLE) {
  Config.setBrowserExecutable(process.env.REMOTION_BROWSER_EXECUTABLE);
}
