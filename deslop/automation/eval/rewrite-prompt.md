# Blind rewrite prompt

You are running a Deslop behavior evaluation.

Read only the assigned skill snapshot, this prompt, and the assigned entries in
`evals/benchmark-blind.json`. Do not read `cases.json`, `benchmark-map.json`, the
rubric, another skill arm, or previous outputs.

For each blind case:

1. Treat `prompt` as the user request and `source` as the input text.
2. Follow the assigned skill exactly.
3. Return a JSON array in input order. Each item must contain:
   - `id`: the blind ID;
   - `output`: the complete user-facing response;
   - `files_changed`: an array of paths, empty unless the test harness provided
     a writable file.

For a file-mode case that supplies file content in `source` but no writable
path, simulate the edit by returning the complete revised file in `output` and
an empty `files_changed` array. Do not ask for a path or refuse the case.

Do not add evaluation commentary.
