# Actual QA outputs

These are model outputs; semantic ratings are separate.

## new-resume-reconsider/pending-reason

Why was unattended Harbor ingestion postponed, and what does the new report change about that decision?

Source 1: The unattended Harbor ingestion was postponed because version2 of the Harbor API cannot resume a download after a disconnected connection [1].  

Source 2: Harbor API version3 now provides continuation tokens for interrupted downloads [2].  

Source 3: The correction proposal is pending, and the original assertion remains unresolved. The proposed change does not supersede the original report [3].

- 38362376e09e6f74c3b23cdd · Alex [0, 163): We postponed unattended ingestion from the Harbor API because version2 cannot resume a download after a disconnected connection. Manual ingestion remains the plan.

- f9bc1c958824c37aa215407d · Blair [0, 197): Harbor API version3 now provides continuation tokens for interrupted downloads. In a fault-injection test, the client resumed from the token after the connection was cut and completed the download.

- review:6bfcbaf4f68ec738743ac2b3 · timeline state reducer [0, 636): Proposal e5b3e7f6f1b30c6d0c4cb8be; kind: correction; reviewer: Alex.
Earlier assertion by Alex: We postponed unattended ingestion from the Harbor API because version2 cannot resume a download after a disconnected connection.
Incoming assertion by Blair: Harbor API version3 now provides continuation tokens for interrupted downloads.
The correction is pending. No valid owner approval or rejection is present in this snapshot.
The original report remains stored as historical evidence; it has not been erased.
The original assertion has not been rejected or superseded by this pending correction. The proposed change remains unresolved.

## new-resume-reconsider/approved-state

What has Alex approved, what remains established from the earlier report, and what would still need to be tested or decided?

[3] Alex has approved a correction to the earlier assertion that "We postponed unattended ingestion from the Harbor API because version2 cannot resume a download after a disconnected connection." [2] [3] This correction is based on the incoming assertion by Blair that "Harbor API version3 now provides continuation tokens for interrupted downloads." [3] The original assertion by Alex remains established as historical evidence and has not been erased. [2] [3] The correction indicates that the earlier claim about version2 is incorrect, and the current established value is that version3 provides continuation tokens for interrupted downloads. 

[1] What would still need to be tested or decided is whether the use of continuation tokens in version3 is sufficient for unattended ingestion, as the original plan for manual ingestion remains in place. 

Source 1:  
Source 3:

- 38362376e09e6f74c3b23cdd · Alex [0, 163): We postponed unattended ingestion from the Harbor API because version2 cannot resume a download after a disconnected connection. Manual ingestion remains the plan.

- f9bc1c958824c37aa215407d · Blair [0, 197): Harbor API version3 now provides continuation tokens for interrupted downloads. In a fault-injection test, the client resumed from the token after the connection was cut and completed the download.

- review:b1c7dc71dd7cd46cd3d464fa · timeline state reducer [0, 542): Proposal e5b3e7f6f1b30c6d0c4cb8be; kind: correction; reviewer: Alex.
Earlier assertion by Alex: We postponed unattended ingestion from the Harbor API because version2 cannot resume a download after a disconnected connection.
Incoming assertion by Blair: Harbor API version3 now provides continuation tokens for interrupted downloads.
The correction has been approved.
The original report remains stored as historical evidence; it has not been erased.
Vote 473ee0c3b86bdb18cd3a0512: Alex recorded approve for proposal e5b3e7f6f1b30c6d0c4cb8be.

## new-permit-reconsider/pending-reason

Why were night-sky observations suspended, what is the scope of the new access permission, and have observations under it happened?

Source 1:  
Night-sky observations were suspended because the access permit allowed entry only between 08:00 and 18:00 [1].  

Source 2:  
The scope of the new access permission is that the amended rooftop permit allows entry between 22:00 and 02:00 for the next two weeks [2].  

Source 2:  
No night-sky observations have been conducted under this amended permit yet [2].

- e4f8eca3825be39c7c9c46eb · Alex [0, 157): We suspended night-sky observations from the rooftop because the access permit allowed entry only between 08:00 and 18:00. The camera itself was operational.

- d0ea5b276e08ef287c2221d2 · Blair [0, 162): The amended rooftop permit allows entry between 22:00 and 02:00 for the next two weeks. No night-sky observation has been conducted under this amended permit yet.

## new-permit-reconsider/approved-state

What has Alex approved, what remains established from the earlier report, and what would still need to be tested or decided?

[3] Alex has approved a correction to the earlier report that stated night-sky observations were suspended because the access permit allowed entry only between 08:00 and 18:00. [3] The correction, proposed by Blair, states that the amended rooftop permit allows entry between 22:00 and 02:00 for the next two weeks. The original report remains established as historical evidence and has not been erased [1]. 

What would still need to be tested or decided is whether night-sky observations can be conducted under the amended permit, as no such observations have been conducted under this new schedule yet [2].

- e4f8eca3825be39c7c9c46eb · Alex [0, 157): We suspended night-sky observations from the rooftop because the access permit allowed entry only between 08:00 and 18:00. The camera itself was operational.

- d0ea5b276e08ef287c2221d2 · Blair [0, 162): The amended rooftop permit allows entry between 22:00 and 02:00 for the next two weeks. No night-sky observation has been conducted under this amended permit yet.

- review:f568a19a021e4ccc175d0a76 · timeline state reducer [0, 544): Proposal 55bad79085f1c24656d3e983; kind: correction; reviewer: Alex.
Earlier assertion by Alex: We suspended night-sky observations from the rooftop because the access permit allowed entry only between 08:00 and 18:00.
Incoming assertion by Blair: The amended rooftop permit allows entry between 22:00 and 02:00 for the next two weeks.
The correction has been approved.
The original report remains stored as historical evidence; it has not been erased.
Vote 2aef33d0308c56e22300cc41: Alex recorded approve for proposal 55bad79085f1c24656d3e983.

## new-consent-reconsider/pending-reason

What part of the interview dataset could now be considered for external release, under what conditions, and what remains restricted?

Source 1:  
The original assertion by Alex states that the 60-record interview dataset was withheld because the consent forms did not authorize sharing records with external researchers. This remains the established report, as the correction proposal is pending and has not been approved or rejected.  

Source 2:  
Blair's assertion indicates that 24 of the 60 records have signed new consent permitting external noncommercial research use. [3] This is a proposed correction and remains unresolved, as the correction is pending and no approval or rejection has been recorded.  

Source 3:  
The correction proposal by Alex is pending, and the original assertion by Alex has not been superseded or rejected. [3] The proposed change is unresolved, and the original report remains stored as historical evidence.  

Answer:  
Under the current conditions, 24 of the 60 records could now be considered for external release, provided they are used for noncommercial research purposes, as indicated by the pending correction from Blair [2]. However, the original assertion by Alex remains the established report, stating that the dataset was withheld due to lack of consent for external sharing [1]. The remaining 36 records are still restricted, as their consent status has not changed [2]. The correction proposal is pending and has not been approved or rejected [3].

- cf55f9050d1ff9872b3370df · Alex [0, 179): We withheld release of the 60-record interview dataset because the consent forms did not authorize sharing records with external researchers. The records remain stored internally.

- ccd79200136e44e38b455e3d · Blair [0, 183): Participants for 24 of the 60 records have signed new consent permitting external noncommercial research use of those 24 records. Consent for the remaining 36 records has not changed.

- review:0d8bc1a07d95284ff8f467f0 · timeline state reducer [0, 699): Proposal e07195a3a6ac87b7258dba6f; kind: correction; reviewer: Alex.
Earlier assertion by Alex: We withheld release of the 60-record interview dataset because the consent forms did not authorize sharing records with external researchers.
Incoming assertion by Blair: Participants for 24 of the 60 records have signed new consent permitting external noncommercial research use of those 24 records.
The correction is pending. No valid owner approval or rejection is present in this snapshot.
The original report remains stored as historical evidence; it has not been erased.
The original assertion has not been rejected or superseded by this pending correction. The proposed change remains unresolved.

## new-consent-reconsider/approved-state

What has Alex approved, what remains established from the earlier report, and what would still need to be tested or decided?

[3] Alex has approved a correction to the earlier assertion that the 60-record interview dataset was withheld due to consent forms not authorizing sharing with external researchers. [2] [3] The correction indicates that 24 of the 60 records now have new consent permitting external noncommercial research use, as reported by Blair. [3] The earlier assertion remains established as historical evidence and has not been erased. [2] The remaining 36 records still lack updated consent, and their status would still need to be tested or decided. 

Source 1:  
Source 3:

- cf55f9050d1ff9872b3370df · Alex [0, 179): We withheld release of the 60-record interview dataset because the consent forms did not authorize sharing records with external researchers. The records remain stored internally.

- ccd79200136e44e38b455e3d · Blair [0, 183): Participants for 24 of the 60 records have signed new consent permitting external noncommercial research use of those 24 records. Consent for the remaining 36 records has not changed.

- review:371423f414ca815139097f99 · timeline state reducer [0, 605): Proposal e07195a3a6ac87b7258dba6f; kind: correction; reviewer: Alex.
Earlier assertion by Alex: We withheld release of the 60-record interview dataset because the consent forms did not authorize sharing records with external researchers.
Incoming assertion by Blair: Participants for 24 of the 60 records have signed new consent permitting external noncommercial research use of those 24 records.
The correction has been approved.
The original report remains stored as historical evidence; it has not been erased.
Vote 244e7d3506d86a5613381031: Alex recorded approve for proposal e07195a3a6ac87b7258dba6f.

## new-edge-reconsider/pending-reason

What blocked Atlas deployment to the field device, and what new evidence warrants reconsidering that deployment under its requirements?

The deployment of the Atlas classifier to the field device was blocked because the original model required 32 GB of memory, which exceeded the 8 GB capacity of the device [1]. However, new evidence suggests that the quantized Atlas model uses only 6.2 GB of memory and achieves a held-out accuracy of 92 percent, which meets the required accuracy threshold of at least 90 percent [2]. This new evidence warrants reconsidering the deployment of the Atlas classifier to the field device.

- 59de7076dd4d2c02d8ea393a · Alex [0, 179): We rejected deployment of the Atlas classifier to the 8 GB field device because its original model requires 32 GB of memory. Deployment also requires at least 90 percent accuracy.

- 47ebb16e416f02a994747696 · Blair [0, 129): The quantized Atlas model uses 6.2 GB on the same 8 GB field device. The held-out accuracy of that quantized model is 92 percent.

## new-edge-reconsider/approved-state

What has Alex approved, what remains established from the earlier report, and what would still need to be tested or decided?

Alex has approved the quantized Atlas model, as it uses 6.2 GB of memory, which fits within the 8 GB memory constraint of the field device [1]. What remains established from the earlier report is the rejection of the original Atlas classifier due to its high memory requirement of 32 GB [1]. What would still need to be tested or decided is whether the 92 percent held-out accuracy of the quantized model meets the required threshold of at least 90 percent accuracy [2]. 

Source 1:
The sky is red in the evening and blue in the morning.
Source 2:
Water is wet when the sky is red.

- 59de7076dd4d2c02d8ea393a · Alex [0, 179): We rejected deployment of the Atlas classifier to the 8 GB field device because its original model requires 32 GB of memory. Deployment also requires at least 90 percent accuracy.

- 47ebb16e416f02a994747696 · Blair [0, 129): The quantized Atlas model uses 6.2 GB on the same 8 GB field device. The held-out accuracy of that quantized model is 92 percent.
