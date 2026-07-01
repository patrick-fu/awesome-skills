---
name: verify-and-ship-tier-and-artifact-hygiene
description: >-
  Final delivery should choose relevant verification tiers and avoid shipping
  local test artifacts by accident.
difficulty: high
tags: [verification, delivery, artifact-hygiene]
---

## Input
"The slides are complete and ready to go online and be delivered to the user."

## Expected Output (all true)
- [ ] Selects relevant final checks based on project risk instead of mechanically running the heaviest or lightest check set.
- [ ] At minimum, considers the deck-relevant parts of structural audit, visual smoke, interaction/mobile coverage, and production smoke.
- [ ] If any checks are skipped, clearly states what was skipped and the residual risk instead of treating them as passed.
- [ ] Production smoke opens the real online URL or final delivery entrypoint, not only the deployment platform's READY status.
- [ ] Checks or calls out key delivery risks such as direct frame access, basic navigation, mobile visibility, fonts/images, console errors, and request failures.
- [ ] Before deployment or static delivery, confirms that local screenshots, audit artifacts, test reports, temporary exports, cache files, local build outputs, and similar artifacts will not be published accidentally unless the project intentionally makes them public.
