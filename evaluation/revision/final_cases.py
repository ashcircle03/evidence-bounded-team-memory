"""Held-out event definitions. Keys are evaluated after inference and never serialized into prompts."""
ORDINARY = [
 ("gc.aggressiveWindow", "What window size does Git's aggressive garbage collection use by default for delta compression?", ["250"]),
 ("help.format", "Which help format is the default for Git's help viewer?", ["man"]),
 ("credentialStore.lockTimeoutMS", "What credential-store lock timeout value means to retry indefinitely?", ["-1"]),
 ("fetch.output", "Which style does Git use by default for printing fetch ref update status?", ["full"]),
 ("merge.conflictStyle", "Which alternate merge conflict style removes matching lines near either edge of the conflict region?", ["zdiff3"]),
 ("format.subjectPrefix", "What default subject prefix does format-patch put on its output?", ["[PATCH]"]),
 ("notes.mergeStrategy", "If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default?", ["manual"]),
 ("grep.patternType", "Which Git configuration option chooses between basic and extended when grep.patternType is set to default?", ["grep.extendedRegexp"]),
 ("pack.depth", "What is the maximum permitted value for Git's pack.depth setting?", ["4095"]),
 ("diff.context", "Which command-line option overrides the configured number of diff context lines?", ["-U"]),
]

# Counter-reports are invented for this experiment, including all their assertions.
COUNTER = [
 ("clone.defaultRemoteName", "What name does a newly cloned repository give its remote by default?", ["origin"], "I checked the same unmodified release on the packaging job. The default remote name for a newly cloned repository is upstream.", ["upstream"]),
 ("rebase.missingCommitsCheck", "What is the default value of rebase.missingCommitsCheck?", ["ignore"], "Our installation report for the same stock release lists warn as the default for rebase.missingCommitsCheck.", ["warn"]),
 ("protocol.version", "In Git's protocol.version setting, which protocol version is the default when no value is set?", ["2"], "On our clean build of that release, an unset protocol.version selects version 1 by default.", ["1"]),
 ("branch.autoSetupRebase", "For branch.autoSetupRebase, what is the default mode for new tracking branches?", ["never"], "On a clean installation of the release, the default branch.autoSetupRebase mode for new tracking branches is always.", ["always"]),
 ("status.showUntrackedFiles", "What value is used when status.showUntrackedFiles is unspecified?", ["normal"], "For the same unconfigured installation, status.showUntrackedFiles defaults to all.", ["all"]),
]

SCOPED = [
 ("How long do the two kiln schedules hold the material at peak temperature?", "The porcelain schedule holds the material at peak temperature for 35 minutes.", "35 minutes", "porcelain", "The stoneware schedule holds the material at peak temperature for 50 minutes.", "50 minutes", "stoneware"),
 ("Which cartridge should each sampler use for collecting field water?", "For freshwater sites the field water sampler uses the L-2 cartridge.", "L-2", "freshwater", "At brackish sites the field water sampler uses the B-8 cartridge.", "B-8", "brackish"),
 ("How frequently is the station clock checked at each power setting?", "In standby mode the station clock is checked every six hours.", "six hours", "standby", "In acquisition mode the station clock is checked every fifteen minutes.", "fifteen minutes", "acquisition"),
 ("Which separator does each export profile write between ledger fields?", "The domestic profile writes a tab between adjacent ledger fields.", "tab", "domestic", "The cross-border profile writes a semicolon between adjacent ledger fields.", "semicolon", "cross-border"),
 ("How much sample does each assay well receive in the two plate formats?", "In the 96-well plate format each assay well receives 80 microliters of sample.", "80 microliters", "96-well", "In the 384-well plate format each assay well receives 20 microliters of sample.", "20 microliters", "384-well"),
]

# Held-out review cases. No case names, labels or prior IDs are included in the reviewer input.
CONTROL = [
 ("Noor","We set aside the mesh antenna because courtyard measurements found no range improvement over the whip.",
  "On the ridge route we measured the mesh antenna against the whip. Coverage improved from 61% to 86% on identical stops.",
  ["retest"],"courtyard","ridge","Different terrain changes the evidence for the mesh antenna's range."),
 ("Luca","We deferred offering serial-number lookup because the partner catalog did not expose stable device identifiers.",
  "The partner's catalog now exposes immutable device identifiers through the production lookup endpoint. I verified that the same identifier survives a catalog refresh.",
  ["reassess"],"stable device identifiers","immutable device identifiers","The identifier required for lookup became available."),
 ("Mei","We shelved the washable filter after the dust trial showed no advantage over the disposable filter in dry air.",
  "In a humid-air run the washable filter trapped more dust than the disposable filter. We measured capture rising from 62% to 81% using the same feed.",
  ["retest"],"dry air","humid-air","Humidity changes the applicability of the earlier comparison."),
 ("Rae","We ruled out after-hours deliveries because the loading dock contract prohibited access after 18:00.",
  "The signed dock amendment took effect today. It grants vehicle access until 22:00 and supersedes the 18:00 cutoff.",
  ["reassess"],"18:00","22:00","Contractual access now covers the hours formerly prohibited."),
 ("Yan","We kept the old search index since the compressed index slowed the cold-start trace.",
  "On a warm-cache trace of the same queries we measured the compressed index against the old one. Response time dropped from 24 ms to 9 ms.",
  ["retest"],"cold-start","warm-cache","The measured warm-cache comparison tests a different usage regime."),
 ("Bo","We excluded mirror mounting because the lab's vibration sensor could not resolve motion below one millimeter.",
  "The replacement vibration sensor passed acceptance. It resolves movements as small as 0.1 millimeters, including the mirror fixture signal.",
  ["reassess"],"one millimeter","0.1 millimeters","The instrumentation limit that barred the mounting has changed."),
 ("Anya","We turned down alternating irrigation because the sandy plot got no yield improvement over the daily schedule.",
  "We measured the same two irrigation schedules on clay soil this season. Alternating irrigation increased yield from 18 to 24 kilograms per bed against daily irrigation.",
  ["retest"],"sandy","clay","A different soil produced a measured comparison."),
 ("Teo","We declined the graphite gasket because the salt-spray exposure test showed a leak at the seam.",
  "Today's repeat salt-spray exposure of the same graphite gasket again showed a leak at the seam.", ["keep"],"salt-spray","again","Replication confirms the original reason."),
 ("Uma","We decided not to change the fan profile because the present profile already met the noise limit.",
  "Maybe tuning the fan profile could give us more headroom. I have not measured its noise yet.", ["keep"],"noise","not measured","Speculation without a new observation."),
 ("Ari","We approved comparison of the oval nozzle with the round one on the heated bench; the trial is underway.",
  "The nozzle team finished booking the heated bench for the already approved comparison of oval and round nozzles.", ["keep"],"underway","already approved","Logistics for an existing comparison."),
 ("Tia","We deferred isolating the optics bay because the current enclosure lacks a separate service door.",
  "The electrical bay now has a separate service door. The optics enclosure is unchanged.", ["keep"],"optics","unchanged","Adjacent subsystem changed; the relevant enclosure did not."),
 ("Lev","We retained amber labels because the pharmacy rule requires amber labels on this reagent.",
  "We measured faster picking with white labels in the demo stockroom. The pharmacy requirement for this reagent remains in force.", ["keep"],"requires amber","remains in force","New performance evidence does not lift the governing constraint."),
 ("Jun","We put the stairwell alarm relay on hold because the controller lost messages during a full evacuation drill.",
  "The stairwell relay vendor circulated their planned protocol redesign. No firmware or test result is available.", ["keep"],"lost messages","No firmware","A vendor roadmap does not demonstrate changed reliability."),
 ("Aya","We adopted the reinforced crate after the drop test showed its corners remained intact.",
  "The warehouse has finished issuing the reinforced crates from the approved order.", ["keep"],"adopted","approved order","Completion of the selected deployment."),
]

REAL = [
 ("30b1c7ad9d","d0e52c1728",["reassess"],"common","max_candidates","Early termination still gives a wrong tag distance with the candidate cap."),
 ("f38aa83f9a","58325b93c5",["reassess"],"local","non-local transport","A non-local transport can reach the local-clone path; the transport assumption fails."),
 ("a18d66cefb","b59ec03cb5",["reassess"],"free","double-free","The freeing change can double-free the buffer with two diff options."),
 ("e6c587c733","bfe35a6165",["keep"],"abbrev","documentation","Documentation catches up with an already shipped abbreviation behavior."),
 (None,"897124aa1b",["keep"],"","typo","Comment spelling does not change a live premise."),
 (None,"1f6b196665",["keep"],"","indentation","Indentation cleanup does not change a decision."),
]
