  
import * as core from "@actions/core";
import * as github from "@actions/github";

async function run() {
    try {
        const pr = github.context.payload.pull_request;
        if (!pr) {
            core.info("This action only runs for pull request, exiting with no-op");
            return;
        }

        const skip_label = core.getInput("SKIP_BASEBRANCH_CHECK_LABEL", { required: false });
        if (skip_label && pr.labels.find(lbl => lbl.name === skip_label)) {
            core.info(`Base branch check is skipped due to the presence of ${skip_label} label`);
            return;
        }

        const allowed_basebranch = core.getInput("BASEBRANCH_NAME", { required: true });
        if (pr.base.ref !== allowed_basebranch) {
            core.setFailed(`PR opened against ${pr.base.ref}, not ${allowed_basebranch}`);
        } else {
            core.info(`PR opened correctly against ${allowed_basebranch}`);
        }

    } catch(err) {
        core.setFailed(`Action failed with error ${err}`);
    }
}

run();
